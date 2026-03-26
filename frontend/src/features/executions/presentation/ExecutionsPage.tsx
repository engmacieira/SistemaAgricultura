import React, { useEffect, useState } from "react";
import { Execution } from "../domain/Execution";
import { ExecutionRepository } from "../data/ExecutionRepository";
import { RequestRepository } from "../../requests/data/RequestRepository";
import { Button } from "../../../shared/components/Button";
import { DataTable } from "../../../shared/components/DataTable";
import { Trash2, ClipboardList } from "lucide-react";
import { Pagination } from "../../../shared/components/Pagination";

const repository = new ExecutionRepository();
const requestRepository = new RequestRepository();

export function ExecutionsPage() {
  const [executions, setExecutions] = useState<Execution[]>([]);
  // Dicionário para mapear o solicitacaoId -> Nome do Produtor
  const [producerNames, setProducerNames] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(true);

  // Paginação
  const [currentPage, setCurrentPage] = useState(0);
  const [limit] = useState(10);
  const [totalItems, setTotalItems] = useState(0);

  const fetchData = async () => {
    setLoading(true);
    try {
      // 1. Busca os pedidos da fila para podermos pegar os nomes dos produtores
      // (Passando skip=0, limit=1000 para garantir que pegamos o histórico)
      const reqs = await requestRepository.getRequests({ skip: 0, limit: 1000 });
      const namesMap: Record<string, string> = {};

      // Criamos um mapa rápido para não ter que fazer find() toda hora
      if (Array.isArray(reqs)) {
        reqs.forEach(r => {
          namesMap[r.id] = r.producerName;
        });
      }
      setProducerNames(namesMap);

      // 2. Busca o histórico de execuções reais
      const data = await repository.getExecutions({ skip: currentPage * limit, limit });
      setExecutions(data.items || []);
      setTotalItems(data.total || 0);
    } catch (error) {
      console.error("Erro ao buscar histórico de execuções:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [currentPage]);

  const handleDelete = async (id: string) => {
    if (window.confirm("Atenção: Ao excluir este histórico, o pagamento gerado poderá ficar órfão. Deseja continuar?")) {
      try {
        // Assume que o método deleteExecution existe no seu repositório
        // Se não existir, avise-me que eu mando o código para adicionar!
        await (repository as any).deleteExecution(id);
        fetchData();
      } catch (error) {
        console.error("Erro ao deletar execução:", error);
        alert("Erro ao excluir o registro.");
      }
    }
  };

  const columns = [
    {
      header: "Data",
      accessorKey: "date" as keyof Execution,
      render: (value: any) => new Date(value).toLocaleDateString()
    },
    {
      header: "Produtor (Fila)",
      accessorKey: "solicitacaoId" as keyof Execution,
      // Mapeia o ID da Fila para o nome do Produtor usando nosso dicionário
      render: (val: any) => <span className="font-semibold text-gray-900">{producerNames[val as string] || "Desconhecido"}</span>
    },
    {
      header: "Serviço",
      accessorKey: "serviceName" as keyof Execution
    },
    {
      header: "Qtd / Unid",
      accessorKey: "quantity" as keyof Execution,
      render: (_: any, item: Execution) => `${item.quantity} ${item.unit}`
    },
    {
      header: "Operador/Máquina",
      accessorKey: "operador_maquina" as keyof Execution,
      render: (val: any) => val || <span className="text-gray-400 italic">Não informado</span>
    },
    {
      header: "Total Faturado",
      accessorKey: "totalValue" as keyof Execution,
      render: (value: any) => (
        <span className="font-bold text-green-700">
          R$ {Number(value).toFixed(2)}
        </span>
      )
    },
    {
      header: "Ações",
      accessorKey: "id" as keyof Execution,
      render: (id: any) => (
        <div className="flex gap-2">
          <Button variant="ghost" size="sm" onClick={() => handleDelete(id as string)} className="text-red-600 hover:text-red-700 hover:bg-red-50">
            <Trash2 className="w-4 h-4" />
          </Button>
        </div>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center">
            <ClipboardList className="w-6 h-6 mr-2 text-blue-600" />
            Histórico de Serviços (Ordens de Serviço)
          </h1>
          <p className="text-gray-500 mt-1">
            Visualização de todos os serviços que já foram realizados em campo e faturados.
          </p>
        </div>
        <div className="bg-blue-50 text-blue-800 text-sm p-3 rounded border border-blue-100 max-w-xs text-right">
          <strong>Nota:</strong> Novos serviços devem ser registrados dando "Baixa" na Fila de Espera.
        </div>
      </div>

      <div className="bg-white rounded-lg shadow">
        {loading ? (
          <div className="text-center py-10 text-gray-500">
            Carregando histórico de serviços...
          </div>
        ) : (
          <DataTable
            columns={columns}
            data={executions}
          />
        )}

        {!loading && totalItems > 0 && (
          <div className="p-4 border-t border-gray-200">
            <Pagination
              currentPage={currentPage}
              totalPages={Math.ceil(totalItems / limit)}
              onPageChange={setCurrentPage}
            />
          </div>
        )}
      </div>
    </div>
  );
}