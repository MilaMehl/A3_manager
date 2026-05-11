"use client";

import { useEffect, useState } from "react";
import Layout from "../../components/Layout";
import Modal from "../../components/Modal";

interface Grouping {
  id: number;
  classification: string;
  status: string;
}

export default function Equipes() {
  const [groupings, setGroupings] = useState<Grouping[]>([]);
  const [selectedGroup, setSelectedGroup] = useState<Grouping | null>(null);

  useEffect(() => {
    setGroupings([
      { id: 1, classification: "Jardinagem", status: "bloqueado" },
      { id: 2, classification: "Daniel Teste", status: "ativo" },
    ]);
  }, []);

  return (
    <Layout>
      <div className="rounded-lg bg-white p-8 shadow-sm">
        <h2 className="mb-6 text-xl font-bold text-gray-800">
          Equipes de atendimento:
        </h2>

        <table className="w-full text-left text-sm text-gray-600">
          <thead className="border-b border-t border-gray-200 bg-[#f8f9fc]">
            <tr>
              <th className="px-4 py-3 font-semibold text-gray-500">ID</th>
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
            {groupings.map((group) => (
              <tr key={group.id} className="border-b border-gray-100 bg-white">
                <td className="px-4 py-4">{group.id}</td>
                <td className="px-4 py-4">{group.classification}</td>
                <td className="px-4 py-4">{group.status}</td>
                <td className="px-4 py-4 text-center">
                  <button
                    onClick={() => setSelectedGroup(group)}
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
          isOpen={!!selectedGroup}
          onClose={() => setSelectedGroup(null)}
          title="Informações da Equipe"
        >
          {selectedGroup && (
            <div className="space-y-4">
              <div className="flex items-center space-x-4">
                <div className="h-12 w-12 rounded bg-[#0f3460] flex items-center justify-center font-bold text-white">
                  EQ
                </div>
                <div>
                  <h4 className="font-bold text-gray-800">
                    Equipe {selectedGroup.id}
                  </h4>
                  <p className="text-sm text-gray-500">
                    {selectedGroup.classification}
                  </p>
                </div>
              </div>
              <div className="rounded-md bg-gray-50 p-4">
                <p className="text-sm text-gray-600">
                  Status atual do agrupamento:{" "}
                  <span className="font-bold text-[#00a2ff]">
                    {selectedGroup.status}
                  </span>
                </p>
              </div>
            </div>
          )}
        </Modal>
      </div>
    </Layout>
  );
}
