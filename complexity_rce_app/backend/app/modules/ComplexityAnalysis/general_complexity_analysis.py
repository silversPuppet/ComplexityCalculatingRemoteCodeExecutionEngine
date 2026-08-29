import subprocess, json
import app.modules.ComplexityAnalysis.dynamic_analysis as dynamic_analysis

def analyse_full_complexity(container, code, input_value, input_type, analyse_dynamically, analyse_statically):
    try:
        #execute user code once to prove it works and further tests are possible 
        script_path="/tmp/main.py"
        print("executing User script")
        result, elapsed = dynamic_analysis.run_with_input(container.short_id, script_path, convert_input_value_to_type(input_value, input_type))
        
        output = result
        complexity = "N/A"
        dynamic_data_points = [(0,0)]
        estimated_function = "N/A"
        certainty = "0"
        analysis_strength = "extremely weak"
        
        dynamicComplexity = ""
        if(analyse_dynamically):
            dynamicComplexity, dynamic_data_points, dynamic_function = dynamic_analysis.calculate_dynamic_complexity(container, script_path, input_type)
            analysis_strength = "only dynamically"
            estimated_function = convert_dynamic_function_to_html(dynamic_function)
            
        if(analyse_statically):
            pass
        
        #combinedComplexity, strength = complexity_comparison()
        print(dynamicComplexity)
        complexity = dynamicComplexity
        
        return output, complexity, dynamic_data_points, estimated_function, certainty, analysis_strength
    except:
        raise 
        
def convert_dynamic_function_to_html(function):
    return "N/A"
    

def complexity_comparison():
    return

def map_complexity():
    return

def start_static_analyser(code, input, input_type):
    return 

def start_dynamic_analyser(container, input, input_type):
    return 

def convert_input_value_to_type(input_value, input_type):
    
    #TODO: Expand Type formatting and also format the output in execution.js
    
    match input_type:
        case "int":
            return int(input_value)
        case "str":
            return str(input_value)
        case _:
            return None


