import axios from 'axios'

const baseUrl = 'http://127.0.0.1:8000/'

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

const start_execute_analysis_task = async (session_id, code, input, input_type, language) => {
  try{
    const response = await api.post('/start-execute-analysis-task/', {
      session_id,
      code, input,
      input_type,
      language
    })
    return response.data
  }catch (error){
    console.error("Error starting a new code execution/analysis task:", error)
    throw error
  }
}

export default{get_new_session_id, start_execute_analysis_task}