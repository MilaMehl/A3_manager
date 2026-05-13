"use client";

import { useEffect, useState } from "react";
import Layout from "../../components/Layout";

interface Item {
  id: number;
  classification: string;
  address?: string;
  total_requests?: number;
}

export default function Roteirizacao() {
  const [viewMode, setViewMode] = useState<"individuais" | "agrupamentos">(
    "individuais",
  );
  const [itens, setItens] = useState<Item[]>([]);
  const [selectedIds, setSelectedIds] = useState<number[]>([]);
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState("");
  const [rotaResult, setRotaResult] = useState<any>(null);

  // Busca os dados (Solicitações ou Agrupamentos) dependendo da aba
  const loadData = async () => {
    const token = localStorage.getItem("token");
    if (!token) return;

    setErro("");
    setItens([]);
    setSelectedIds([]);

    try {
      const endpoint =
        viewMode === "individuais" ? "/api/requests/" : "/api/groupings/";
      const res = await fetch(`http://localhost:5000${endpoint}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      if (res.ok) {
        setItens(data.data.slice(0, 10)); // Pega os 10 primeiros pra teste
      }
    } catch (error) {
      setErro("Erro ao carregar dados do servidor.");
    }
  };

  useEffect(() => {
    loadData();
    setRotaResult(null);
  }, [viewMode]);

  const toggleSelection = (id: number) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((i) => i !== id) : [...prev, id],
    );
  };

  const handleGenerateRoute = () => {
    if (selectedIds.length === 0) return;
    setLoading(true);
    setErro("");

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const token = localStorage.getItem("token");
        // Escolhe o endpoint correto baseado no que o usuário selecionou
        const endpoint =
          viewMode === "individuais" ? "/api/routes/" : "/api/grouping-routes/";
        // Escolhe o nome da chave do body (request_ids ou grouping_ids)
        const bodyKey =
          viewMode === "individuais" ? "request_ids" : "grouping_ids";

        try {
          const response = await fetch(`http://localhost:5000${endpoint}`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
              latitude: position.coords.latitude,
              longitude: position.coords.longitude,
              [bodyKey]: selectedIds,
            }),
          });

          const data = await response.json();
          if (response.ok) {
            setRotaResult(data);
            window.open(data.google_maps_url, "_blank");
          } else {
            setErro(
              "Erro ao calcular rota: " + (data.error || "Verifique os dados."),
            );
          }
        } catch (err) {
          setErro("Erro de conexão com o backend.");
        } finally {
          setLoading(false);
        }
      },
      () => {
        alert("GPS negado. Tente habilitar a localização.");
        setLoading(false);
      },
    );
  };

  return (
    <Layout>
      <div className="rounded-lg bg-white p-8 shadow-sm">
        <h2 className="mb-2 text-xl font-bold text-gray-800">
          Traçar Rota de Atendimento
        </h2>

        {/* Seletor de Modo (Abas) */}
        <div className="mb-6 flex gap-4 border-b pb-4">
          <button
            onClick={() => setViewMode("individuais")}
            className={`pb-2 text-sm font-bold transition-all ${viewMode === "individuais" ? "border-b-2 border-[#00a2ff] text-[#00a2ff]" : "text-gray-400"}`}
          >
            Pedidos Individuais
          </button>
          <button
            onClick={() => setViewMode("agrupamentos")}
            className={`pb-2 text-sm font-bold transition-all ${viewMode === "agrupamentos" ? "border-b-2 border-[#00a2ff] text-[#00a2ff]" : "text-gray-400"}`}
          >
            Por Agrupamentos
          </button>
        </div>

        {!rotaResult ? (
          <>
            <p className="mb-6 text-sm text-gray-600">
              Selecione os itens abaixo para gerar a rota otimizada via{" "}
              <strong>{viewMode}</strong>.
            </p>

            {erro && (
              <div className="mb-4 rounded bg-red-50 p-3 text-xs font-bold text-red-500">
                {erro}
              </div>
            )}

            <div className="space-y-3">
              {itens.length === 0 ? (
                <p className="text-sm text-gray-400">
                  Nenhum item disponível...
                </p>
              ) : (
                itens.map((item) => (
                  <label
                    key={item.id}
                    className={`flex cursor-pointer items-center justify-between rounded-md border p-4 transition-all ${selectedIds.includes(item.id) ? "border-[#00a2ff] bg-[#eaf6ff]" : "border-gray-200 bg-white"}`}
                  >
                    <div className="flex items-center">
                      <input
                        type="checkbox"
                        checked={selectedIds.includes(item.id)}
                        onChange={() => toggleSelection(item.id)}
                        className="h-5 w-5 rounded text-[#00a2ff]"
                      />
                      <div className="ml-4">
                        <span className="block font-bold text-gray-800">
                          {viewMode === "individuais"
                            ? `Solicitação #${item.id}`
                            : `Agrupamento #${item.id}`}{" "}
                          - {item.classification}
                        </span>
                        <span className="text-xs text-gray-500">
                          {viewMode === "individuais"
                            ? item.address
                            : `${item.total_requests} solicitações inclusas`}
                        </span>
                      </div>
                    </div>
                  </label>
                ))
              )}
            </div>

            <button
              onClick={handleGenerateRoute}
              disabled={loading || selectedIds.length === 0}
              className={`mt-8 w-full rounded-md py-3 font-bold text-white shadow-md ${selectedIds.length > 0 && !loading ? "bg-[#00a2ff] hover:bg-blue-600" : "bg-gray-300"}`}
            >
              {loading ? "Processando Rota..." : `Gerar Rota Otimizada`}
            </button>
          </>
        ) : (
          <div className="animate-in fade-in duration-500">
            <div className="mb-6 rounded-lg border border-green-200 bg-green-50 p-6">
              <h3 className="text-lg font-bold text-green-800">
                ✅ Rota Gerada com Sucesso!
              </h3>
              <p className="text-sm text-green-600">
                Total de paradas: <strong>{rotaResult.total_stops}</strong>
              </p>
            </div>

            <h4 className="mb-4 font-bold text-gray-700">
              Sequência do Trajeto:
            </h4>
            <div className="mb-8 space-y-4">
              {rotaResult.ordered_stops.map((stop: any, index: number) => (
                <div key={index} className="flex items-center gap-4">
                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-[#00a2ff] text-white text-sm font-bold">
                    {index + 1}
                  </div>
                  <div className="flex-1 border-b pb-2">
                    <p className="text-sm font-bold text-gray-800">
                      {stop.address || `Centroide do Agrupamento #${stop.id}`}
                    </p>
                    <p className="text-xs text-gray-500">
                      {stop.classification} • {stop.distance_from_prev_km} km
                    </p>
                  </div>
                </div>
              ))}
            </div>

            <div className="flex gap-4">
              <button
                onClick={() => setRotaResult(null)}
                className="flex-1 rounded-md border border-gray-300 py-3 font-bold text-gray-600 hover:bg-gray-50"
              >
                Refazer
              </button>
              <a
                href={rotaResult.google_maps_url}
                target="_blank"
                className="flex-[2] rounded-md bg-green-500 py-3 text-center font-bold text-white hover:bg-green-600"
              >
                Iniciar Navegação GPS
              </a>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
