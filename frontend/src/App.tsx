/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Layout } from "./shared/components/Layout";
import { ProducersPage } from "./features/producers/presentation/ProducersPage";
import { ServicesPage } from "./features/services/presentation/ServicesPage";
import { ExecutionsPage } from "./features/executions/presentation/ExecutionsPage";
import { RequestsPage } from "./features/requests/presentation/RequestsPage";
import { PaymentsPage } from "./features/payments/presentation/PaymentsPage";
import { ReportsPage } from "./features/reports/presentation/ReportsPage";
import { SettingsPage } from "./features/settings/presentation/SettingsPage";
import { LoginPage } from "./features/auth/presentation/LoginPage";
import { UserProfilePage } from "./features/auth/presentation/UserProfilePage";
import { UsersManagementPage } from "./features/admin/presentation/UsersManagementPage";
import { SystemLogsPage } from "./features/admin/presentation/SystemLogsPage";
import { DashboardPage } from "./features/dashboard/presentation/DashboardPage";
import { AuthProvider } from "./core/context/AuthContext";
import { ProtectedRoute } from "./core/auth/ProtectedRoute";

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />

          <Route path="/" element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }>
            <Route index element={<DashboardPage />} />
            <Route path="dashboard" element={<DashboardPage />} />
            <Route path="produtores" element={<ProducersPage />} />
            <Route path="servicos" element={<ServicesPage />} />
            <Route path="agendamentos" element={<RequestsPage />} />
            <Route path="execucoes" element={<ExecutionsPage />} />
            <Route path="pagamentos" element={<PaymentsPage />} />
            <Route path="relatorios" element={<ReportsPage />} />
            <Route path="configuracoes" element={<SettingsPage />} />
            <Route path="perfil" element={<UserProfilePage />} />
            <Route path="usuarios" element={<UsersManagementPage />} />
            <Route path="logs" element={<SystemLogsPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
