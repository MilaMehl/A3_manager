import Layout from "../../components/Layout";

export default function Usuarios() {
  return (
    <Layout>
      <div className="rounded-lg bg-white p-8 shadow-sm">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="text-xl font-bold text-gray-800">
            Gestão de Usuários
          </h2>
          <button className="rounded-md bg-[#00a2ff] px-6 py-2 font-semibold text-white shadow-sm transition-colors hover:bg-blue-600">
            Novo Usuário
          </button>
        </div>
        <div className="flex h-64 flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-200 bg-gray-50">
          <span className="text-4xl">👥</span>
          <p className="mt-4 font-medium text-gray-500">
            Módulo de gestão de usuários em desenvolvimento.
          </p>
        </div>
      </div>
    </Layout>
  );
}
