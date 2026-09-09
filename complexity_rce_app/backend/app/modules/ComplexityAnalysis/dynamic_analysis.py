import scipy
import math 
import numpy as np
import docker
import subprocess, json
import random
import string

client = docker.from_env()

def calculate_dynamic_complexity(container, script_path, input_type, number_data_points):
    try:
        n, time = execute_script_with_autogenerate_data(container, script_path, input_type, number_data_points)
    except:
        raise
    
    #Compaaring models with Residual Sum of Squares 
    print("Fitting model to data:")
    predictions = {}
    for name, model_func, k in [
        #k = number of model parameters -> used for aic
        ("constant",  constant_progression, 1),
        ("logarithmic",  logarithmic_progression, 2),
        ("polynomial",  polynomial_progression, 3),
         ("exponential",  exponential_progression, 3)
    ]:
        p0 = get_initial_guess(name, n, time)
        try:
            params, covariance = scipy.optimize.curve_fit(f=model_func,xdata=n, ydata=time, p0=p0, maxfev=1500)
        except RuntimeError as e:
            print(f"Model '{name}' failed to converge, skipping: {e}")
            continue
        
        y_predicted = [model_func(ni, *params) for ni in n]
        #Using Reverse Square sum to calculate the difference between measured and predicted data
        rss = sum((ti - yi) ** 2 for ti, yi in zip(time, y_predicted))
        
        #Akaike’s Information Criterion is used to find the best model https://www.statisticshowto.com/akaikes-information-criterion/
        #Since we only have four models second order AIC is necessary 
        aic = len(n) * math.log(rss) + 2 * k
        aicc = aic + (2 * k * (k + 1)/(len(n)-k-1))
        predictions[name] = {"params": params, "rss": rss, "aicc": aicc}
    
    best_model = min(predictions, key=lambda name: predictions[name]["aicc"])
    print("Best Model: " + best_model)
    
    dynamicComplexity = best_model
    dynamic_data_points = [n, time]
    params = predictions[best_model]["params"].tolist()
    print(params)
    return dynamicComplexity, dynamic_data_points, params

#TODO: Test length should be up to the user (and the power scaling propably too)
def execute_script_with_autogenerate_data(container, script_path, input_type, test_length=5, input_scaling=3):
    try:
        match input_type:
            case "string":
                values = [(''.join(random.choices(string.ascii_letters + string.digits, 
                                                  k=int(math.pow(i, input_scaling))))) for i in range(test_length)]
                random.shuffle(values)
                n = [len(s) for s in values]
            case "int":
                values = [int(math.pow(i, input_scaling) + random.random()) for i in range(test_length)]
                
                random.shuffle(values)
                n = [x for x in values]
            case "float":
                values = [math.pow(i, input_scaling) + random.random() for i in range(test_length)]
            case "string[]":
                values = []
                for i in range (test_length) :
                    value = [(''.join(random.choices(string.ascii_letters + string.digits, k=int(math.pow(j, input_scaling))))) for j in range(int(math.pow(i + random.random(), input_scaling)))]
                    random.shuffle(value)
                    values.append(value)
                    
                random.shuffle(values)
                n = [len(a) for a in values]
            case "int[]":
                values = []
                for i in range(test_length) :
                    value = [int(math.pow(j + random.random(), input_scaling)) for j in range(int(math.pow(i + random.random(), input_scaling)))]
                    random.shuffle(value)
                    values.append(value)
                    
                random.shuffle(values)
                n = [len(a) for a in values]
            case "float[]":
                values = []
                for i in range(test_length) :
                    value = [math.pow(j, input_scaling) + random.random() for j in range(int(math.pow(i + random.random(), input_scaling)))]
                    random.shuffle(value)
                    values.append(value)
                random.shuffle(values)
                n = [len(a) for a in values]
            case "adjacency-matrix":
                values = []
                for i in range(test_length * input_scaling):
                    matrix = []
                    for y in range(i):
                        row = []
                        for x in range(i):
                            row.append(int(random.getrandbits(1)))
                        matrix.append(row)
                        
                    values.append(matrix)
                random.shuffle(values)
                #number of vertecies in matrix
                n = [len(m) for m in values]
            case _:
                #TODO: Possibly allow for not using dynamic measuring?
                raise ValueError("Input Type not supported!")
        inputs, times = fullRun(values, container, script_path)
        return n, times    
                
    except:
        raise

def fullRun(values, container, script_path):
    try:
        inputs = []
        times = []
        for n in values:
            result, duration = medianRunScript(n, container, script_path)
            inputs.append(n)
            times.append(duration)
        return inputs, times
    except:
        raise
        
def medianRunScript(n, container, script_path):
    try:
        values = []
        for i in range(3):
            reset_environment(container)
            output, duration = run_with_input(container.short_id, script_path, n)
            values.append((output, duration))
        
        return sorted(values, key=lambda tupple: tupple[1])[1]
    except:
        raise
        

def reset_environment(container):
    exit_code, output = container.exec_run(
    ["sh", "-c", "find /tmp -mindepth 1 ! -name 'main.py' -delete"]
    #sh -c runs a shell command 
    #-mindepth 1 -> skips /tmp itself
    # ! -name 'main.py'
    )

    #print(exit_code)
    #print(output.decode())
    
def run_with_input(container_id, script_path, n):
    proc = subprocess.run(
        ["docker", "exec", "-i", container_id, "python", script_path],
        input=json.dumps(n).encode(),
        capture_output=True,
        timeout=180 #3 Minutes as max subprocess runtime (avoids while true: consuming all server resources)
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode())
    output = json.loads(proc.stdout)
    return output["result"], output["elapsed"]

def get_initial_guess(name, n, time):
    n = np.asarray(n, dtype=float)
    time = np.asarray(time, dtype=float)

    if name == "constant":
        return [np.mean(time)]

    elif name == "logarithmic":
        safe_n = np.where(n <= 0, 1e-6, n)  #log(0) not defined 
        a, b = np.polyfit(np.log(safe_n), time, 1)
        return [a, b]

    elif name == "polynomial":
        return [1.0, 1.0, float(np.min(time))]

    elif name == "exponential":
        #Estimate via log-linearization: log(time - c) ≈ log(a) + b*n
        c0 = max(float(np.min(time)) - 1e-6, 0.0)
        shifted = np.where(time - c0 <= 0, 1e-9, time - c0)
        b0, log_a0 = np.polyfit(n, np.log(shifted), 1)
        return [float(np.exp(log_a0)), float(b0), c0]

#----Complexity Functiions----

def constant_progression(x,c):
    return c

def logarithmic_progression(x, a, b):
    return a * np.log(x) + b

def polynomial_progression(x, a, k, b):
    return a * (x ** k) + b

def exponential_progression(x, a, b, c):
    return a * np.exp(b * x) + c