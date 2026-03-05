import React, { useEffect, useState, useCallback } from "react";
import { SystemLog } from "../../logs/domain/SystemLog";
import { logRepository } from "../../logs/data/LogRepository";
import { DataTable } from "../../../shared/components/DataTable";
import { Pagination } from "../../../shared/components/Pagination";
import { Modal } from "../../../shared/components/Modal";
import { Search, Eye } from "lucide-react";

export function SystemLogsPage() {
  const [logs, setLogs] = useState<SystemLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");

  const [selectedJson, setSelectedJson] = useState<{ title: string; content: string } | null>(null);

  const [currentPage, setCurrentPage] = useState(0);
  const [totalPages, setTotalPages] = useState(0);
  const [sortConfig, setSortConfig] = useState<{ sortBy: string; order: "asc" | "desc" }>({
    sortBy: "timestamp",
    order: "desc",
  });
  const limit = 10;

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedSearch(searchTerm);
      setCurrentPage(0); // Reset page on search
    }, 500);
    return () => clearTimeout(handler);
  }, [searchTerm]);

  useEffect(() => {
    const fetchLogs = async () => {
      setLoading(true);
      try {
        const response = await logRepository.getLogs(
          currentPage * limit,
          limit,
          sortConfig.sortBy,
          sortConfig.order,
          debouncedSearch
        );
        setLogs(response.items);
        setTotalPages(response.pages);
      } catch (error) {
        console.error("Failed to fetch logs", error);
      } finally {
        setLoading(false);
      }
    };
    fetchLogs();
  }, [currentPage, sortConfig, debouncedSearch]);

  const handleSort = (column: string) => {
    setSortConfig((current) => {
      if (current.sortBy === column) {
        return { sortBy: column, order: current.order === "asc" ? "desc" : "asc" };
      }
      return { sortBy: column, order: "asc" };
    });
  };

  const getActionColor = (action: string) => {
    switch (action) {
      case "CRIAR": return "bg-green-100 text-green-800 border-green-300";
      case "EDITAR": return "bg-blue-100 text-blue-800 border-blue-300";
      case "EXCLUIR": return "bg-red-100 text-red-800 border-red-300";
      case "LOGIN": return "bg-purple-100 text-purple-800 border-purple-300";
      case "LOGOUT": return "bg-gray-100 text-gray-800 border-gray-300";
      default: return "bg-gray-100 text-gray-800 border-gray-300";
    }
  };

  const renderJsonLink = (jsonStr: string | null | undefined, title: string) => {
    if (!jsonStr) return <span className="text-gray-400">-</span>;
    return (
      <button
        type="button"
        onClick={() => setSelectedJson({ title, content: jsonStr })}
        className="inline-flex items-center gap-1 text-sm font-medium text-blue-600 hover:text-blue-800 transition-colors"
      >
        <Eye className="w-4 h-4" />
        Visualizar
      </button>
    );
  };

  const columns = [
    {
      header: "Data/Hora",
      accessorKey: "timestamp",
      cell: (item: SystemLog) => {
        const date = new Date(item.timestamp);
        return new Intl.DateTimeFormat("pt-BR", {
          day: "2-digit",
          month: "2-digit",
          year: "numeric",
          hour: "2-digit",
          minute: "2-digit",
        }).format(date);
      },
    },
    { header: "Usuário", accessorKey: "userName" },
    {
      header: "Ação",
      accessorKey: "action",
      cell: (item: SystemLog) => (
        <span className={`inline-flex items-center rounded-full px-2 py-1 text-xs font-bold uppercase tracking-wider border ${getActionColor(item.action)}`}>
          {item.action}
        </span>
      ),
    },
    { header: "Entidade", accessorKey: "entity" },
    { header: "Detalhes", accessorKey: "details" },
    {
      header: "Registro Anterior",
      accessorKey: "dados_anteriores",
      cell: (item: SystemLog) => renderJsonLink(item.dados_anteriores, "Registro Anterior"),
    },
    {
      header: "Registro Novo",
      accessorKey: "dados_novos",
      cell: (item: SystemLog) => renderJsonLink(item.dados_novos, "Registro Novo"),
    },
  ];

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-gray-300 pb-6">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-gray-900">Logs de Auditoria</h1>
          <p className="text-lg text-gray-600 mt-2">Histórico de ações realizadas no sistema para segurança e controle.</p>
        </div>
      </div>

      <div className="flex items-center gap-4 bg-white p-4 rounded-lg border border-gray-300 shadow-sm">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-500" />
          <input
            type="text"
            placeholder="Buscar nos logs..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="h-12 w-full rounded-md border border-gray-300 pl-12 pr-4 text-base font-medium text-gray-900 placeholder-gray-500 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      {loading ? (
        <div className="flex h-64 items-center justify-center rounded-lg border border-gray-300 bg-white">
          <div className="text-xl font-bold text-gray-500 animate-pulse">Carregando logs...</div>
        </div>
      ) : (
        <div className="space-y-4">
          <DataTable
            data={logs}
            columns={columns}
            onSort={handleSort}
            sortConfig={sortConfig}
          />
          <Pagination
            currentPage={currentPage}
            totalPages={totalPages}
            onPageChange={setCurrentPage}
          />
        </div>
      )}

      {/* Modal para exibir JSON */}
      <Modal
        isOpen={!!selectedJson}
        onClose={() => setSelectedJson(null)}
        title={selectedJson?.title || "Detalhes"}
      >
        {selectedJson && (
          <div className="bg-gray-50 p-4 rounded-md border border-gray-200 overflow-auto max-h-[60vh]">
            <pre className="text-sm text-gray-800 whitespace-pre-wrap">
              {(() => {
                try {
                  return JSON.stringify(JSON.parse(selectedJson.content), null, 2);
                } catch {
                  return selectedJson.content;
                }
              })()}
            </pre>
          </div>
        )}
      </Modal>
    </div>
  );
}
