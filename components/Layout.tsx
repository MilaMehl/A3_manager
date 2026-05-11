"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ReactNode } from "react";

interface LayoutProps {
  children: ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const pathname = usePathname();

  const getLinkClass = (path: string) => {
    const isActive = pathname === path;
    return `flex items-center px-6 py-3 ${
      isActive
        ? "rounded-r-full bg-[#eaf6ff] text-[#00a2ff]"
        : "text-gray-500 hover:text-[#00a2ff]"
    }`;
  };

  return (
    <div className="flex min-h-screen bg-[#f8f9fc]">
      <aside className="flex w-64 flex-col bg-white shadow-md">
        <div className="flex flex-col items-center border-b border-gray-100 p-6">
          <h1 className="text-center text-lg font-bold text-gray-800">
            AMO Pedra
            <br />
            Branca
          </h1>
          <div className="mt-6 flex flex-col items-center">
            <div className="mb-2 flex h-16 w-16 items-center justify-center rounded-lg bg-[#0f3460]">
              <span className="font-bold text-[10px] text-white">AMO</span>
            </div>
            <span className="text-sm font-bold text-gray-700">Triceras</span>
            <span className="text-xs text-gray-400">admin</span>
          </div>
        </div>

        <nav className="flex-1 py-4 pr-4">
          <ul className="space-y-2 text-sm font-medium">
            <li>
              <Link href="/dashboard" className={getLinkClass("/dashboard")}>
                <span className="mr-3 text-lg">⏱</span>
                Dashboard
              </Link>
            </li>
            <li>
              <Link
                href="/solicitacoes"
                className={getLinkClass("/solicitacoes")}
              >
                <span className="mr-3 text-lg">📋</span>
                Solicitações
              </Link>
            </li>
            <li>
              <Link href="/mensagens" className={getLinkClass("/mensagens")}>
                <span className="mr-3 text-lg">✉</span>
                Mensagens
              </Link>
            </li>
            <li>
              <Link href="/usuarios" className={getLinkClass("/usuarios")}>
                <span className="mr-3 text-lg">👥</span>
                Usuários
              </Link>
            </li>
            <li>
              <Link href="/equipes" className={getLinkClass("/equipes")}>
                <span className="mr-3 text-lg">🚌</span>
                Equipes de Atendimento
              </Link>
            </li>
            <li>
              <Link
                href="/roteirizacao"
                className={getLinkClass("/roteirizacao")}
              >
                <span className="mr-3 text-lg">🗺️</span>
                Traçar Rota
              </Link>
            </li>
            <li>
              <Link href="/relatorios" className={getLinkClass("/relatorios")}>
                <span className="mr-3 text-lg">📱</span>
                Relatórios
              </Link>
            </li>
          </ul>
        </nav>
      </aside>

      <div className="flex flex-1 flex-col">
        <header className="flex h-16 items-center justify-between bg-white px-8 shadow-sm">
          <button className="text-2xl text-[#00a2ff]">≡</button>

          <div className="flex items-center space-x-4">
            <span className="text-xl">🇧🇷</span>
            <span className="text-xl opacity-50">🇺🇸</span>
            <div className="flex h-8 w-8 items-center justify-center rounded-full border border-gray-300 bg-gray-100">
              <span className="text-xs text-gray-500">↪</span>
            </div>
          </div>
        </header>

        <main className="p-8">{children}</main>
      </div>
    </div>
  );
}
