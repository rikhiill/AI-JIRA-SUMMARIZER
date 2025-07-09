// auth.js
export const saveToken = (token) => localStorage.setItem("token", token);
export const getToken = () => localStorage.getItem("token");
export const removeToken = () => localStorage.removeItem("token");

export const isAuthenticated = () => {
  return !!getToken(); // returns true if token exists
};
