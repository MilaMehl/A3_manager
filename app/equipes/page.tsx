"use client";

import { useEffect, useState, FormEvent } from "react";
import Layout from "../../components/Layout";
import Modal from "../../components/Modal";
import { getGroupings, createGrouping } from "../../services/groupings";

interface Grouping {
  id: number;
  classification: string;
  status: string;
}

export default function Equipes() {
  const [groupings, setGroupings] = useState<Grouping[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [limit, setLimit] = useState(10);
  const [page, setPage] = useState(1);
  const [selectedGroup, setSelectedGroup] = useState<Grouping | null>(null);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [newClassification, setNewClassification] = useState("");
  const [newStatus, setNewStatus] = useState("ativo");

  const fetchGroupings = async () => {
    setLoading(true);
    try {
      const res = await getGroupings({ search: searchTerm, limit, page });
      setGroupings(res.data || []);
    } catch (error) {
      setGroupings([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGroupings();
  }, [searchTerm, limit, page]);

  const handleCreate = async (e: FormEvent) => {
    e.preventDefault();
    try {
      await createGrouping({
        classification: newClassification,
        status: newStatus,
      });
      setIsCreateModalOpen(false);
      setNewClassification("");
      setNewStatus("ativo");
      fetchGroupings();
    } catch (error) {
      alert("Erro ao cadastrar equipe");
    }
  };

  return (
    <Layout>
      <div className="rounded-lg bg-white p-8 shadow-sm">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="text-xl font-bold text-gray-800">
            Equipes de atendimento:
          </h2>
          <button
            onClick={() => setIsCreateModalOpen(true)}
            className="rounded-md bg-[#00a2ff] px-6 py-2 font-semibold text-white transition-colors hover:bg-blue-600 shadow-sm"
          >
            Cadastrar
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
                <th className="px-4 py-3 font-semibold text-gray-500">ID</th>
                <th className="px-4 py-3 font-semibold text-gray-500">
                  Classificação
                </th>
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
                  <td colSpan={4} className="py-8 text-center text-gray-500">
                    Buscando dados...
                  </td>
                </tr>
              ) : groupings.length === 0 ? (
                <tr>
                  <td colSpan={4} className="py-8 text-center text-gray-500">
                    Nenhum registro encontrado.
                  </td>
                </tr>
              ) : (
                groupings.map((group) => (
                  <tr
                    key={group.id}
                    className="border-b border-gray-100 bg-white hover:bg-gray-50"
                  >
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

        <Modal
          isOpen={isCreateModalOpen}
          onClose={() => setIsCreateModalOpen(false)}
          title="Cadastrar Nova Equipe"
        >
          <form onSubmit={handleCreate} className="space-y-4">
            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">
                Classificação
              </label>
              <input
                type="text"
                value={newClassification}
                onChange={(e) => setNewClassification(e.target.value)}
                className="w-full rounded-md border border-gray-300 p-2 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                required
              />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">
                Status
              </label>
              <select
                value={newStatus}
                onChange={(e) => setNewStatus(e.target.value)}
                className="w-full rounded-md border border-gray-300 p-2 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
              >
                <option value="ativo">Ativo</option>
                <option value="bloqueado">Bloqueado</option>
              </select>
            </div>
            <div className="pt-4">
              <button
                type="submit"
                className="w-full rounded-md bg-[#00a2ff] py-2 font-semibold text-white hover:bg-blue-600"
              >
                Salvar Equipe
              </button>
            </div>
          </form>
        </Modal>
      </div>
    </Layout>
  );
}
