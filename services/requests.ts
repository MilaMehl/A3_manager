import { api } from "./api";

export const getRequests = async (params = {}) => {
  const response = await api.get("/requests/", { params });
  return response.data;
};

export const createRequest = async (data: {
  address: string;
  classification: string;
}) => {
  const response = await api.post("/requests/", data);
  return response.data;
};
