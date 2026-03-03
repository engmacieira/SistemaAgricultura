import React, { useEffect, useState } from "react";
import { Producer } from "../domain/Producer";
import { ProducerRepository } from "../data/ProducerRepository";
import { Button } from "../../../shared/components/Button";
import { DataTable } from "../../../shared/components/DataTable";
import { Modal } from "../../../shared/components/Modal";
import { Plus, Search, UserPlus, Edit } from "lucide-react";

const repository = new ProducerRepository();

export function ProducersPage() {
  const [producers, setProducers] = useState<Producer[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  
  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  
  // Form State
  const [formData, setFormData] = useState({
    name: "",
    cpfCnpj: "",
    property: "",
    totalArea: 0,
    status: "Ativo" as string,
  });

  const fetchProducers = async () => {
    setLoading(true);
    try {
      const data = await repository.getProducers();
      setProducers(data);
    } catch (error) {
      console.error(error);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchProducers();
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ 
      ...prev, 
      [name]: name === "totalArea" ? Number(value) : value 
    }));
  };

  const handleNewClick = () => {
    setFormData({
      name: "",
      cpfCnpj: "",
      property: "",
      totalArea: 0,
      status: "Ativo",
    });
    setEditingId(null);
    setIsModalOpen(true);
  };

  const handleEditClick = (producer: Producer) => {
    setFormData({
      name: producer.name,
      cpfCnpj: producer.cpfCnpj,
      property: producer.property,
      totalArea: producer.totalArea,
      status: producer.status,
    });
    setEditingId(producer.id);
    setIsModalOpen(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    if (editingId) {
      await repository.updateProducer(editingId, formData);
    } else {
      await repository.addProducer(formData);
    }
    
    await fetchProducers(); // Refresh list
    
    setIsSubmitting(false);
    setIsModalOpen(false);
    setEditingId(null);
  };

  const filteredProducers = producers.filter((p) =>
    p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.cpfCnpj.includes(searchTerm)
  );

  const columns = [
    { header: "Nome do Produtor", accessorKey: "name" },
    { header: "CPF/CNPJ", accessorKey: "cpfCnpj" },
    { header: "Propriedade", accessorKey: "property" },
    { header: "Área Total (ha)", accessorKey: "totalArea" },
    {
      header: "Status",
      accessorKey: "status",
      cell: (item: Producer) => (
        <span
          className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-bold uppercase tracking-wider ${
            item.status === "Ativo"
              ? "bg-green-100 text-green-800 border border-green-300"
              : "bg-red-100 text-red-800 border border-red-300"
          }`}
        >
          {item.status}
        </span>
      ),
    },
    {
      header: "Ações",
      accessorKey: "actions",
      cell: (item: Producer) => (
        <Button 
          variant="ghost" 
          size="sm" 
          onClick={(e) => {
            e.stopPropagation();
            handleEditClick(item);
          }}
          className="h-8 w-8 p-0 text-blue-600 hover:text-blue-800 hover:bg-blue-50"
          title="Editar Produtor"
        >
          <Edit className="h-4 w-4" />
        </Button>
      ),
    }
  ];

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-gray-300 pb-6">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-gray-900">Produtores Rurais</h1>
          <p className="text-lg text-gray-600 mt-2">Gerencie o cadastro de produtores e suas propriedades.</p>
        </div>
        <Button size="lg" className="shrink-0 gap-2" onClick={handleNewClick}>
          <UserPlus className="h-5 w-5" />
          Novo Produtor
        </Button>
      </div>

      <div className="flex items-center gap-4 bg-white p-4 rounded-lg border border-gray-300 shadow-sm">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-500" />
          <input
            type="text"
            placeholder="Buscar por nome ou CPF/CNPJ..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="h-12 w-full rounded-md border border-gray-300 pl-12 pr-4 text-base font-medium text-gray-900 placeholder-gray-500 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      {loading ? (
        <div className="flex h-64 items-center justify-center rounded-lg border border-gray-300 bg-white">
          <div className="text-xl font-bold text-gray-500 animate-pulse">Carregando produtores...</div>
        </div>
      ) : (
        <DataTable data={filteredProducers} columns={columns} />
      )}

      <Modal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        title={editingId ? "Editar Produtor" : "Cadastrar Novo Produtor"}
      >
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <label htmlFor="name" className="block text-sm font-bold text-gray-900">Nome Completo</label>
              <input
                id="name"
                name="name"
                type="text"
                required
                value={formData.name}
                onChange={handleInputChange}
                className="h-12 w-full rounded-md border border-gray-300 px-4 text-base font-medium text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Ex: João da Silva"
              />
            </div>
            <div className="space-y-2">
              <label htmlFor="cpfCnpj" className="block text-sm font-bold text-gray-900">CPF ou CNPJ</label>
              <input
                id="cpfCnpj"
                name="cpfCnpj"
                type="text"
                required
                value={formData.cpfCnpj}
                onChange={handleInputChange}
                className="h-12 w-full rounded-md border border-gray-300 px-4 text-base font-medium text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="000.000.000-00"
              />
            </div>
            <div className="space-y-2">
              <label htmlFor="property" className="block text-sm font-bold text-gray-900">Nome da Propriedade</label>
              <input
                id="property"
                name="property"
                type="text"
                required
                value={formData.property}
                onChange={handleInputChange}
                className="h-12 w-full rounded-md border border-gray-300 px-4 text-base font-medium text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Ex: Fazenda Boa Vista"
              />
            </div>
            <div className="space-y-2">
              <label htmlFor="totalArea" className="block text-sm font-bold text-gray-900">Área Total (ha)</label>
              <input
                id="totalArea"
                name="totalArea"
                type="number"
                step="0.01"
                required
                value={formData.totalArea}
                onChange={handleInputChange}
                className="h-12 w-full rounded-md border border-gray-300 px-4 text-base font-medium text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Ex: 150.5"
              />
            </div>
            <div className="space-y-2">
              <label htmlFor="status" className="block text-sm font-bold text-gray-900">Status</label>
              <select
                id="status"
                name="status"
                value={formData.status}
                onChange={handleInputChange}
                className="h-12 w-full rounded-md border border-gray-300 px-4 text-base font-medium text-gray-900 bg-white focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="Ativo">Ativo</option>
                <option value="Inativo">Inativo</option>
              </select>
            </div>
          </div>
          
          <div className="flex justify-end gap-4 pt-6 border-t border-gray-200 mt-8">
            <Button 
              type="button" 
              variant="ghost" 
              onClick={() => setIsModalOpen(false)}
              disabled={isSubmitting}
            >
              Cancelar
            </Button>
            <Button 
              type="submit" 
              disabled={isSubmitting}
            >
              {isSubmitting ? "Salvando..." : "Salvar Produtor"}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
