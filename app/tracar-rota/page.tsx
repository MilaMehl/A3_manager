"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function TracarRota() {
  const [pedidos, setPedidos] = useState<any[]>([]);
  const [selecionados, setSelecionados] = useState<number[]>([]);
  const [rota, setRota] = useState<any>(null);
  const [erro, setErro] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  // Coordenadas de origem (podem ser alteradas pelo usuário)
  const [lat, setLat] = useState("-27.6200"); // Exemplo genérico pra região
  const [lng, setLng] = useState("-48.6700");

  useEffect(() => {
    // Carrega as solicitações para o usuário escolher quais quer visitar
    const carregarSolicitacoes = async () => {
      const token = localStorage.getItem("token");
      if (!token) return router.push("/");

      try {
        const response = await fetch("http://localhost:5000/api/requests/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        const data = await response.json();
        if (response.ok) setPedidos(data.data);
      } catch (err) {
        setErro("Erro ao carregar solicitações.");
      }
    };
    carregarSolicitacoes();
  }, [router]);

  // Função para marcar/desmarcar os checkboxes
  const toggleSelecao = (id: number) => {
    setSelecionados((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id],
    );
  };

  // Função que chama o algoritmo do Python
  const calcularRota = async () => {
    if (selecionados.length === 0) {
      setErro("Selecione pelo menos uma solicitação para traçar a rota.");
      return;
    }

    setLoading(true);
    setErro("");
    setRota(null);
    const token = localStorage.getItem("token");

    try {
      const response = await fetch("http://localhost:5000/api/routes/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          latitude: parseFloat(lat),
          longitude: parseFloat(lng),
          request_ids: selecionados,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setRota(data);
      } else {
        setErro("Erro ao calcular rota: " + (data.error || "Tente novamente."));
      }
    } catch (error) {
      setErro("Erro de conexão com a API de rotas.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        padding: "2rem",
        backgroundColor: "#f8f9fa",
        minHeight: "100vh",
        color: "#333",
        width: "100%",
      }}
    >
      <div style={{ maxWidth: "900px", margin: "0 auto" }}>
        <header style={{ marginBottom: "2rem" }}>
          <h1>🗺️ Traçar Rota de Atendimento</h1>
          <p style={{ color: "#666" }}>
            Selecione as solicitações abaixo e clique em calcular para gerar a
            rota otimizada.
          </p>
        </header>

        {erro && (
          <p
            style={{
              color: "red",
              fontWeight: "bold",
              padding: "1rem",
              backgroundColor: "#ffe6e6",
              borderRadius: "8px",
            }}
          >
            {erro}
          </p>
        )}

        <div style={{ display: "flex", gap: "2rem", alignItems: "flex-start" }}>
          {/* LADO ESQUERDO: Lista para selecionar */}
          <div
            style={{
              flex: 1,
              backgroundColor: "white",
              padding: "1.5rem",
              borderRadius: "8px",
              boxShadow: "0 2px 4px rgba(0,0,0,0.05)",
            }}
          >
            <h3>1. Escolha os locais</h3>
            <p style={{ fontSize: "14px", color: "#888" }}>
              {selecionados.length} selecionados
            </p>

            <div
              style={{
                maxHeight: "400px",
                overflowY: "auto",
                border: "1px solid #eee",
                padding: "1rem",
                borderRadius: "4px",
                display: "flex",
                flexDirection: "column",
                gap: "10px",
              }}
            >
              {pedidos.map((p) => (
                <label
                  key={p.id}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "10px",
                    cursor: "pointer",
                    padding: "0.5rem",
                    borderBottom: "1px solid #f0f0f0",
                  }}
                >
                  <input
                    type="checkbox"
                    checked={selecionados.includes(p.id)}
                    onChange={() => toggleSelecao(p.id)}
                    style={{ width: "18px", height: "18px" }}
                  />
                  <div>
                    <strong style={{ display: "block", fontSize: "14px" }}>
                      ID #{p.id} - {p.classification}
                    </strong>
                    <span style={{ fontSize: "12px", color: "#666" }}>
                      {p.address}
                    </span>
                  </div>
                </label>
              ))}
            </div>
          </div>

          {/* LADO DIREITO: Controles e Resultado */}
          <div
            style={{
              flex: 1,
              display: "flex",
              flexDirection: "column",
              gap: "1.5rem",
            }}
          >
            <div
              style={{
                backgroundColor: "white",
                padding: "1.5rem",
                borderRadius: "8px",
                boxShadow: "0 2px 4px rgba(0,0,0,0.05)",
              }}
            >
              <h3>2. Sua Localização Atual</h3>
              <div style={{ display: "flex", gap: "10px", marginTop: "1rem" }}>
                <input
                  type="text"
                  placeholder="Latitude"
                  value={lat}
                  onChange={(e) => setLat(e.target.value)}
                  style={{
                    width: "100%",
                    padding: "0.5rem",
                    border: "1px solid #ccc",
                    borderRadius: "4px",
                    color: "black",
                  }}
                />
                <input
                  type="text"
                  placeholder="Longitude"
                  value={lng}
                  onChange={(e) => setLng(e.target.value)}
                  style={{
                    width: "100%",
                    padding: "0.5rem",
                    border: "1px solid #ccc",
                    borderRadius: "4px",
                    color: "black",
                  }}
                />
              </div>
              <button
                onClick={calcularRota}
                disabled={loading}
                style={{
                  width: "100%",
                  marginTop: "1rem",
                  padding: "1rem",
                  backgroundColor: "#fd7e14",
                  color: "white",
                  border: "none",
                  borderRadius: "4px",
                  cursor: "pointer",
                  fontWeight: "bold",
                  fontSize: "16px",
                }}
              >
                {loading ? "Calculando..." : "Traçar Melhor Rota"}
              </button>
            </div>

            {/* RESULTADO DA ROTA */}
            {rota && (
              <div
                style={{
                  backgroundColor: "#e6f2ff",
                  border: "2px solid #0070f3",
                  padding: "1.5rem",
                  borderRadius: "8px",
                }}
              >
                <h3 style={{ margin: "0 0 1rem 0", color: "#0070f3" }}>
                  ✅ Rota Calculada!
                </h3>
                <p>
                  <strong>Paradas:</strong> {rota.total_stops}
                </p>
                <p>
                  <strong>Distância Total:</strong> {rota.total_distance_km} km
                </p>

                <a
                  href={rota.google_maps_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{
                    display: "block",
                    textAlign: "center",
                    padding: "1rem",
                    backgroundColor: "#0070f3",
                    color: "white",
                    textDecoration: "none",
                    borderRadius: "4px",
                    fontWeight: "bold",
                    marginTop: "1rem",
                  }}
                >
                  📍 Abrir no Google Maps
                </a>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
