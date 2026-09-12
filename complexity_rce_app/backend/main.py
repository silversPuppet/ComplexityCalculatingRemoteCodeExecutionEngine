import uvicorn
import backend.app.modules.ComplexityAnalysis.static_analysis as staticAnalysis
#This file is used to launch the backend for local development 

if __name__ == "__main__":
    uvicorn.run("backend.app.api:app", host="0.0.0.0", port=8000, reload=True)
    #For manual testing only run: staticAnalysis.calculate_static_complexity()