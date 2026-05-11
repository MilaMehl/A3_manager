"use client";

import { useEffect, useState } from "react";
import Layout from "../../components/Layout";
import { getGroupings } from "../../services/groupings";
import { createRoute } from "../../services/routes";

interface Grouping {
  id: number;
  classification: string;
  status: string;
}

export default function Roteirizacao() {
  const [groupings, setGroupings] = useState<Grouping[]>([]);
  const [selectedIds, setSelectedIds] = useState<number[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await getGroupings();
        setGroupings(res.data || []);
      } catch (error) {
        setGroupings([
          { id: 1, classification: "Jardinagem", status: "ativo" },
          { id: 2, classification: "Zeladoria", status: "ativo" },
          { id: 3, classification: "Iluminação", status: "ativo" },
        ]);
      }
    };
    load();
  }, []);

  const toggleSelection = (id: number) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((i) => i !== id) : [...prev, id],
    );
  };

  const handleGenerateRoute = () => {
    if (selectedIds.length === 0) return;

    setLoading(true);
    navigator.geolocation.getCurrentPosition(
      async (position) => {
        try {
          const { latitude, longitude } = position.coords;
          const data = await createRoute(selectedIds, latitude, longitude);
          window.open(data.google_maps_url, "_blank");
        } catch (error) {
          alert("Erro ao gerar rota.");
        } finally {
          setLoading(false);
        }
      },
      () => {
        alert("Permissão de GPS negada.");
        setLoading(false);
      },
    );
  };

  return (
    <Layout>
      <div className="rounded-lg bg-white p-8 shadow-sm">
        <h2 className="mb-6 text-xl font-bold text-gray-800">
          Traçar Rota de Atendimento
        </h2>

        <p className="mb-6 text-sm text-gray-600">
          Selecione as equipes abaixo e clique em gerar para calcular a melhor
          rota partindo da sua localização atual.
        </p>

        <div className="space-y-3">
          {groupings.map((group) => (
            <label
              key={group.id}
              className={`flex cursor-pointer items-center justify-between rounded-md border p-4 transition-all ${
                selectedIds.includes(group.id)
                  ? "border-[#00a2ff] bg-[#eaf6ff]"
                  : "border-gray-200 bg-white hover:border-gray-300"
              }`}
            >
              <div className="flex items-center">
                <input
                  type="checkbox"
                  checked={selectedIds.includes(group.id)}
                  onChange={() => toggleSelection(group.id)}
                  className="h-5 w-5 rounded border-gray-300 text-[#00a2ff] focus:ring-[#00a2ff]"
                />
                <div className="ml-4">
                  <span className="block font-bold text-gray-800">
                    Equipe {group.id}
                  </span>
                  <span className="text-xs text-gray-500 uppercase tracking-wider">
                    {group.classification}
                  </span>
                </div>
              </div>
              <span className="text-xs font-semibold text-green-600">
                {group.status}
              </span>
            </label>
          ))}
        </div>

        <button
          onClick={handleGenerateRoute}
          disabled={loading || selectedIds.length === 0}
          className={`mt-8 w-full rounded-md py-3 font-bold text-white shadow-md transition-all ${
            selectedIds.length > 0 && !loading
              ? "bg-[#00a2ff] hover:bg-blue-600"
              : "cursor-not-allowed bg-gray-300"
          }`}
        >
          {loading
            ? "Processando Localização..."
            : `Gerar Rota para ${selectedIds.length} Equipes`}
        </button>
      </div>
    </Layout>
  );
}
