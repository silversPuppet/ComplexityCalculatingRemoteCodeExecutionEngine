import subprocess, json
import app.modules.ComplexityAnalysis.dynamic_analysis as dynamic_analysis
import complexity_rce_app.backend.app.modules.ComplexityAnalysis.static_analysis as static_analysis

def analyse_full_complexity(container, code, input_value, input_type, number_data_points, analyse_dynamically, analyse_statically, language):
    try:
        #execute user code once to prove it works and further tests are possible 
        script_path="/tmp/main.py"
        print("executing User script")
        result, elapsed = dynamic_analysis.run_with_input(container.short_id, script_path, convert_input_value_to_type(input_value, input_type))
        
        output = result
        complexity = "N/A"
        dynamic_data_points = [(0,0)]
        model_function = "N/A"
        certainty = "N/A"
        analysis_strength = "None"
        parameters = [0.0]
        
        dynamicComplexity = ""
        if(analyse_dynamically):
            dynamicComplexity, dynamic_data_points, parameters= dynamic_analysis.calculate_dynamic_complexity(container, script_path, input_type, number_data_points)
            analysis_strength = "only dynamically"
            model_function = dynamicComplexity
            complexity = dynamicComplexity
            
        if(analyse_statically):
            staticComplexity, static_degree = static_analysis.calculate_static_complexity(code, language)
            if(dynamicComplexity != ""):
                complexity, certainty = complexity_comparison(dynamicComplexity, staticComplexity, static_degree)
                analysis_strength = "dynamically and statically"
            else:
                complexity = staticComplexity
                analysis_strength = "only statically"
        
        
        return output, complexity, dynamic_data_points, model_function, certainty, analysis_strength, parameters
    except:
        raise 

COMPLEXITY_ORDER = ["constant", "logarithmic", "polynomial", "exponential"]
        
def complexity_comparison(dynamic, static, static_degree):
    if static != "unkown":
        distance = abs(COMPLEXITY_ORDER.index(dynamic) - COMPLEXITY_ORDER.index(static))
        print(distance)
        if distance == 0:
            return dynamic, "100"
        if distance == 1:
            #Difference between any polynomial function and exponential function is a lot more significant 
            if dynamic == "exponential" or static == "exponential":
                return dynamic + " / " + static, "30"
            return dynamic + " / " + static, "70"
        if distance >= 2:
            return dynamic + " / " + static, str(50 // distance)
    else:
        return dynamic, "25"


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


