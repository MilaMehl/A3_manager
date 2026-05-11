import Layout from "../../components/Layout";

export default function Relatorios() {
  return (
    <Layout>
      <div className="rounded-lg bg-white p-8 shadow-sm">
        <h2 className="mb-6 text-xl font-bold text-gray-800">
          Relatórios Gerenciais
        </h2>
        <div className="flex h-64 flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-200 bg-gray-50">
          <span className="text-4xl">📊</span>
          <p className="mt-4 font-medium text-gray-500">
            Módulo de relatórios em desenvolvimento.
          </p>
        </div>
      </div>
    </Layout>
  );
}
