import docker
from docker.types import Ulimit
import tarfile 
import io
import app.modules.ComplexityAnalysis.general_complexity_analysis as general_complexity_analysis
import app.modules.comunicationClasses as communicationClasses

client = docker.from_env()

user_code_modifiers = {"python":  
'''import sys, time, json
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
    container = create_contrainer(user_execute)
    result = communicationClasses.ExecutionAnalysisOutput(session_id, task_id)
    result.setOutput(general_complexity_analysis.analysse_full_complexity(
        container, 
        user_execute.code, 
        user_execute.input, 
        user_execute.input_type,
        ))
    container.stop()
    container.remove()
    return result

def create_contrainer(user_execute):
    match user_execute["language"]:
        case "python":
            create_python_container(user_execute)
            return
        case "c++":
            raise ValueError #maybe implement later?
        case _:
            raise ValueError
        
def create_python_container(user_execute: communicationClasses.TaskRequest):
    print("creating container with python.")
    container = client.containers.run(
        "python:3.11-slim",
        command="sleep infinity",   
        detach=True,
        runtime="runsc", #gvisor for better isolation
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
    
    #io:BytesIO() only accepts bytes ane tarinfo.size needs exact byte length
    script_bytes = script_content.encode("utf-8")
    
    #RAM stored tar archive
    tar_stream = io.BytesIO()
    with tarfile.open(fileobj=tar_stream, mode="w") as tar:
        tarinfo = tarfile.TarInfo(name="main.py")
        tarinfo.size = len(script_bytes)
        
    tar.addfile(tarinfo, tar_stream)
    
    return