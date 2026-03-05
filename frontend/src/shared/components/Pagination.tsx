import React from "react";
import { Button } from "./Button";
import { ChevronLeft, ChevronRight } from "lucide-react";

interface PaginationProps {
    currentPage: number;
    totalPages: number;
    onPageChange: (page: number) => void;
    className?: string;
}

export function Pagination({ currentPage, totalPages, onPageChange, className }: PaginationProps) {
    if (totalPages <= 1) return null;

    const pages = Array.from({ length: totalPages }, (_, i) => i);

    // Logic to show a limited number of page buttons around current page
    const maxVisiblePages = 5;
    let startPage = Math.max(0, currentPage - Math.floor(maxVisiblePages / 2));
    let endPage = Math.min(totalPages - 1, startPage + maxVisiblePages - 1);

    if (endPage - startPage + 1 < maxVisiblePages) {
        startPage = Math.max(0, endPage - maxVisiblePages + 1);
    }

    const visiblePages = pages.slice(startPage, endPage + 1);

    return (
        <div className={`flex items-center justify-between px-2 ${className}`}>
            <div className="flex-1 text-sm text-gray-700">
                Página <span className="font-bold text-gray-900">{currentPage + 1}</span> de{" "}
                <span className="font-bold text-gray-900">{totalPages}</span>
            </div>
            <div className="flex items-center space-x-2">
                <Button
                    variant="outline"
                    size="sm"
                    onClick={() => onPageChange(currentPage - 1)}
                    disabled={currentPage === 0}
                    className="h-8 w-8 p-0"
                >
                    <ChevronLeft className="h-4 w-4" />
                </Button>

                {startPage > 0 && (
                    <>
                        <Button
                            variant={currentPage === 0 ? "default" : "outline"}
                            size="sm"
                            onClick={() => onPageChange(0)}
                            className="h-8 w-8 p-0"
                        >
                            1
                        </Button>
                        {startPage > 1 && <span className="text-gray-400">...</span>}
                    </>
                )}

                {visiblePages.map((page) => (
                    <Button
                        key={page}
                        variant={currentPage === page ? "default" : "outline"}
                        size="sm"
                        onClick={() => onPageChange(page)}
                        className="h-8 w-8 p-0"
                    >
                        {page + 1}
                    </Button>
                ))}

                {endPage < totalPages - 1 && (
                    <>
                        {endPage < totalPages - 2 && <span className="text-gray-400">...</span>}
                        <Button
                            variant={currentPage === totalPages - 1 ? "default" : "outline"}
                            size="sm"
                            onClick={() => onPageChange(totalPages - 1)}
                            className="h-8 w-8 p-0"
                        >
                            {totalPages}
                        </Button>
                    </>
                )}

                <Button
                    variant="outline"
                    size="sm"
                    onClick={() => onPageChange(currentPage + 1)}
                    disabled={currentPage === totalPages - 1}
                    className="h-8 w-8 p-0"
                >
                    <ChevronRight className="h-4 w-4" />
                </Button>
            </div>
        </div>
    );
}
