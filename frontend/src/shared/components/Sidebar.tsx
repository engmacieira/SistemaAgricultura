import React from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { cn } from "../../core/utils";
import { Users, Tractor, Calendar, ClipboardList, DollarSign, FileText, Settings, LogOut, User, ShieldAlert, UserCog, LayoutDashboard } from "lucide-react";
import { useAuth } from "../../core/context/AuthContext";

const navItems = [
  { name: "Dashboard", path: "/dashboard", icon: LayoutDashboard },
  { name: "Produtores", path: "/produtores", icon: Users },
  { name: "Serviços", path: "/servicos", icon: Tractor },
  { name: "Agendamentos", path: "/agendamentos", icon: Calendar },
  { name: "Execuções", path: "/execucoes", icon: ClipboardList },
  { name: "Pagamentos", path: "/pagamentos", icon: DollarSign },
  { name: "Relatórios", path: "/relatorios", icon: FileText },
];

export function Sidebar() {
  const location = useLocation();
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate("/login");
  };

  return (
    <aside className="fixed inset-y-0 left-0 z-10 w-64 flex-col border-r border-gray-300 bg-gray-900 text-white hidden md:flex">
      <div className="flex h-20 items-center justify-center border-b border-gray-800 px-6">
        <h1 className="text-xl font-bold tracking-tight text-white uppercase flex items-center gap-3">
          <Tractor className="h-8 w-8 text-blue-400" />
          Serviços Agrícolas
        </h1>
      </div>

      <div className="px-4 py-4 border-b border-gray-800">
        <div className="flex items-center gap-3 px-2">
          <div className="h-10 w-10 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold">
            {user?.name.charAt(0).toUpperCase()}
          </div>
          <div className="overflow-hidden">
            <p className="text-sm font-bold truncate">{user?.name}</p>
            <p className="text-xs text-gray-400 truncate">{user?.role === 'admin' ? 'Administrador' : 'Usuário'}</p>
          </div>
        </div>
        <Link
          to="/perfil"
          className={cn(
            "mt-3 flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm font-medium transition-all hover:bg-gray-800 hover:text-white",
            location.pathname === "/perfil" ? "bg-gray-800 text-white" : "text-gray-400"
          )}
        >
          <User className="h-4 w-4" />
          Meu Perfil
        </Link>
      </div>

      <nav className="flex-1 overflow-y-auto py-6 px-4 space-y-2">
        {navItems.map((item) => {
          const isActive = location.pathname.startsWith(item.path);
          return (
            <Link
              key={item.name}
              to={item.path}
              className={cn(
                "flex items-center gap-4 rounded-lg px-4 py-4 text-base font-bold transition-all hover:bg-gray-800 hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500",
                isActive ? "bg-blue-800 text-white shadow-md" : "text-gray-300"
              )}
            >
              <item.icon className="h-6 w-6" />
              {item.name}
            </Link>
          );
        })}

        {user?.role === 'admin' && (
          <>
            <div className="pt-4 pb-2 px-2 text-xs font-bold text-gray-500 uppercase tracking-wider">
              Administração
            </div>
            <Link
              to="/usuarios"
              className={cn(
                "flex items-center gap-4 rounded-lg px-4 py-4 text-base font-bold transition-all hover:bg-gray-800 hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500",
                location.pathname.startsWith("/usuarios") ? "bg-purple-900 text-white shadow-md" : "text-gray-300"
              )}
            >
              <UserCog className="h-6 w-6 text-purple-400" />
              Usuários
            </Link>
            <Link
              to="/logs"
              className={cn(
                "flex items-center gap-4 rounded-lg px-4 py-4 text-base font-bold transition-all hover:bg-gray-800 hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500",
                location.pathname.startsWith("/logs") ? "bg-purple-900 text-white shadow-md" : "text-gray-300"
              )}
            >
              <ShieldAlert className="h-6 w-6 text-purple-400" />
              Logs do Sistema
            </Link>
          </>
        )}
      </nav>

      <div className="border-t border-gray-800 p-4 space-y-2">
        <Link
          to="/configuracoes"
          className={cn(
            "flex w-full items-center gap-4 rounded-lg px-4 py-4 text-base font-bold transition-all hover:bg-gray-800 hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500",
            location.pathname.startsWith("/configuracoes") ? "bg-blue-800 text-white shadow-md" : "text-gray-300"
          )}
        >
          <Settings className="h-6 w-6" />
          Configurações
        </Link>
        <button
          onClick={handleLogout}
          className="flex w-full items-center gap-4 rounded-lg px-4 py-4 text-base font-bold text-red-400 transition-all hover:bg-red-900/20 hover:text-red-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-red-500"
        >
          <LogOut className="h-6 w-6" />
          Sair do Sistema
        </button>
      </div>
    </aside>
  );
}
