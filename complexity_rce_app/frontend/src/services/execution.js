import axios from 'axios'

const baseUrl = 'http://127.0.0.1:8000/'

const api = axios.create({
  baseURL: baseUrl,
  withCredentials: true,  // This sends/receives cookies
});

const get_new_session_id = async () => {
  try {
    const request = api.get('/get-session-id/')
    return request.then(respons => respons.data.session_id)
  } catch (error) {
    console.error("Error fetching session ID:", error)
    throw error
  }
}

export default{get_new_session_id}