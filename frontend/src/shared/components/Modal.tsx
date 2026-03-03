import React from "react";
import { X } from "lucide-react";
import { cn } from "../../core/utils";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  className?: string;
}

export function Modal({ isOpen, onClose, title, children, className }: ModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4 animate-in fade-in duration-200">
      <div 
        className={cn(
          "bg-white rounded-lg shadow-xl w-full max-w-2xl flex flex-col max-h-[90vh] animate-in zoom-in-95 duration-200", 
          className
        )}
      >
        <div className="flex items-center justify-between border-b border-gray-300 px-6 py-4">
          <h2 className="text-xl font-bold text-gray-900">{title}</h2>
          <button 
            onClick={onClose} 
            className="text-gray-500 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-md p-1 transition-colors"
            aria-label="Fechar modal"
          >
            <X className="h-6 w-6" />
          </button>
        </div>
        <div className="p-6 overflow-y-auto flex-1">
          {children}
        </div>
      </div>
    </div>
  );
}
