import axios from 'axios'

//const baseUrl = 'http://localhost:8000/' //testing with npm run dev
const baseUrl = 'https://backend:8000' //Docker Container 

const api = axios.create({
  baseURL: baseUrl,
  withCredentials: true,  // This sends/receives cookies
});

const get_new_session_id = async () => {
  try {
    const response = await api.get('/get-session-id/')
    return response.data.session_id
  } catch (error) {
    console.error("Error fetching session ID:", error)
    throw error
  }
}
 
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

                                        //interval in seconds -> 5min max
const get_task_status = async (task_id, session_id, { interval = 7000, maxAttempts = 60 } = {}) => {
  for(let attempt = 0; attempt < maxAttempts; attempt++) {
    console.log(`Getting Task Status ${task_id}`)
    const response = await api.get(`${baseUrl}task-status/${task_id}`, {
      params: {session_id}
    })

    if(response.data.status === "completed") {
      return response.data
    }
    if(response.data.status === "failed") {
      return response.data
    }
    await sleep(interval)
  }
  throw new Error(`Task ${task_id} timed out after ${maxAttempts} attempts`)
};

const start_execute_analysis_task = async (session_id, code, input_value, input_type, language,number_data_points, analyse_dynamically, analyse_statically) => {
  try{
    //TODO: Input validation!!!
    console.log(input_value)

    const response = await api.post('/start-execute-analysis-task/', {
      session_id,
      code, 
      input_value,
      input_type,
      language,
      number_data_points,
      analyse_dynamically,
      analyse_statically
    })
    return response.data
  }catch (error){
    console.error("Error starting a new code execution/analysis task:", error)
    throw error
  }
}

export default{get_new_session_id, start_execute_analysis_task, get_task_status}