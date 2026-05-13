import { api } from "./api";

export const getGroupings = async (params = {}) => {
  const response = await api.get("/groupings/", { params });
  return response.data;
};

export const createGrouping = async (data: {
  classification: string;
  status: string;
}) => {
  const response = await api.post("/groupings/", data);
  return response.data;
};
