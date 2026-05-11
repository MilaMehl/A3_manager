import { api } from "./api";

export const createRoute = async (
  grouping_ids: number[],
  lat: number,
  lng: number,
) => {
  const response = await api.post("/routes/", {
    grouping_ids,
    requester_lat: lat,
    requester_lng: lng,
  });
  return response.data;
};
