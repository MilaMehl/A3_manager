import { api } from "./api";

export const getGroupings = async (params = {}) => {
  const response = await api.get("/groupings/", { params });
  return response.data;
};
