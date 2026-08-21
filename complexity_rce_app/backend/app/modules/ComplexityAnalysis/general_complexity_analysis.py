import subprocess, json


def analyse_full_complexity(container, code, input_value, input_type):
    try:
        #execute user code once to prove it works and further tests are possible 
        print("executing User script")
        result, elapsed = run_with_input(container.short_id, "/tmp/main.py", input_value)
        
            #Later try analyse the code
            #temporary value assignment 
        output = result
        complexity = "O(0)"
        dynamic_data_points = [(0,0)]
        estimated_function = "14"
        certainty = "100"
        analysis_strength = "strong"
    except:
        raise Exception("User script failed to execute.")
        
    return output, complexity, dynamic_data_points, estimated_function, certainty, analysis_strength

def complexity_comparison():
    return

def map_complexity():
    return

def start_static_analyser(code, input, input_type):
    return 

def start_dynamic_analyser(container, input, input_type):
    return 

def run_with_input(container_id, script_path, n):
    proc = subprocess.run(
        ["docker", "exec", "-i", container_id, "python", script_path],
        input=json.dumps(n).encode(),
        capture_output=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode())
    output = json.loads(proc.stdout)
    return output["result"], output["elapsed"]
