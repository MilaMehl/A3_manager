"use client";

import { useEffect, useState } from "react";
import Layout from "../../components/Layout";
import Modal from "../../components/Modal";

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
  const [selectedRequest, setSelectedRequest] = useState<RequestItem | null>(
    null,
  );

  useEffect(() => {
    setTimeout(() => {
      setRequests([
        {
          id: 1,
          address: "Rua das Flores, 123",
          classification: "Buraco na via",
          date: "2024-06-15T08:30:00",
          status: "em andamento",
          photo_url: "https://via.placeholder.com/600x400?text=Buraco+na+Via",
        },
        {
          id: 2,
          address: "Av. Paulista, 1500",
          classification: "Iluminação",
          date: "2024-06-16T14:20:00",
          status: "pendente",
          photo_url: "https://via.placeholder.com/600x400?text=Poste+Queimado",
        },
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  return (
    <Layout>
      <div className="rounded-lg bg-white p-8 shadow-sm">
        <h2 className="mb-6 text-xl font-bold text-gray-800">
          Solicitações Registradas
        </h2>

        <table className="w-full text-left text-sm text-gray-600">
          <thead className="border-b border-t border-gray-200 bg-[#f8f9fc]">
            <tr>
              <th className="px-4 py-3 font-semibold text-gray-500">
                Endereço
              </th>
              <th className="px-4 py-3 font-semibold text-gray-500">
                Classificação
              </th>
              <th className="px-4 py-3 font-semibold text-gray-500">Status</th>
              <th className="px-4 py-3 font-semibold text-gray-500 text-center">
                Ação
              </th>
            </tr>
          </thead>
          <tbody>
            {requests.map((req) => (
              <tr key={req.id} className="border-b border-gray-100 bg-white">
                <td className="px-4 py-4">{req.address}</td>
                <td className="px-4 py-4">{req.classification}</td>
                <td className="px-4 py-4">{req.status}</td>
                <td className="px-4 py-4 text-center">
                  <button
                    onClick={() => setSelectedRequest(req)}
                    className="rounded-full bg-[#6c757d] px-4 py-1.5 text-xs font-semibold text-white hover:bg-gray-700"
                  >
                    Visualizar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

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
            </div>
          )}
        </Modal>
      </div>
    </Layout>
  );
}
