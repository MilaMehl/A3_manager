"use client";

import { useEffect, useState, FormEvent } from "react";
import Layout from "../../components/Layout";
import Modal from "../../components/Modal";
import { getRequests, createRequest } from "../../services/requests";

interface RequestItem {
  id: number;
  address: string;
  classification: string;
  date: string;
  status: string;
  photo_url?: string;
}

export default function Solicitacoes() {
  const [requests, setRequests] = useState<RequestItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [limit, setLimit] = useState(10);
  const [page, setPage] = useState(1);
  const [selectedRequest, setSelectedRequest] = useState<RequestItem | null>(
    null,
  );
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [newAddress, setNewAddress] = useState("");
  const [newClassification, setNewClassification] = useState("");

  const fetchRequests = async () => {
    setLoading(true);
    try {
      const res = await getRequests({ search: searchTerm, limit, page });
      setRequests(res.data || []);
    } catch (error) {
      setRequests([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRequests();
  }, [searchTerm, limit, page]);

  const handleCreate = async (e: FormEvent) => {
    e.preventDefault();
    try {
      await createRequest({
        address: newAddress,
        classification: newClassification,
      });
      setIsCreateModalOpen(false);
      setNewAddress("");
      setNewClassification("");
      fetchRequests();
    } catch (error) {
      alert("Erro ao registrar solicitação");
    }
  };

  const formatDate = (isoString: string) => {
    try {
      const date = new Date(isoString);
      return date.toLocaleDateString("pt-BR", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    } catch {
      return isoString;
    }
  };

  return (
    <Layout>
      <div className="rounded-lg bg-white p-8 shadow-sm">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="text-xl font-bold text-gray-800">
            Solicitações Registradas
          </h2>
          <button
            onClick={() => setIsCreateModalOpen(true)}
            className="rounded-md bg-[#00a2ff] px-6 py-2 font-semibold text-white transition-colors hover:bg-blue-600 shadow-sm"
          >
            Nova Solicitação
          </button>
        </div>

        <div className="mb-4 flex items-center justify-between text-sm text-gray-500">
          <div className="flex items-center space-x-2">
            <span>Show</span>
            <select
              value={limit}
              onChange={(e) => setLimit(Number(e.target.value))}
              className="rounded-md border border-gray-300 p-1 outline-none focus:border-[#00a2ff] focus:ring-1 focus:ring-[#00a2ff]"
            >
              <option value={10}>10</option>
              <option value={25}>25</option>
              <option value={50}>50</option>
            </select>
            <span>entries</span>
          </div>
          <div className="flex items-center space-x-2">
            <span>Search:</span>
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="rounded-md border border-gray-300 p-1 outline-none focus:border-[#00a2ff] focus:ring-1 focus:ring-[#00a2ff]"
            />
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-gray-600">
            <thead className="border-b border-t border-gray-200 bg-[#f8f9fc]">
              <tr>
                <th className="px-4 py-3 font-semibold text-gray-500">
                  Endereço
                </th>
                <th className="px-4 py-3 font-semibold text-gray-500">
                  Classificação
                </th>
                <th className="px-4 py-3 font-semibold text-gray-500">Data</th>
                <th className="px-4 py-3 font-semibold text-gray-500">
                  Status
                </th>
                <th className="px-4 py-3 font-semibold text-gray-500 text-center">
                  Ação
                </th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan={5} className="py-8 text-center text-gray-500">
                    Buscando dados...
                  </td>
                </tr>
              ) : requests.length === 0 ? (
                <tr>
                  <td colSpan={5} className="py-8 text-center text-gray-500">
                    Nenhuma solicitação encontrada.
                  </td>
                </tr>
              ) : (
                requests.map((req) => (
                  <tr
                    key={req.id}
                    className="border-b border-gray-100 bg-white hover:bg-gray-50"
                  >
                    <td className="px-4 py-4">{req.address}</td>
                    <td className="px-4 py-4">{req.classification}</td>
                    <td className="px-4 py-4">{formatDate(req.date)}</td>
                    <td className="px-4 py-4">
                      <span
                        className={`rounded-full px-2 py-1 text-xs font-semibold ${
                          req.status === "concluído"
                            ? "bg-green-100 text-green-700"
                            : req.status === "em andamento"
                              ? "bg-blue-100 text-blue-700"
                              : "bg-yellow-100 text-yellow-700"
                        }`}
                      >
                        {req.status}
                      </span>
                    </td>
                    <td className="px-4 py-4 text-center">
                      <button
                        onClick={() => setSelectedRequest(req)}
                        className="rounded-full bg-[#6c757d] px-4 py-1.5 text-xs font-semibold text-white hover:bg-gray-700"
                      >
                        Visualizar
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        <div className="mt-6 flex items-center justify-end space-x-2 text-sm">
          <button
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            className="px-3 py-1 text-gray-400 hover:text-gray-800 transition-colors disabled:opacity-50"
            disabled={page === 1}
          >
            Previous
          </button>
          <button className="rounded bg-gray-200 px-3 py-1 font-semibold text-gray-700">
            {page}
          </button>
          <button
            onClick={() => setPage((p) => p + 1)}
            className="px-3 py-1 text-gray-400 hover:text-gray-800 transition-colors"
          >
            Next
          </button>
        </div>

        <Modal
          isOpen={!!selectedRequest}
          onClose={() => setSelectedRequest(null)}
          title="Detalhes da Solicitação"
        >
          {selectedRequest && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="block font-bold text-gray-500 uppercase text-[10px]">
                    Endereço
                  </span>
                  <p className="text-gray-800">{selectedRequest.address}</p>
                </div>
                <div>
                  <span className="block font-bold text-gray-500 uppercase text-[10px]">
                    Status
                  </span>
                  <p className="text-gray-800 capitalize">
                    {selectedRequest.status}
                  </p>
                </div>
              </div>
              {selectedRequest.photo_url && (
                <div>
                  <span className="block font-bold text-gray-500 uppercase text-[10px] mb-2">
                    Evidência
                  </span>
                  <img
                    src={selectedRequest.photo_url}
                    alt="Ocorrência"
                    className="w-full rounded-lg border border-gray-200"
                  />
                </div>
              )}
            </div>
          )}
        </Modal>

        <Modal
          isOpen={isCreateModalOpen}
          onClose={() => setIsCreateModalOpen(false)}
          title="Registrar Solicitação"
        >
          <form onSubmit={handleCreate} className="space-y-4">
            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">
                Endereço Completo
              </label>
              <input
                type="text"
                value={newAddress}
                onChange={(e) => setNewAddress(e.target.value)}
                className="w-full rounded-md border border-gray-300 p-2 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                required
              />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">
                Classificação (Problema)
              </label>
              <input
                type="text"
                value={newClassification}
                onChange={(e) => setNewClassification(e.target.value)}
                placeholder="Ex: Buraco na via, Iluminação..."
                className="w-full rounded-md border border-gray-300 p-2 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                required
              />
            </div>
            <div className="pt-4">
              <button
                type="submit"
                className="w-full rounded-md bg-[#00a2ff] py-2 font-semibold text-white hover:bg-blue-600"
              >
                Registrar
              </button>
            </div>
          </form>
        </Modal>
      </div>
    </Layout>
  );
}
