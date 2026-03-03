import React, { useState } from "react";
import { useAuth } from "../../../core/context/AuthContext";
import { Button } from "../../../shared/components/Button";
import { User, Lock, Save } from "lucide-react";

export function UserProfilePage() {
  const { user } = useAuth();
  const [formData, setFormData] = useState({
    name: user?.name || "",
    email: user?.email || "",
    currentPassword: "",
    newPassword: "",
    confirmPassword: "",
  });
  const [isSaving, setIsSaving] = useState(false);
  const [message, setMessage] = useState<{ text: string; type: "success" | "error" } | null>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    setMessage(null);

    // Simulação de validação e salvamento
    setTimeout(() => {
      if (formData.newPassword && formData.newPassword !== formData.confirmPassword) {
        setMessage({ text: "As senhas não conferem.", type: "error" });
        setIsSaving(false);
        return;
      }

      setMessage({ text: "Perfil atualizado com sucesso!", type: "success" });
      setIsSaving(false);
      setFormData((prev) => ({ ...prev, currentPassword: "", newPassword: "", confirmPassword: "" }));
    }, 1000);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-500 max-w-4xl mx-auto">
      <div className="border-b border-gray-300 pb-6">
        <h1 className="text-3xl font-extrabold tracking-tight text-gray-900">Meu Perfil</h1>
        <p className="text-lg text-gray-600 mt-2">Gerencie suas informações pessoais e de acesso.</p>
      </div>

      {message && (
        <div className={`p-4 rounded-md font-bold text-sm ${
          message.type === "success" ? "bg-green-100 text-green-800 border border-green-300" : "bg-red-100 text-red-800 border border-red-300"
        }`}>
          {message.text}
        </div>
      )}

      <div className="bg-white rounded-lg border border-gray-300 shadow-sm overflow-hidden">
        <div className="border-b border-gray-200 bg-gray-50 px-6 py-4 flex items-center gap-3">
          <User className="h-6 w-6 text-gray-700" />
          <h2 className="text-xl font-bold text-gray-900">Dados Pessoais</h2>
        </div>
        
        <form onSubmit={handleSubmit} className="p-6 space-y-6">
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
              />
            </div>
            
            <div className="space-y-2">
              <label htmlFor="email" className="block text-sm font-bold text-gray-900">Email</label>
              <input
                id="email"
                name="email"
                type="email"
                required
                disabled
                value={formData.email}
                className="h-12 w-full rounded-md border border-gray-300 px-4 text-base font-medium text-gray-500 bg-gray-100 cursor-not-allowed"
              />
              <p className="text-xs text-gray-500">O email não pode ser alterado.</p>
            </div>
          </div>

          <div className="border-t border-gray-200 pt-6 mt-6">
            <div className="flex items-center gap-3 mb-6">
              <Lock className="h-5 w-5 text-gray-700" />
              <h3 className="text-lg font-bold text-gray-900">Alterar Senha</h3>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="space-y-2">
                <label htmlFor="currentPassword" className="block text-sm font-bold text-gray-900">Senha Atual</label>
                <input
                  id="currentPassword"
                  name="currentPassword"
                  type="password"
                  value={formData.currentPassword}
                  onChange={handleInputChange}
                  className="h-12 w-full rounded-md border border-gray-300 px-4 text-base font-medium text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div className="space-y-2">
                <label htmlFor="newPassword" className="block text-sm font-bold text-gray-900">Nova Senha</label>
                <input
                  id="newPassword"
                  name="newPassword"
                  type="password"
                  value={formData.newPassword}
                  onChange={handleInputChange}
                  className="h-12 w-full rounded-md border border-gray-300 px-4 text-base font-medium text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div className="space-y-2">
                <label htmlFor="confirmPassword" className="block text-sm font-bold text-gray-900">Confirmar Nova Senha</label>
                <input
                  id="confirmPassword"
                  name="confirmPassword"
                  type="password"
                  value={formData.confirmPassword}
                  onChange={handleInputChange}
                  className="h-12 w-full rounded-md border border-gray-300 px-4 text-base font-medium text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
          </div>

          <div className="flex justify-end pt-6">
            <Button type="submit" size="lg" disabled={isSaving} className="gap-2">
              <Save className="h-5 w-5" />
              {isSaving ? "Salvando..." : "Salvar Alterações"}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
