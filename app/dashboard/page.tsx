import Layout from "../../components/Layout";

export default function Dashboard() {
  return (
    <Layout>
      <div className="rounded-lg bg-white p-6 shadow-sm">
        <h2 className="mb-4 text-xl font-bold text-gray-800">Visão Geral</h2>
        <p className="text-gray-600">
          Bem-vindo ao painel administrativo ProPedido.
        </p>
      </div>
    </Layout>
  );
}
