from general_complexity_analysis import run_with_input
import scipy
import math 
import docker
import subprocess, json
import random

client = docker.from_env()

def calculate_dynamic_complexity(container, script_path, input_type):
    try:
        n, time = execute_script_with_autogenerate_data(container, script_path, input_type)
    except:
        raise
    
    #Compaaring models with Residual Sum of Squares 
    predictions = {}
    for name, model_func, k in [
        #k = number of model parameters -> used for aic
        ("constant",  constant_progression, 1),
        ("logarithmic",  logarithmic_progression, 2),
        ("polynomial",  polynomial_progression, 3),
         ("exponential",  exponential_progression, 3)
    ]:
        params, covariance = scipy.curve_fit(model_func, n, time)
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
    
    dynamicComplexity = convertToBigO(best_model, [best_model]["params"])
    dynamic_data_points = (n, time)
    estimated_function = (best_model, predictions[best_model]["params"])
    
    return dynamicComplexity, dynamic_data_points, estimated_function

def convertToBigO():
    return

def execute_script_with_autogenerate_data(container, script_path, input_type):
    
    return n, time 

def fullRun(values, container_id, script_path):
    random.shuffle(values)
    inputs = []
    times = []
    for n in values:
        result, duration = medianRunScript(n, container_id)
        inputs.append(n)
        times.append(duration)
        
def medianRunScript(n, container, script_path):
    values = []
    for i in range(3):
        reset_environment(container)
        output, duration = run_with_input(container.short_id, script_path, n)
        values.append(duration, values)
    
    print(values)
    return sorted(values, key=lambda tupple: tupple[0])[1]
        

def reset_environment(container):
    exit_code, output = container.exec_run(
    ["sh", "-c", "find /tmp -mindepth 1 ! -name 'main.py' -delete"]
    #sh -c runs a shell command 
    #-mindepth 1 -> skips /tmp itself
    # ! -name 'main.py'
    )

    print(exit_code)
    print(output.decode())


#----Complexity Functiions----

def constant_progression(c):
    return c

def logarithmic_progression(n, a, b):
    return a * math.log(n) + b

def polynomial_progression(n, a, k, b):
    return a * (n ** k) + b

def exponential_progression(n, a, b, c):
    return a * math.exp(b * n) + c