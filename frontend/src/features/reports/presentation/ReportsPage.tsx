import React from "react";
import { FileText, Download, BarChart3, TrendingUp, Users } from "lucide-react";
import { Button } from "../../../shared/components/Button";

export function ReportsPage() {
  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-gray-300 pb-6">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-gray-900">Relatórios Gerenciais</h1>
          <p className="text-lg text-gray-600 mt-2">Visão geral e exportação de dados do sistema.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg border border-gray-300 shadow-sm flex flex-col items-center text-center gap-4">
          <div className="h-16 w-16 bg-blue-100 text-blue-800 rounded-full flex items-center justify-center">
            <BarChart3 className="h-8 w-8" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-gray-900">Serviços Executados</h3>
            <p className="text-sm text-gray-600 mt-1">Relatório detalhado de todos os serviços prestados por período.</p>
          </div>
          <Button variant="secondary" className="w-full mt-auto gap-2">
            <Download className="h-4 w-4" />
            Exportar PDF
          </Button>
        </div>

        <div className="bg-white p-6 rounded-lg border border-gray-300 shadow-sm flex flex-col items-center text-center gap-4">
          <div className="h-16 w-16 bg-green-100 text-green-800 rounded-full flex items-center justify-center">
            <TrendingUp className="h-8 w-8" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-gray-900">Faturamento</h3>
            <p className="text-sm text-gray-600 mt-1">Balanço financeiro de pagamentos recebidos e pendentes.</p>
          </div>
          <Button variant="secondary" className="w-full mt-auto gap-2">
            <Download className="h-4 w-4" />
            Exportar Excel
          </Button>
        </div>

        <div className="bg-white p-6 rounded-lg border border-gray-300 shadow-sm flex flex-col items-center text-center gap-4">
          <div className="h-16 w-16 bg-purple-100 text-purple-800 rounded-full flex items-center justify-center">
            <Users className="h-8 w-8" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-gray-900">Produtores Ativos</h3>
            <p className="text-sm text-gray-600 mt-1">Listagem completa de produtores e histórico de serviços.</p>
          </div>
          <Button variant="secondary" className="w-full mt-auto gap-2">
            <Download className="h-4 w-4" />
            Exportar PDF
          </Button>
        </div>
      </div>
    </div>
  );
}
