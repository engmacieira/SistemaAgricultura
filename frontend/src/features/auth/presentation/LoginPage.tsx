import React, { useState, useEffect } from "react";
import { useAuth } from "../../../core/context/AuthContext";
import { useNavigate } from "react-router-dom";
import { Tractor, Lock, Users, Loader2 } from "lucide-react"; // Troquei Mail por Users
import { Button } from "../../../shared/components/Button";
import { authRepository } from "../data/AuthRepository"; // Importamos o repositório

export function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // ✅ NOVOS ESTADOS PARA O SELECT
  const [usuariosLista, setUsuariosLista] = useState<{ name: string, email: string }[]>([]);
  const [loadingUsers, setLoadingUsers] = useState(true);

  // ✅ BUSCA OS USUÁRIOS AO ABRIR A TELA
  useEffect(() => {
    const fetchUsuarios = async () => {
      const lista = await authRepository.getPublicUsers();
      setUsuariosLista(lista);
      if (lista.length > 0) {
        setEmail(lista[0].email); // Já deixa o primeiro selecionado
      }
      setLoadingUsers(false);
    };
    fetchUsuarios();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const success = await login(email, password);
      if (success) {
        navigate("/dashboard");
      } else {
        setError("Senha incorreta."); // Ajustei a mensagem, já que o usuário é fixo
      }
    } catch (err) {
      setError("Sistema temporariamente indisponível. Tente mais tarde.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#f8fafc] p-4">
      <div className="w-full max-w-md space-y-8 rounded-2xl bg-white p-10 shadow-xl border border-gray-100">

        <div className="flex flex-col items-center text-center">
          <div className="rounded-2xl bg-blue-600 p-4 mb-6 shadow-lg shadow-blue-100">
            <Tractor className="h-10 w-10 text-white" />
          </div>
          <h2 className="text-3xl font-bold tracking-tight text-gray-900">
            AgroGestão PRO
          </h2>
          <p className="mt-3 text-base text-gray-500">
            Acesse sua conta para gerenciar sua produção
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="space-y-5">
            {/* ✅ CAMPO DE E-MAIL TRANSFORMADO EM SELECT */}
            <div>
              <label htmlFor="email" className="block text-sm font-semibold text-gray-700 ml-1">
                Selecione seu Perfil
              </label>
              <div className="relative mt-1.5">
                <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                  <Users className="h-5 w-5 text-gray-400" />
                </div>
                {loadingUsers ? (
                  <div className="block w-full rounded-xl border border-gray-200 pl-10 py-3.5 bg-gray-50 text-gray-500 sm:text-sm animate-pulse">
                    Carregando perfis...
                  </div>
                ) : (
                  <select
                    id="email"
                    name="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="block w-full rounded-xl border border-gray-200 pl-10 py-3.5 text-gray-900 transition-all focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 sm:text-sm appearance-none bg-white"
                  >
                    <option value="" disabled>Selecione quem você é...</option>
                    {usuariosLista.map((user, idx) => (
                      <option key={idx} value={user.email}>
                        {user.name}
                      </option>
                    ))}
                  </select>
                )}
              </div>
            </div>

            {/* CAMPO DE SENHA INTACTO */}
            <div>
              <label htmlFor="password" className="block text-sm font-semibold text-gray-700 ml-1">
                Senha de Acesso
              </label>
              <div className="relative mt-1.5">
                <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                  <Lock className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="password"
                  name="password"
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="block w-full rounded-xl border border-gray-200 pl-10 py-3.5 text-gray-900 transition-all focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 sm:text-sm"
                  placeholder="••••••••"
                />
              </div>
            </div>
          </div>

          {error && (
            <div className="rounded-xl bg-red-50 p-4 text-sm font-medium text-red-600 border border-red-100 flex items-center gap-2">
              <span className="h-1.5 w-1.5 rounded-full bg-red-600" />
              {error}
            </div>
          )}

          <Button
            type="submit"
            className="w-full justify-center py-4 text-lg font-bold bg-blue-600 hover:bg-blue-700 rounded-xl transition-all shadow-lg shadow-blue-100"
            disabled={loading || loadingUsers || !email}
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                Autenticando...
              </>
            ) : (
              "Acessar Painel"
            )}
          </Button>
        </form>

        <div className="mt-8 text-center">
          <p className="text-sm text-gray-400">
            &copy; {new Date().getFullYear()} AgroGestão Sistemas.
          </p>
        </div>
      </div>
    </div>
  );
}