from dataclasses import dataclass

@dataclass
class TaskRequest():
    session_id: str
    code: str
    input_value: str
    input_type: str
    language: str
    number_data_points: int
    analyse_dynamically: bool
    analyse_statically: bool
    
@dataclass
class ExecutionAnalysisOutput():
    output: str
    complexity: str
    dynamic_data_points: list[list[int], list[float]]
    model_function: str
    certainty: str
    analysis_strength: str
    parameters: list[float]
    task_id: str
    session_id: str
    
    def __init__(self, session_id, task_id):
        print("Session ID:" + session_id + " Task ID: " + task_id)
        self.session_id = session_id
        self.task_id = task_id

    def setOutput(self, output, complexity, dynamic_data_points, model_function, certainty, analysis_strength, parameters):
        print(dynamic_data_points)
        self.output = output
        self.complexity = complexity
        self.dynamic_data_points = dynamic_data_points
        self.model_function = model_function
        self.certainty = certainty
        self.analysis_strength = analysis_strength
        self.parameters = parameters