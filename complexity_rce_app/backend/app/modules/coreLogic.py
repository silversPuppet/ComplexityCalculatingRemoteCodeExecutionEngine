import docker
from docker.types import Ulimit
from docker.errors import APIError, ImageNotFound
import tarfile 
import io
import time
import app.modules.ComplexityAnalysis.general_complexity_analysis as general_complexity_analysis
import app.modules.comunicationClasses as communicationClasses
import base64

client = docker.from_env()
print("Is Docker Connected: " + str(client.ping()))  

user_code_modifiers = {"python":  
'''\n
import sys, time, json
if __name__ == "__main__":
    n = json.load(sys.stdin)

    # actual timed run
    t_start = time.perf_counter()
    result = main(n)
    t_end = time.perf_counter()
    elapsed = t_end - t_start

    print(json.dumps({
        "result": result,
        "elapsed": elapsed
}))'''}

def execute_and_analyse_userScript(user_execute: communicationClasses.TaskRequest, session_id, task_id):
    try:
        print("Creating Container")
        container = create_contrainer(user_execute)
        result = communicationClasses.ExecutionAnalysisOutput(session_id, task_id)
        print("starting complexity analysis")
        output, complexity, dynamic_data_points, estimated_function, certainty, analysis_strength = general_complexity_analysis.analyse_full_complexity(
            container, 
            user_execute.code, 
            user_execute.input, 
            user_execute.input_type,
        )
        result.setOutput(output, complexity, dynamic_data_points, estimated_function, certainty, analysis_strength)
        container.stop()
        container.remove()
        return result
    except Exception as e:
        container.stop()
        container.remove()
        raise e

def create_contrainer(user_execute):
    match user_execute.language:
        case "python":
            container = create_python_container(user_execute)
            return container 
        case "c++":
            raise ValueError #maybe implement later?
        case _:
            raise ValueError
        
def create_python_container(user_execute: communicationClasses.TaskRequest):
    print("creating container with python.")    
    try:
        
        container = client.containers.run(
        "python:3.11-slim",
        command="sleep infinity",   
        detach=True,
        #TODO: Uhh Figure out how to use runsc for better isolation
        network_mode="none",
        mem_limit= "128m", #megabites
        memswap_limit= "128m",
        
        cpu_quota=50000, #50ms 
        cpu_period=100000, #100ms  #TODO: Verify these are reasonable cpu constraints (numbers taken from internet)
        
        read_only=True, 
        tmpfs={"/tmp": "size=32m,exec,mode=1777"}, #read-only root folder + limited writable space 
        
        cap_drop=["ALL"], #No Kernel capabilities
        security_opt=["no-new-privileges:true"],
    )  
        
        python_input_output_block = user_code_modifiers["python"]
        script_content = user_execute.code + python_input_output_block
        
        encoded_script = base64.b64encode(script_content.encode("utf-8")).decode("utf-8")
        
        #Using a shell command to create the file since tarfile would need write permissions which we cant give because of possible security issues 
        write_command = [
        "sh", "-c",
        f"echo '{encoded_script}' | base64 -d > /tmp/main.py"
        ]
            
        container.exec_run(write_command)
        #Why write command possible if read_only=true ? readonly applies only to the root file system -> sub-directory /tmp allows file writing 

        print("Finished creating and filling container.")
        return container 
    except APIError as e:
        container.stop()
        #TODO: Handle Error Raising behaviour and passing it to the user? 
        raise Exception("API Error when trying to initialise Docker container." + e)
    
    