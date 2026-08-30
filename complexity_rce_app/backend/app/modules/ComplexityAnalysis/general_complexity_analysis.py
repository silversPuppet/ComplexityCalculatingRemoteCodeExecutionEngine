import subprocess, json
import app.modules.ComplexityAnalysis.dynamic_analysis as dynamic_analysis

def analyse_full_complexity(container, code, input_value, input_type, number_data_points, analyse_dynamically, analyse_statically):
    try:
        #execute user code once to prove it works and further tests are possible 
        script_path="/tmp/main.py"
        print("executing User script")
        result, elapsed = dynamic_analysis.run_with_input(container.short_id, script_path, convert_input_value_to_type(input_value, input_type))
        
        output = result
        complexity = "N/A"
        dynamic_data_points = [(0,0)]
        model_function = "N/A"
        certainty = "0"
        analysis_strength = "extremely weak"
        parameters = [0.0]
        
        dynamicComplexity = ""
        if(analyse_dynamically):
            dynamicComplexity, dynamic_data_points, parameters= dynamic_analysis.calculate_dynamic_complexity(container, script_path, input_type, number_data_points)
            analysis_strength = "only dynamically"
            model_function = dynamicComplexity
            print(model_function)
            
        if(analyse_statically):
            pass
        
        #combinedComplexity, strength = complexity_comparison()
        complexity = dynamicComplexity
        
        return output, complexity, dynamic_data_points, model_function, certainty, analysis_strength, parameters
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

def convert_input_value_to_type(input_value: str, input_type: str):
    
    #TODO: Expand Type formatting and also format the output in execution.js
    
    match input_type:
        case "int":
            return int(input_value)
        case "str":
            return str(input_value)
        case "float":
            return float(input_value)
        case "int[]":
            filter_characters = "[] ()"
            translation_table = str.maketrans("", "",  filter_characters)
            clean_text = input_value.translate(translation_table)
            number_list = clean_text.split(",")
            
            converted_list = []
            for number in number_list:
                converted_list.append(int(number))
            return converted_list
        case _:
            raise TypeError("Input Type: " + input_type + " not supported!")


