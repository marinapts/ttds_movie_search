import axios from 'axios'

export default axios.create({
  baseURL: 'http://167.71.139.222/',
  responseType: 'json'
})
