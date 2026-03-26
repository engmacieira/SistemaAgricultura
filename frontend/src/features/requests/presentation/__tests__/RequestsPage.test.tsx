import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { RequestsPage } from '../RequestsPage';
import { RequestRepository } from '../../data/RequestRepository';
import { ExecutionRepository } from '../../../executions/data/ExecutionRepository';
import { ProducerRepository } from '../../../producers/data/ProducerRepository';
import { ServiceRepository } from '../../../services/data/ServiceRepository';

// Mock Lucide icons
vi.mock('lucide-react', () => ({
    Plus: () => <div data-testid="icon-plus" />,
    CheckCircle: () => <div data-testid="icon-check-circle" />,
    Clock: () => <div data-testid="icon-clock" />,
    XCircle: () => <div data-testid="icon-x-circle" />,
    Play: () => <div data-testid="icon-play" />,
    AlertTriangle: () => <div data-testid="icon-alert-triangle" />,
    X: () => <div data-testid="icon-x" />,
}));

const {
    mockGetRequests,
    mockAddRequest,
    mockUpdateRequest,
    mockAddExecution,
    mockGetProducers,
    mockGetServices
} = vi.hoisted(() => {
    return {
        mockGetRequests: vi.fn().mockResolvedValue([]),
        mockAddRequest: vi.fn().mockResolvedValue({}),
        mockUpdateRequest: vi.fn().mockResolvedValue({}),
        mockAddExecution: vi.fn().mockResolvedValue({}),
        mockGetProducers: vi.fn().mockResolvedValue({ items: [] }),
        mockGetServices: vi.fn().mockResolvedValue({ items: [] }),
    };
});

vi.mock('../../data/RequestRepository', () => {
    return {
        RequestRepository: class {
            getRequests = mockGetRequests;
            addRequest = mockAddRequest;
            updateRequest = mockUpdateRequest;
        }
    };
});

vi.mock('../../../executions/data/ExecutionRepository', () => {
    return {
        ExecutionRepository: class {
            addExecution = mockAddExecution;
        }
    };
});

vi.mock('../../../producers/data/ProducerRepository', () => {
    return {
        ProducerRepository: class {
            getProducers = mockGetProducers;
        }
    };
});

vi.mock('../../../services/data/ServiceRepository', () => {
    return {
        ServiceRepository: class {
            getServices = mockGetServices;
        }
    };
});

describe('RequestsPage Integration', () => {
    beforeEach(() => {
        vi.clearAllMocks();

        // Setup default mocks
        mockGetProducers.mockResolvedValue({
            items: [{ id: 'prod1', name: 'João Produtor' }]
        });

        mockGetServices.mockResolvedValue({
            items: [{ id: 'serv1', name: 'Aração', unit: 'Horas', basePrice: 150 }]
        });

        mockGetRequests.mockImplementation((params: any) => {
            if (params?.status_filtro === 'EM_ANDAMENTO') {
                return Promise.resolve([
                    { id: 'req1', producerName: 'João Produtor', prioridade: 1, data_solicitacao: '2023-10-27T00:00:00.000Z', observacoes: '', status: 'EM_ANDAMENTO' }
                ]);
            }
            return Promise.resolve([]);
        });
    });

    it('submits "Dar Baixa" form and calculates total value correctly', async () => {
        // Render with "Em Andamento" tab
        render(<RequestsPage />);

        // Click "Em Andamento" tab to load those requests
        fireEvent.click(screen.getByText('Em Andamento'));

        // Let's first make sure the list renders by awaiting it
        await waitFor(() => {
            expect(screen.getByText('João Produtor')).toBeInTheDocument();
        });

        // Click "Dar Baixa no Serviço"
        await waitFor(() => {
             expect(screen.getByText('Dar Baixa no Serviço')).toBeInTheDocument();
        });
        fireEvent.click(screen.getByText('Dar Baixa no Serviço'));

        // Wait for modal to open
        await waitFor(() => {
            expect(screen.getByText('Qual serviço foi realizado?')).toBeInTheDocument();
        });

        // Fill form
        const selectElement = screen.getByRole('combobox');
        fireEvent.change(selectElement, { target: { value: 'serv1' } });
        fireEvent.change(screen.getByPlaceholderText(/Ex: João \/ Trator 01/i), { target: { value: 'Operador Teste' } });

        const quantityInputs = screen.getAllByRole('spinbutton');

        // Input [0] is Qtd.
        fireEvent.change(quantityInputs[0], { target: { value: '5' } });

        // Input [1] is Valor Unitario
        fireEvent.change(quantityInputs[1], { target: { value: '150' } });

        // Submit form
        fireEvent.click(screen.getByText('Confirmar e Gerar Pagamento'));

        // Verify ExecutionRepository.addExecution was called with correct totalValue
        await waitFor(() => {
            expect(mockAddExecution).toHaveBeenCalledWith(expect.objectContaining({
                solicitacaoId: 'req1',
                serviceId: 'serv1',
                serviceName: 'Aração',
                quantity: 5,
                unit: 'Horas',
                valor_unitario: 150,
                totalValue: 750, // 5 * 150
                operador_maquina: 'Operador Teste',
            }));
        });
    });
});
