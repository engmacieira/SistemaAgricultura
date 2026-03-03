import React from "react";
import { cn } from "../../core/utils";

interface Column<T> {
  header: string;
  accessorKey: keyof T | string;
  cell?: (item: T) => React.ReactNode;
}

interface DataTableProps<T> {
  data: T[];
  columns: Column<T>[];
  onRowClick?: (item: T) => void;
  className?: string;
}

export function DataTable<T>({ data, columns, onRowClick, className }: DataTableProps<T>) {
  return (
    <div className={cn("w-full overflow-auto rounded-lg border border-gray-300 bg-white shadow-sm", className)}>
      <table className="w-full caption-bottom text-sm">
        <thead className="bg-gray-100 border-b border-gray-300">
          <tr>
            {columns.map((col, index) => (
              <th
                key={index}
                className="h-14 px-6 text-left align-middle font-bold text-gray-900 uppercase tracking-wider"
              >
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {data.length === 0 ? (
            <tr>
              <td colSpan={columns.length} className="h-24 text-center text-gray-600 font-medium">
                Nenhum registro encontrado.
              </td>
            </tr>
          ) : (
            data.map((row, rowIndex) => (
              <tr
                key={rowIndex}
                onClick={() => onRowClick?.(row)}
                className={cn(
                  "transition-colors hover:bg-blue-50 data-[state=selected]:bg-gray-100",
                  onRowClick && "cursor-pointer"
                )}
              >
                {columns.map((col, colIndex) => (
                  <td key={colIndex} className="p-6 align-middle text-gray-800 font-medium">
                    {col.cell ? col.cell(row) : (row as any)[col.accessorKey]}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
