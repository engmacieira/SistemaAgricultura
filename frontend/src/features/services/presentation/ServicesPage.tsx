import React, { useEffect, useState, useCallback } from "react";
import { AgriculturalService } from "../domain/AgriculturalService";
import { ServiceRepository } from "../data/ServiceRepository";
import { settingsRepository } from "../../settings/data/SettingsRepository";
import { Button } from "../../../shared/components/Button";
import { DataTable } from "../../../shared/components/DataTable";
import { Modal } from "../../../shared/components/Modal";
import { Pagination } from "../../../shared/components/Pagination";
import { Plus, Search, Tractor, Edit, Trash2, AlertTriangle } from "lucide-react";

const repository = new ServiceRepository();

export function ServicesPage() {
  const [services, setServices] = useState<AgriculturalService[]>([]);
  const [unitsList, setUnitsList] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");

  // Pagination State
  const [currentPage, setCurrentPage] = useState(0);
  const [totalItems, setTotalItems] = useState(0);
  const [pageSize] = useState(10);

  // Sorting State
  const [sortConfig, setSortConfig] = useState<{ sortBy: string; order: "asc" | "desc" }>({
    sortBy: "name",
    order: "asc",
  });

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [serviceToDelete, setServiceToDelete] = useState<AgriculturalService | null>(null);

  // Form State
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    unit: "Hectare",
    basePrice: 0,
    active: true,
  });

  const fetchServicesAndUnits = useCallback(async () => {
    setLoading(true);
    try {
      const [{ items, total }, unitsData] = await Promise.all([
        repository.getServices(currentPage, pageSize, sortConfig.sortBy, sortConfig.order),
        settingsRepository.getUnits(),
      ]);
      setServices(items);
      setTotalItems(total);
      setUnitsList(unitsData);
    } catch (error) {
      console.error("Erro ao buscar dados:", error);
    } finally {
      setLoading(false);
    }
  }, [currentPage, pageSize, sortConfig]);

  useEffect(() => {
    fetchServicesAndUnits();
  }, [fetchServicesAndUnits]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;

    if (name === "basePrice") {
      setFormData((prev) => ({ ...prev, [name]: parseFloat(value) || 0 }));
    } else if (name === "active") {
      setFormData((prev) => ({ ...prev, [name]: value === "true" }));
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleNewClick = () => {
    setFormData({
      name: "",
      description: "",
      unit: unitsList.length > 0 ? unitsList[0] : "Hectare",
      basePrice: 0,
      active: true,
    });
    setEditingId(null);
    setIsModalOpen(true);
  };

  const handleEditClick = (service: AgriculturalService) => {
    setFormData({
      name: service.name,
      description: service.description,
      unit: service.unit,
      basePrice: service.basePrice,
      active: service.active,
    });
    setEditingId(service.id);
    setIsModalOpen(true);
  };

  const handleDeleteClick = (service: AgriculturalService) => {
    setServiceToDelete(service);
    setIsDeleteModalOpen(true);
  };

  const confirmDelete = async () => {
    if (!serviceToDelete) return;

    setIsSubmitting(true);
    const success = await repository.deleteService(serviceToDelete.id);
    if (success) {
      await fetchServicesAndUnits();
      setIsDeleteModalOpen(false);
      setServiceToDelete(null);
    }
    setIsSubmitting(false);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    if (editingId) {
      await repository.updateService(editingId, formData as AgriculturalService);
    } else {
      await repository.addService(formData as Omit<AgriculturalService, "id">);
    }

    await fetchServicesAndUnits(); // Refresh list

    setIsSubmitting(false);
    setIsModalOpen(false);
    setEditingId(null);
  };

  const handleSort = (column: string) => {
    setSortConfig((prev) => ({
      sortBy: column,
      order: prev.sortBy === column && prev.order === "asc" ? "desc" : "asc",
    }));
    setCurrentPage(0); // Reset to first page when sorting
  };

  const totalPages = Math.ceil(totalItems / pageSize);

  const filteredServices = services.filter((s) =>
    s.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const columns = [
    { header: "Nome do Serviço", accessorKey: "name" },
    { header: "Descrição", accessorKey: "description" },
    { header: "Unidade", accessorKey: "unit" },
    {
      header: "Preço Base",
      accessorKey: "basePrice",
      cell: (item: AgriculturalService) => (
        <span className="font-mono text-gray-900">
          {new Intl.NumberFormat("pt-BR", {
            style: "currency",
            currency: "BRL",
          }).format(item.basePrice)}
        </span>
      ),
    },
    {
      header: "Status",
      accessorKey: "active",
      cell: (item: AgriculturalService) => (
        <span
          className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-bold uppercase tracking-wider ${item.active
              ? "bg-green-100 text-green-800 border border-green-300"
              : "bg-gray-200 text-gray-700 border border-gray-400"
            }`}
        >
          {item.active ? "Ativo" : "Inativo"}
        </span>
      ),
    },
    {
      header: "Ações",
      accessorKey: "actions",
      cell: (item: AgriculturalService) => (
        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={(e) => {
              e.stopPropagation();
              handleEditClick(item);
            }}
            className="h-8 w-8 p-0 text-blue-600 hover:text-blue-800 hover:bg-blue-50"
            title="Editar Serviço"
          >
            <Edit className="h-4 w-4" />
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={(e) => {
              e.stopPropagation();
              handleDeleteClick(item);
            }}
            className="h-8 w-8 p-0 text-red-600 hover:text-red-800 hover:bg-red-50"
            title="Excluir Serviço"
          >
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
      ),
    }
  ];

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-gray-300 pb-6">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-gray-900">Catálogo de Serviços</h1>
          <p className="text-lg text-gray-600 mt-2">Defina os tipos de serviços agrícolas oferecidos e seus valores base.</p>
        </div>
        <Button size="lg" className="shrink-0 gap-2" onClick={handleNewClick}>
          <Plus className="h-5 w-5" />
          Novo Serviço
        </Button>
      </div>

      <div className="flex items-center gap-4 bg-white p-4 rounded-lg border border-gray-300 shadow-sm">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-500" />
          <input
            type="text"
            placeholder="Buscar serviço por nome..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="h-12 w-full rounded-md border border-gray-300 pl-12 pr-4 text-base font-medium text-gray-900 placeholder-gray-500 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      {loading ? (
        <div className="flex h-64 items-center justify-center rounded-lg border border-gray-300 bg-white">
          <div className="text-xl font-bold text-gray-500 animate-pulse">Carregando serviços...</div>
        </div>
      ) : (
        <div className="space-y-4">
          <DataTable
            data={filteredServices}
            columns={columns}
            onSort={handleSort}
            sortConfig={sortConfig}
          />
          <Pagination
            currentPage={currentPage}
            totalPages={totalPages}
            onPageChange={setCurrentPage}
            className="bg-white p-4 rounded-lg border border-gray-300 shadow-sm"
          />
        </div>
      )}

      {/* Form Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={editingId ? "Editar Serviço" : "Cadastrar Novo Serviço"}
      >
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 gap-6">
            <div className="space-y-2">
              <label htmlFor="name" className="block text-sm font-bold text-gray-900">Nome do Serviço</label>
              <input
                id="name"
                name="name"
                type="text"
                required
                value={formData.name}
                onChange={handleInputChange}
                className="h-12 w-full rounded-md border border-gray-300 px-4 text-base font-medium text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Ex: Aração"
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="description" className="block text-sm font-bold text-gray-900">Descrição</label>
              <textarea
                id="description"
                name="description"
                required
                value={formData.description}
                onChange={handleInputChange}
                className="min-h-[100px] w-full rounded-md border border-gray-300 p-4 text-base font-medium text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-y"
                placeholder="Descreva os detalhes do serviço..."
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <label htmlFor="unit" className="block text-sm font-bold text-gray-900">Unidade de Medida</label>
                <select
                  id="unit"
                  name="unit"
                  value={formData.unit}
                  onChange={handleInputChange}
                  className="h-12 w-full rounded-md border border-gray-300 px-4 text-base font-medium text-gray-900 bg-white focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  {unitsList.length === 0 && <option value="Hectare">Hectare</option>}
                  {unitsList.map(unit => (
                    <option key={unit} value={unit}>{unit}</option>
                  ))}
                </select>
              </div>

              <div className="space-y-2">
                <label htmlFor="basePrice" className="block text-sm font-bold text-gray-900">Preço Base (R$)</label>
                <input
                  id="basePrice"
                  name="basePrice"
                  type="number"
                  step="0.01"
                  min="0"
                  required
                  value={formData.basePrice}
                  onChange={handleInputChange}
                  className="h-12 w-full rounded-md border border-gray-300 px-4 text-base font-medium text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="0.00"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label htmlFor="active" className="block text-sm font-bold text-gray-900">Status</label>
              <select
                id="active"
                name="active"
                value={formData.active ? "true" : "false"}
                onChange={handleInputChange}
                className="h-12 w-full rounded-md border border-gray-300 px-4 text-base font-medium text-gray-900 bg-white focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="true">Ativo</option>
                <option value="false">Inativo</option>
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
              {isSubmitting ? "Salvando..." : "Salvar Serviço"}
            </Button>
          </div>
        </form>
      </Modal>

      {/* Delete Confirmation Modal */}
      <Modal
        isOpen={isDeleteModalOpen}
        onClose={() => setIsDeleteModalOpen(false)}
        title="Confirmar Exclusão"
      >
        <div className="space-y-6">
          <div className="flex items-center gap-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-800">
            <AlertTriangle className="h-6 w-6 shrink-0" />
            <p className="text-sm font-medium">
              Tem certeza que deseja excluir o serviço <strong>{serviceToDelete?.name}</strong>?
              Esta ação não pode ser desfeita.
            </p>
          </div>

          <div className="flex justify-end gap-4">
            <Button
              variant="ghost"
              onClick={() => setIsDeleteModalOpen(false)}
              disabled={isSubmitting}
            >
              Cancelar
            </Button>
            <Button
              variant="default"
              className="bg-red-600 hover:bg-red-700 text-white"
              onClick={confirmDelete}
              disabled={isSubmitting}
            >
              {isSubmitting ? "Excluindo..." : "Confirmar Exclusão"}
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
