from general_complexity_analysis import run_with_input
import scipy
import math 
import docker
import subprocess, json

client = docker.from_env()

def calculate_dynamic_complexity(container, script_path, input_type):
    n, time = execute_script_with_autogenerate_data(container.short_id, script_path, input_type)
    
    #Compaaring models with Residual Sum of Squares 
    
    for name, model_func, k in [
        ("constant",  )
    ]:
        params, covariance = scipy.curve_fit(model_func, n, time)
        y_predicted = [model_func(ni, *params) for ni in n]
        rss = sum((ti - yi) ** 2 for ti, yi in zip(time, y_predicted))
    
    return dynamicComplexity, dynamic_data_points, estimated_function

def execute_script_with_autogenerate_data(container_id, script_path, input_type):
    return n, time 

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