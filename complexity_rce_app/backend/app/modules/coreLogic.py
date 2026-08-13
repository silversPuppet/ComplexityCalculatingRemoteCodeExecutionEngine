import docker
import tarfile 
import io
import app.modules.ComplexityAnalysis.general_complexity_analysis as general_complexity_analysis

class coreLogic:
    
    #client = docker.from_env()
    
    execute: dict[str, str] = {
        "code": "",
        "input": "",  
        "input_type": "",
        "language": "python",
    }
    
    result = {
            "output": "",
            "complexity": "",  
            "dynamic_data_points": [],
            "estimated_function": "",
            "certainty": "",
            "analysis_strength": "", #Whether or not static-analysis was able to be used
            "session_id": ""
    }
    
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
    
    def execute_and_analyse_userScript(self, user_execute):
        container = self.create_contrainer(user_execute)
        result = general_complexity_analysis.analyse(container, user_execute["code"], user_execute["input"], user_execute["input_type"])
        container.stop()
        container.remove()
        return result
    
    def create_contrainer(self, user_execute):
        match user_execute["language"]:
            case "python":
                self.create_python_container(self, user_execute)
                return
            case "c++":
                raise ValueError #maybe implement later?
            case _:
                raise ValueError
            
    def create_python_container(self, user_execute):
        container = self.client.containers.run(
            "python:3.11-slim",
            command="sleep infinity",   # keep it alive so you can exec into it
            detach=True
        )  
        # 1. Your script content, with whatever text block you want to inject
        python_input_output_block = self.user_code_modifiers["python"]
        script_content = user_execute["code"] + python_input_output_block
        
        #io:BytesIO() only accepts bytes ane tarinfo.size needs exact byte length
        script_bytes = script_content.encode("utf-8")
        
        #RAM stored tar archive
        tar_stream = io.BytesIO()
        with tarfile.open(fileobj=tar_stream, mode="w") as tar:
            tarinfo = tarfile.TarInfo(name="main.py")
            tarinfo.size = len(script_bytes)
            
        tar.addfile(tarinfo, tar_stream)
        
        return