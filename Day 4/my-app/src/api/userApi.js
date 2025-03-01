import axios from "axios";
const API_URL = "http://localhost:4000/api/users";
export const getUsers = async (token) => {
 return axios.get(API_URL, {
 headers: { Authorization: `Bearer ${token}`  }
 });
};