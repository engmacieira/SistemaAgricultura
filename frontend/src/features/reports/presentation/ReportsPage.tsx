import React, { useState, useEffect } from "react";
import { FileText, Download, BarChart3, TrendingUp, Users, Calendar, Filter } from "lucide-react";
import { Button } from "../../../shared/components/Button";

interface Producer {
  id: string;
  name: string;
  regiao_referencia: string;
}

export function ReportsPage() {
  const [producers, setProducers] = useState<Producer[]>([]);

  // States for Services Report
  const [servStart, setServStart] = useState("");
  const [servEnd, setServEnd] = useState("");

  // States for Billing Report
  const [billStart, setBillStart] = useState("");
  const [billEnd, setBillEnd] = useState("");
  const [billProducers, setBillProducers] = useState<string[]>([]);

  // States for Producers Report
  const [prodId, setProdId] = useState("");
  const [prodStatus, setProdStatus] = useState("");
  const [prodRegion, setProdRegion] = useState("");

  useEffect(() => {
    fetch("http://localhost:8000/produtores?size=1000")
      .then(res => res.json())
      .then(data => {
        if (data && data.items) {
          setProducers(data.items);
        } else if (Array.isArray(data)) {
          setProducers(data);
        }
      })
      .catch(err => console.error("Error fetching producers:", err));
  }, []);

  const handleExportServices = () => {
    if (!servStart || !servEnd) {
      alert("Por favor, selecione o período inicial e final.");
      return;
    }
    window.open(`http://localhost:8000/relatorios/servicos-executados?start_date=${servStart}&end_date=${servEnd}&format=pdf`, "_blank");
  };

  const handleExportBilling = () => {
    let url = `http://localhost:8000/relatorios/faturamento?`;
    if (billStart) url += `start_date=${billStart}&`;
    if (billEnd) url += `end_date=${billEnd}&`;
    if (billProducers.length > 0) {
      billProducers.forEach(p => {
        url += `producers=${encodeURIComponent(p)}&`;
      });
    }
    window.open(url, "_blank");
  };

  const handleExportProducers = () => {
    let url = `http://localhost:8000/relatorios/produtores?`;
    if (prodId) url += `producer_id=${prodId}&`;
    if (prodStatus) url += `status=${prodStatus}&`;
    if (prodRegion) url += `regiao=${encodeURIComponent(prodRegion)}&`;
    window.open(url, "_blank");
  };

  const regions = Array.from(new Set(producers.map(p => p.regiao_referencia).filter(r => r))).sort();

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-gray-300 pb-6">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-gray-900">Relatórios Gerenciais</h1>
          <p className="text-lg text-gray-600 mt-2">Filtre os dados para gerar relatórios detalhados em PDF ou Excel.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Bloco Serviços Executados */}
        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex flex-col gap-6">
          <div className="flex items-center gap-4">
            <div className="h-12 w-12 bg-blue-100 text-blue-700 rounded-lg flex items-center justify-center">
              <BarChart3 className="h-6 w-6" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-gray-900">Serviços Executados</h3>
              <p className="text-sm text-gray-500">Relatório de serviços concluídos.</p>
            </div>
          </div>

          <div className="space-y-4">
            <div className="grid grid-cols-1 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Início</label>
                <input
                  type="date"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                  value={servStart}
                  onChange={(e) => setServStart(e.target.value)}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Fim</label>
                <input
                  type="date"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                  value={servEnd}
                  onChange={(e) => setServEnd(e.target.value)}
                />
              </div>
            </div>
          </div>

          <Button onClick={handleExportServices} className="w-full gap-2 bg-blue-600 hover:bg-blue-700 text-white mt-auto">
            <Download className="h-4 w-4" />
            Gerar Relatório (PDF)
          </Button>
        </div>

        {/* Bloco Faturamento */}
        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex flex-col gap-6">
          <div className="flex items-center gap-4">
            <div className="h-12 w-12 bg-green-100 text-green-700 rounded-lg flex items-center justify-center">
              <TrendingUp className="h-6 w-6" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-gray-900">Faturamento</h3>
              <p className="text-sm text-gray-500">Balanço financeiro por período.</p>
            </div>
          </div>

          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Início</label>
                <input
                  type="date"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-green-500 focus:border-green-500"
                  value={billStart}
                  onChange={(e) => setBillStart(e.target.value)}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Fim</label>
                <input
                  type="date"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-green-500 focus:border-green-500"
                  value={billEnd}
                  onChange={(e) => setBillEnd(e.target.value)}
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Produtores (Opcional)</label>
              <select
                multiple
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-green-500 focus:border-green-500 h-24"
                value={billProducers}
                onChange={(e) => {
                  const options = Array.from(e.target.selectedOptions).map(opt => (opt as HTMLOptionElement).value);
                  setBillProducers(options);
                }}
              >
                {producers.map(p => (
                  <option key={p.id} value={p.name}>{p.name}</option>
                ))}
              </select>
              <p className="text-xs text-gray-400 mt-1">Segure Ctrl para selecionar vários.</p>
            </div>
          </div>

          <Button onClick={handleExportBilling} variant="secondary" className="w-full gap-2 border-green-600 text-green-700 hover:bg-green-50 mt-auto">
            <Download className="h-4 w-4" />
            Gerar Relatório (PDF)
          </Button>
        </div>

        {/* Bloco Produtores */}
        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex flex-col gap-6">
          <div className="flex items-center gap-4">
            <div className="h-12 w-12 bg-purple-100 text-purple-700 rounded-lg flex items-center justify-center">
              <Users className="h-6 w-6" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-gray-900">Produtores</h3>
              <p className="text-sm text-gray-500">Informações completas e cadastro.</p>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Produtor Específico</label>
              <select
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-purple-500 focus:border-purple-500"
                value={prodId}
                onChange={(e) => setProdId(e.target.value)}
              >
                <option value="">Todos os Produtores</option>
                {producers.map(p => (
                  <option key={p.id} value={p.id}>{p.name}</option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
                <select
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-purple-500 focus:border-purple-500"
                  value={prodStatus}
                  onChange={(e) => setProdStatus(e.target.value)}
                >
                  <option value="">Todos</option>
                  <option value="Ativo">Ativos</option>
                  <option value="Inativo">Inativos</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Comunidade</label>
                <select
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-purple-500 focus:border-purple-500"
                  value={prodRegion}
                  onChange={(e) => setProdRegion(e.target.value)}
                >
                  <option value="">Todas</option>
                  {regions.map(r => (
                    <option key={r} value={r}>{r}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          <Button onClick={handleExportProducers} className="w-full gap-2 bg-purple-600 hover:bg-purple-700 text-white mt-auto">
            <Download className="h-4 w-4" />
            Ficha Completa (PDF)
          </Button>
        </div>
      </div>
    </div>
  );
}
