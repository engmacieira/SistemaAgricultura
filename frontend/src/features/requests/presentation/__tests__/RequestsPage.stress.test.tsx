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
        mockAddExecution: vi.fn().mockImplementation(() => new Promise(resolve => setTimeout(() => resolve({}), 100))), // Simulate network delay
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

describe('RequestsPage UI Stress Test', () => {
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

    it('prevents multiple submissions when "Confirmar e Gerar Pagamento" is clicked rapidly', async () => {
        render(<RequestsPage />);

        // Click "Em Andamento" tab to load those requests
        fireEvent.click(screen.getByText('Em Andamento'));

        // Wait for data to load
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

        // Fill form to make it valid
        const selectElement = screen.getByRole('combobox');
        fireEvent.change(selectElement, { target: { value: 'serv1' } });

        const quantityInputs = screen.getAllByRole('spinbutton');
        fireEvent.change(quantityInputs[0], { target: { value: '5' } });
        fireEvent.change(quantityInputs[1], { target: { value: '150' } });

        // Submit form rapidly 20 times
        const submitButton = screen.getByText('Confirmar e Gerar Pagamento');

        for (let i = 0; i < 20; i++) {
            fireEvent.click(submitButton);
        }

        // Wait for the modal to close or the status to change
        await waitFor(() => {
            expect(mockAddExecution).toHaveBeenCalledTimes(1);
        });
    });
});
