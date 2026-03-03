import React, { useEffect, useState } from "react";
import { User } from "../../auth/domain/User";
import { userManagementRepository } from "../data/UserManagementRepository";
import { Button } from "../../../shared/components/Button";
import { DataTable } from "../../../shared/components/DataTable";
import { Modal } from "../../../shared/components/Modal";
import { Plus, Search, UserPlus, Edit, Trash2 } from "lucide-react";

export function UsersManagementPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);

  // Form State
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    role: "user" as "admin" | "user",
    password: "", // Apenas para novos usuários
  });

  const fetchUsers = async () => {
    setLoading(true);
    const data = await userManagementRepository.getUsers();
    setUsers(data);
    setLoading(false);
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleNewClick = () => {
    setFormData({
      name: "",
      email: "",
      role: "user",
      password: "",
    });
    setEditingId(null);
    setIsModalOpen(true);
  };

  const handleEditClick = (user: User) => {
    setFormData({
      name: user.name,
      email: user.email,
      role: user.role,
      password: "", // Não exibimos a senha
    });
    setEditingId(user.id);
    setIsModalOpen(true);
  };

  const handleDeleteClick = async (id: string) => {
    if (window.confirm("Tem certeza que deseja excluir este usuário?")) {
      await userManagementRepository.deleteUser(id);
      await fetchUsers();
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    if (editingId) {
      await userManagementRepository.updateUser(editingId, formData);
    } else {
      await userManagementRepository.addUser(formData);
    }
    
    await fetchUsers(); // Refresh list
    setIsSubmitting(false);
    setIsModalOpen(false);
    setEditingId(null);
  };

  const filteredUsers = users.filter((u) =>
    u.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    u.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const columns = [
    { header: "Nome", accessorKey: "name" },
    { header: "Email", accessorKey: "email" },
    {
      header: "Função",
      accessorKey: "role",
      cell: (item: User) => (
        <span
          className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-bold uppercase tracking-wider ${
            item.role === "admin"
              ? "bg-purple-100 text-purple-800 border border-purple-300"
              : "bg-blue-100 text-blue-800 border border-blue-300"
          }`}
        >
          {item.role === "admin" ? "Administrador" : "Usuário"}
        </span>
      ),
    },
    {
      header: "Ações",
      accessorKey: "actions",
      cell: (item: User) => (
        <div className="flex items-center gap-2">
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={(e) => {
              e.stopPropagation();
              handleEditClick(item);
            }}
            className="h-8 w-8 p-0 text-blue-600 hover:text-blue-800 hover:bg-blue-50"
            title="Editar Usuário"
          >
            <Edit className="h-4 w-4" />
          </Button>
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={(e) => {
              e.stopPropagation();
              handleDeleteClick(item.id);
            }}
            className="h-8 w-8 p-0 text-red-600 hover:text-red-800 hover:bg-red-50"
            title="Excluir Usuário"
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
          <h1 className="text-3xl font-extrabold tracking-tight text-gray-900">Gestão de Usuários</h1>
          <p className="text-lg text-gray-600 mt-2">Administre os usuários que têm acesso ao sistema.</p>
        </div>
        <Button size="lg" className="shrink-0 gap-2" onClick={handleNewClick}>
          <UserPlus className="h-5 w-5" />
          Novo Usuário
        </Button>
      </div>

      <div className="flex items-center gap-4 bg-white p-4 rounded-lg border border-gray-300 shadow-sm">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-500" />
          <input
            type="text"
            placeholder="Buscar por nome ou email..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="h-12 w-full rounded-md border border-gray-300 pl-12 pr-4 text-base font-medium text-gray-900 placeholder-gray-500 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      {loading ? (
        <div className="flex h-64 items-center justify-center rounded-lg border border-gray-300 bg-white">
          <div className="text-xl font-bold text-gray-500 animate-pulse">Carregando usuários...</div>
        </div>
      ) : (
        <DataTable data={filteredUsers} columns={columns} />
      )}

      <Modal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        title={editingId ? "Editar Usuário" : "Novo Usuário"}
      >
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-4">
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
              />
            </div>
            
            <div className="space-y-2">
              <label htmlFor="email" className="block text-sm font-bold text-gray-900">Email</label>
              <input
                id="email"
                name="email"
                type="email"
                required
                value={formData.email}
                onChange={handleInputChange}
                className="h-12 w-full rounded-md border border-gray-300 px-4 text-base font-medium text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="role" className="block text-sm font-bold text-gray-900">Função</label>
              <select
                id="role"
                name="role"
                value={formData.role}
                onChange={handleInputChange}
                className="h-12 w-full rounded-md border border-gray-300 px-4 text-base font-medium text-gray-900 bg-white focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="user">Usuário Comum</option>
                <option value="admin">Administrador (Master)</option>
              </select>
            </div>

            {!editingId && (
              <div className="space-y-2">
                <label htmlFor="password" className="block text-sm font-bold text-gray-900">Senha Inicial</label>
                <input
                  id="password"
                  name="password"
                  type="password"
                  required={!editingId}
                  value={formData.password}
                  onChange={handleInputChange}
                  className="h-12 w-full rounded-md border border-gray-300 px-4 text-base font-medium text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            )}
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
              {isSubmitting ? "Salvando..." : "Salvar Usuário"}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
