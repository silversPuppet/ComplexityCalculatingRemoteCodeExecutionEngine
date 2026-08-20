from dataclasses import dataclass
import array

@dataclass
class TaskRequest():
    session_id: str
    code: str
    input: str
    input_type: str
    language: str
    
@dataclass
class ExecutionAnalysisOutput():
    output: str
    complexity: str
    dynamic_data_points: array 
    estimated_function: str
    certainty: str
    analysis_strength: str
    task_id: str
    session_id: str
    
    def __init__(self, session_id, task_id):
        print("Session ID:" + session_id + " Task ID: " + task_id)
        self.session_id = session_id
        self.task_id = task_id

    def setOutput(self, output, complexity, dynamic_data_points, estimated_function, certainty, analysis_strength):
        self.output = output
        self.complexity = complexity
        self.dynamic_data_points = dynamic_data_points
        self.estimated_function = estimated_function
        self.certainty = certainty
        self.analysis_strength = analysis_strength