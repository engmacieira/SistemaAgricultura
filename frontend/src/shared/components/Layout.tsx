import React from "react";
import { Outlet } from "react-router-dom";
import { Sidebar } from "./Sidebar";

export function Layout() {
  return (
    <div className="flex min-h-screen w-full bg-gray-50 text-gray-900 font-sans">
      <Sidebar />
      <main className="flex-1 md:ml-64 p-8 lg:p-12 overflow-y-auto">
        <div className="mx-auto max-w-7xl">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
