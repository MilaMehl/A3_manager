import { api } from "./api";

export const getRequests = async (params = {}) => {
  const response = await api.get("/requests/", { params });
  return response.data;
};
