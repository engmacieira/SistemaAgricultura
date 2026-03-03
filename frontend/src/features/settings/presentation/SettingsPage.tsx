import React, { useEffect, useState } from "react";
import { settingsRepository } from "../data/SettingsRepository";
import { Button } from "../../../shared/components/Button";
import { Database, Download, Upload, Trash2, Plus, Settings2 } from "lucide-react";

export function SettingsPage() {
  const [units, setUnits] = useState<string[]>([]);
  const [newUnit, setNewUnit] = useState("");
  const [loading, setLoading] = useState(true);
  
  const [isBackingUp, setIsBackingUp] = useState(false);
  const [isRestoring, setIsRestoring] = useState(false);
  const [message, setMessage] = useState<{ text: string; type: "success" | "error" } | null>(null);

  useEffect(() => {
    const fetchSettings = async () => {
      setLoading(true);
      const data = await settingsRepository.getUnits();
      setUnits(data);
      setLoading(false);
    };
    fetchSettings();
  }, []);

  const handleAddUnit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newUnit.trim()) return;
    
    const updatedUnits = await settingsRepository.addUnit(newUnit);
    setUnits(updatedUnits);
    setNewUnit("");
    showMessage("Unidade adicionada com sucesso!", "success");
  };

  const handleRemoveUnit = async (unit: string) => {
    const updatedUnits = await settingsRepository.removeUnit(unit);
    setUnits(updatedUnits);
    showMessage(`Unidade "${unit}" removida com sucesso!`, "success");
  };

  const handleBackup = async () => {
    setIsBackingUp(true);
    await settingsRepository.performBackup();
    setIsBackingUp(false);
    showMessage("Backup do banco de dados realizado com sucesso!", "success");
  };

  const handleRestore = async () => {
    if (!window.confirm("Atenção: Restaurar um backup irá sobrescrever todos os dados atuais. Deseja continuar?")) {
      return;
    }
    setIsRestoring(true);
    await settingsRepository.performRestore();
    setIsRestoring(false);
    showMessage("Banco de dados restaurado com sucesso!", "success");
  };

  const showMessage = (text: string, type: "success" | "error") => {
    setMessage({ text, type });
    setTimeout(() => setMessage(null), 4000);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-gray-300 pb-6">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-gray-900">Configurações do Sistema</h1>
          <p className="text-lg text-gray-600 mt-2">Gerencie parâmetros globais e a segurança dos dados.</p>
        </div>
      </div>

      {message && (
        <div className={`p-4 rounded-md font-bold text-sm ${
          message.type === "success" ? "bg-green-100 text-green-800 border border-green-300" : "bg-red-100 text-red-800 border border-red-300"
        }`}>
          {message.text}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Parâmetros do Sistema */}
        <div className="bg-white rounded-lg border border-gray-300 shadow-sm overflow-hidden">
          <div className="border-b border-gray-200 bg-gray-50 px-6 py-4 flex items-center gap-3">
            <Settings2 className="h-6 w-6 text-gray-700" />
            <h2 className="text-xl font-bold text-gray-900">Parâmetros do Sistema</h2>
          </div>
          
          <div className="p-6 space-y-6">
            <div>
              <h3 className="text-base font-bold text-gray-900 mb-4">Unidades de Medida (Serviços)</h3>
              
              <form onSubmit={handleAddUnit} className="flex gap-4 mb-6">
                <input
                  type="text"
                  value={newUnit}
                  onChange={(e) => setNewUnit(e.target.value)}
                  placeholder="Nova unidade (ex: Saca)"
                  className="h-12 flex-1 rounded-md border border-gray-300 px-4 text-base font-medium text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <Button type="submit" className="shrink-0 gap-2">
                  <Plus className="h-5 w-5" />
                  Adicionar
                </Button>
              </form>

              {loading ? (
                <div className="h-32 flex items-center justify-center text-gray-500 font-bold animate-pulse">
                  Carregando unidades...
                </div>
              ) : (
                <div className="border border-gray-200 rounded-md divide-y divide-gray-200">
                  {units.map((unit) => (
                    <div key={unit} className="flex items-center justify-between p-4 hover:bg-gray-50 transition-colors">
                      <span className="font-medium text-gray-900">{unit}</span>
                      <Button 
                        variant="ghost" 
                        size="sm" 
                        onClick={() => handleRemoveUnit(unit)}
                        className="text-red-600 hover:text-red-800 hover:bg-red-50 h-10 w-10 p-0"
                        title="Remover unidade"
                      >
                        <Trash2 className="h-5 w-5" />
                      </Button>
                    </div>
                  ))}
                  {units.length === 0 && (
                    <div className="p-4 text-center text-gray-500">Nenhuma unidade cadastrada.</div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Banco de Dados e Segurança */}
        <div className="bg-white rounded-lg border border-gray-300 shadow-sm overflow-hidden h-fit">
          <div className="border-b border-gray-200 bg-gray-50 px-6 py-4 flex items-center gap-3">
            <Database className="h-6 w-6 text-gray-700" />
            <h2 className="text-xl font-bold text-gray-900">Banco de Dados e Segurança</h2>
          </div>
          
          <div className="p-6 space-y-6">
            <p className="text-gray-600">
              Realize cópias de segurança regularmente para evitar perda de informações importantes.
            </p>
            
            <div className="flex flex-col gap-4">
              <Button 
                size="lg" 
                className="w-full justify-start gap-4" 
                onClick={handleBackup}
                disabled={isBackingUp || isRestoring}
              >
                <Download className="h-6 w-6" />
                {isBackingUp ? "Gerando arquivo de backup..." : "Fazer Backup do Sistema"}
              </Button>
              
              <Button 
                variant="secondary" 
                size="lg" 
                className="w-full justify-start gap-4"
                onClick={handleRestore}
                disabled={isBackingUp || isRestoring}
              >
                <Upload className="h-6 w-6" />
                {isRestoring ? "Restaurando dados..." : "Restaurar Backup"}
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
