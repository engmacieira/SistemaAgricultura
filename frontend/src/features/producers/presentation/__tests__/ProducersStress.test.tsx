import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { ProducersPage } from '../ProducersPage';
import { ProducerRepository } from '../../data/ProducerRepository';
import { Producer } from '../../domain/Producer';

// Mock Lucide icons
vi.mock('lucide-react', () => ({
    Search: () => <div data-testid="icon-search" />,
    Plus: () => <div data-testid="icon-plus" />,
    UserPlus: () => <div data-testid="icon-user-plus" />,
    Edit: () => <div data-testid="icon-edit" />,
    Trash2: () => <div data-testid="icon-trash" />,
    ArrowUp: () => <div data-testid="icon-arrow-up" />,
    ArrowDown: () => <div data-testid="icon-arrow-down" />,
}));

describe('ProducersPage Stress Tests', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    // Helper to generate a large mocked dataset
    const generateLargeDataset = (count: number): Producer[] => {
        return Array.from({ length: count }).map((_, i) => ({
            id: `prod-${i}`,
            name: `Produtor Stress ${i}`,
            cpfCnpj: `000.000.000-${i.toString().padStart(2, '0')}`,
            property: `Fazenda ${i}`,
            regiao_referencia: `Região ${i % 10}`,
            telefone_contato: `(00) 00000-${i.toString().padStart(4, '0')}`,
            apelido_produtor: `Apelido ${i}`,
            status: i % 10 === 0 ? 'Inativo' : 'Ativo',
            is_deleted: false,
        }));
    };

    it('renders correctly with a large dataset (100 items)', async () => {
        const LARGE_COUNT = 100;
        const largeData = generateLargeDataset(LARGE_COUNT);

        // Use spyOn instead of vi.mock for class prototypes
        const getProducersSpy = vi.spyOn(ProducerRepository.prototype, 'getProducers')
            .mockResolvedValue({
                items: largeData,
                total: 10000,
                pages: 100
            });

        const startTime = performance.now();

        render(<ProducersPage />);

        // Wait for the loading state to disappear
        await waitFor(() => {
            expect(screen.queryByText(/carregando produtores/i)).not.toBeInTheDocument();
        }, { timeout: 3000 });

        const rowRenderTime = performance.now() - startTime;

        expect(screen.getByText('Produtor Stress 0')).toBeInTheDocument();
        expect(screen.getByText(`Produtor Stress ${LARGE_COUNT - 1}`)).toBeInTheDocument();

        // Assert rendering performance (< 1500ms is generous for 100 rows in JSDOM)
        expect(rowRenderTime).toBeLessThan(1500);

        getProducersSpy.mockRestore();
    });

    it('handles rapid user interactions (typing search, clicking sort, clicking pagination)', async () => {
        const normalData = generateLargeDataset(10);

        const getProducersSpy = vi.spyOn(ProducerRepository.prototype, 'getProducers')
            .mockResolvedValue({
                items: normalData,
                total: 50,
                pages: 5
            });

        render(<ProducersPage />);

        // Wait for initial load
        await waitFor(() => {
            expect(screen.queryByText(/carregando produtores/i)).not.toBeInTheDocument();
        });

        const searchInput = screen.getByPlaceholderText(/buscar por nome/i);
        const sortButtonNome = screen.getByText('Nome');
        const nextButton = screen.getByRole('button', { name: /próximo/i });

        // Simulate rapid interactions
        await act(async () => {
            // Rapid typing
            fireEvent.change(searchInput, { target: { value: 'S' } });
            fireEvent.change(searchInput, { target: { value: 'St' } });
            fireEvent.change(searchInput, { target: { value: 'Str' } });

            // Rapid sorting
            fireEvent.click(sortButtonNome);
            fireEvent.click(sortButtonNome);

            // Rapid paging
            fireEvent.click(nextButton);
            fireEvent.click(nextButton);
        });

        // Validations to ensure UI didn't break and state updated
        expect(screen.getByDisplayValue('Str')).toBeInTheDocument();

        await waitFor(() => {
            const activePageButton = screen.getByRole('button', { name: '3' });
            expect(activePageButton).toHaveClass('bg-blue-800'); // active variant
        });

        getProducersSpy.mockRestore();
    });
});
