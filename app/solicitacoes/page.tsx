"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function Solicitacoes() {
  const [viewMode, setViewMode] = useState<"individuais" | "agrupamentos">(
    "individuais",
  );
  const [pedidos, setPedidos] = useState<any[]>([]);
  const [agrupamentos, setAgrupamentos] = useState<any[]>([]);
  const [total, setTotal] = useState(0);
  const [busca, setBusca] = useState("");
  const [erro, setErro] = useState("");

  // Controle de qual grupo está "aberto" na sanfona
  const [grupoExpandido, setGrupoExpandido] = useState<number | null>(null);

  const router = useRouter();

  const carregarDados = async (filtroEndereco = "") => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/");
      return;
    }

    try {
      // Decide qual API chamar com base na aba selecionada
      const endpoint =
        viewMode === "individuais" ? "/api/requests/" : "/api/groupings/";

      const url = filtroEndereco
        ? `http://localhost:5000${endpoint}?address=${filtroEndereco}`
        : `http://localhost:5000${endpoint}`;

      const response = await fetch(url, {
        headers: { Authorization: `Bearer ${token}` },
      });

      const data = await response.json();

      if (response.ok) {
        if (viewMode === "individuais") {
          setPedidos(data.data);
        } else {
          setAgrupamentos(data.data);
        }
        setTotal(data.total);
        setErro(""); // Limpa erros antigos
      } else {
        setErro("Erro na API: " + (data.error || "Falha desconhecida"));
      }
    } catch (error) {
      setErro("Erro de conexão com o servidor Python.");
    }
  };

  // Recarrega os dados toda vez que a aba (viewMode) mudar
  useEffect(() => {
    carregarDados(busca);
    setGrupoExpandido(null); // Fecha a sanfona ao trocar de aba
  }, [viewMode]);

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
      <div style={{ maxWidth: "800px", margin: "0 auto" }}>
        {/* Cabeçalho */}
        <header
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "1.5rem",
          }}
        >
          <h1>📋 Solicitações ({total})</h1>
          <button
            onClick={() => router.push("/dashboard")}
            style={{
              padding: "0.5rem 1rem",
              backgroundColor: "#6c757d",
              color: "white",
              border: "none",
              borderRadius: "4px",
              cursor: "pointer",
              fontWeight: "bold",
            }}
          >
            ⬅ Voltar ao Menu
          </button>
        </header>

        {/* Abas (Toggle) */}
        <div style={{ display: "flex", gap: "10px", marginBottom: "1.5rem" }}>
          <button
            onClick={() => setViewMode("individuais")}
            style={{
              flex: 1,
              padding: "0.75rem",
              borderRadius: "4px",
              fontWeight: "bold",
              border: "1px solid #0070f3",
              cursor: "pointer",
              backgroundColor: viewMode === "individuais" ? "#0070f3" : "white",
              color: viewMode === "individuais" ? "white" : "#0070f3",
              transition: "0.2s",
            }}
          >
            Visão Individual
          </button>
          <button
            onClick={() => setViewMode("agrupamentos")}
            style={{
              flex: 1,
              padding: "0.75rem",
              borderRadius: "4px",
              fontWeight: "bold",
              border: "1px solid #28a745",
              cursor: "pointer",
              backgroundColor:
                viewMode === "agrupamentos" ? "#28a745" : "white",
              color: viewMode === "agrupamentos" ? "white" : "#28a745",
              transition: "0.2s",
            }}
          >
            Visão em Agrupamentos
          </button>
        </div>

        {/* Barra de Busca */}
        <div style={{ marginBottom: "2rem", display: "flex", gap: "10px" }}>
          <input
            type="text"
            placeholder="Filtrar por endereço..."
            value={busca}
            onChange={(e) => setBusca(e.target.value)}
            style={{
              flex: 1,
              padding: "0.75rem",
              borderRadius: "4px",
              border: "1px solid #ccc",
              color: "black",
            }}
          />
          <button
            onClick={() => carregarDados(busca)}
            style={{
              padding: "0.75rem 1.5rem",
              backgroundColor: "#343a40",
              color: "white",
              border: "none",
              borderRadius: "4px",
              cursor: "pointer",
              fontWeight: "bold",
            }}
          >
            Buscar
          </button>
        </div>

        {erro && <p style={{ color: "red", fontWeight: "bold" }}>{erro}</p>}

        {/* Lista de Dados (Renderização Condicional) */}
        <div style={{ display: "grid", gap: "1rem" }}>
          {/* MODO INDIVIDUAL */}
          {viewMode === "individuais" &&
            (pedidos.length === 0 ? (
              <p style={{ textAlign: "center", color: "#666" }}>
                Nenhum registro encontrado.
              </p>
            ) : (
              pedidos.map((p) => (
                <div
                  key={p.id}
                  style={{
                    backgroundColor: "white",
                    padding: "1.5rem",
                    borderRadius: "8px",
                    boxShadow: "0 2px 4px rgba(0,0,0,0.05)",
                    borderLeft: "5px solid #0070f3",
                  }}
                >
                  <div
                    style={{ display: "flex", justifyContent: "space-between" }}
                  >
                    <span style={{ fontSize: "12px", color: "#888" }}>
                      ID: #{p.id}
                    </span>
                    <span
                      style={{
                        backgroundColor: "#e1f0ff",
                        color: "#0070f3",
                        padding: "2px 8px",
                        borderRadius: "12px",
                        fontSize: "12px",
                        fontWeight: "bold",
                      }}
                    >
                      {p.status}
                    </span>
                  </div>
                  <h3 style={{ margin: "0.5rem 0" }}>{p.classification}</h3>
                  <p style={{ margin: 0, color: "#555" }}>📍 {p.address}</p>
                </div>
              ))
            ))}

          {/* MODO AGRUPAMENTOS */}
          {viewMode === "agrupamentos" &&
            (agrupamentos.length === 0 ? (
              <p style={{ textAlign: "center", color: "#666" }}>
                Nenhum agrupamento encontrado.
              </p>
            ) : (
              agrupamentos.map((grupo) => (
                <div
                  key={grupo.id}
                  style={{
                    backgroundColor: "white",
                    borderRadius: "8px",
                    boxShadow: "0 2px 4px rgba(0,0,0,0.05)",
                    borderLeft: "5px solid #28a745",
                    overflow: "hidden",
                  }}
                >
                  {/* Cabeçalho do Grupo (Clicável) */}
                  <div
                    onClick={() =>
                      setGrupoExpandido(
                        grupoExpandido === grupo.id ? null : grupo.id,
                      )
                    }
                    style={{
                      padding: "1.5rem",
                      cursor: "pointer",
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                      backgroundColor:
                        grupoExpandido === grupo.id ? "#f1f8f3" : "white",
                    }}
                  >
                    <div>
                      <h3 style={{ margin: "0 0 0.5rem 0", color: "#28a745" }}>
                        Agrupamento #{grupo.id}
                      </h3>
                      <p style={{ margin: 0, color: "#555", fontSize: "14px" }}>
                        <strong>{grupo.total_requests}</strong> solicitações •
                        Classificação: {grupo.classification}
                      </p>
                    </div>
                    <span style={{ fontSize: "20px" }}>
                      {grupoExpandido === grupo.id ? "🔼" : "🔽"}
                    </span>
                  </div>

                  {/* Miolo da Sanfona (As solicitações dentro do grupo) */}
                  {grupoExpandido === grupo.id && (
                    <div
                      style={{
                        padding: "1.5rem",
                        backgroundColor: "#fafafa",
                        borderTop: "1px solid #eee",
                      }}
                    >
                      <h4
                        style={{
                          margin: "0 0 1rem 0",
                          fontSize: "14px",
                          color: "#666",
                        }}
                      >
                        Pedidos neste grupo:
                      </h4>
                      <ul
                        style={{
                          listStyle: "none",
                          padding: 0,
                          margin: 0,
                          display: "flex",
                          flexDirection: "column",
                          gap: "10px",
                        }}
                      >
                        {grupo.requests.map((req: any) => (
                          <li
                            key={req.id}
                            style={{
                              padding: "10px",
                              backgroundColor: "white",
                              border: "1px solid #ddd",
                              borderRadius: "4px",
                              fontSize: "14px",
                            }}
                          >
                            <strong>ID #{req.id}</strong> - {req.address} <br />
                            <span style={{ color: "#888", fontSize: "12px" }}>
                              Status: {req.status}
                            </span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))
            ))}
        </div>
      </div>
    </div>
  );
}
