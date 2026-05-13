"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [mensagem, setMensagem] = useState("");
  const router = useRouter(); // Ferramenta do Next.js para trocar de página

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setMensagem("Autenticando...");

    try {
      const response = await fetch("http://localhost:5000/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        // 1. Salva o token no navegador do usuário
        localStorage.setItem("token", data.token);

        // 2. Manda o usuário para a tela principal!
        router.push("/dashboard");
      } else {
        setMensagem("❌ Erro da API: " + JSON.stringify(data));
      }
    } catch (error) {
      setMensagem("⚠️ Erro de conexão!");
    }
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        backgroundColor: "#f0f0f0",
      }}
    >
      <form
        onSubmit={handleLogin}
        style={{
          padding: "2rem",
          backgroundColor: "white",
          borderRadius: "8px",
          boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
          display: "flex",
          flexDirection: "column",
          gap: "1rem",
        }}
      >
        <h2 style={{ textAlign: "center", color: "#333" }}>Login ProPedido</h2>

        <input
          type="email"
          placeholder="E-mail"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={{
            padding: "0.5rem",
            borderRadius: "4px",
            border: "1px solid #ccc",
            color: "black",
          }}
        />

        <input
          type="password"
          placeholder="Senha"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{
            padding: "0.5rem",
            borderRadius: "4px",
            border: "1px solid #ccc",
            color: "black",
          }}
        />

        <button
          type="submit"
          style={{
            padding: "0.75rem",
            backgroundColor: "#0070f3",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
            fontWeight: "bold",
          }}
        >
          Entrar
        </button>

        {mensagem && (
          <div
            style={{
              marginTop: "1rem",
              padding: "1rem",
              backgroundColor: "#eee",
              borderRadius: "4px",
              color: "black",
              fontSize: "14px",
              maxWidth: "300px",
              wordWrap: "break-word",
            }}
          >
            {mensagem}
          </div>
        )}
      </form>
    </div>
  );
}
