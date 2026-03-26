import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { RequestsPage } from '../RequestsPage';
import { RequestRepository } from '../../data/RequestRepository';
import { ExecutionRepository } from '../../../executions/data/ExecutionRepository';
import { ProducerRepository } from '../../../producers/data/ProducerRepository';
import { ServiceRepository } from '../../../services/data/ServiceRepository';
import { BrowserRouter } from 'react-router-dom';

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

const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
    const actual = await vi.importActual('react-router-dom');
    return {
        ...actual,
        useNavigate: () => mockNavigate,
    };
});

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

// Create a spy function for apiFetch throwing unauthorized errors
const mockFetchError = vi.fn().mockRejectedValue({ status: 401 });

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

describe('RequestsPage Session Security Test', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        localStorage.clear();

        // Setup default mocks for a valid session initially
        mockGetProducers.mockResolvedValue({
            items: [{ id: 'prod1', name: 'João Produtor' }]
        });

        mockGetServices.mockResolvedValue({
            items: [{ id: 'serv1', name: 'Aração', unit: 'Horas', basePrice: 150 }]
        });

        mockGetRequests.mockResolvedValue([
            { id: 'req1', producerName: 'João Produtor', prioridade: 1, data_solicitacao: '2023-10-27T00:00:00.000Z', observacoes: '', status: 'PENDENTE' }
        ]);
    });

    it('handles unauthorized API calls gracefully', async () => {
        // First render with a valid mock to load initial state
        render(
            <BrowserRouter>
                <RequestsPage />
            </BrowserRouter>
        );

        // Wait for data to load
        await waitFor(() => {
            expect(screen.getByText('João Produtor')).toBeInTheDocument();
        });

        // Simulate session expiration by making the repository throw an error
        // Note: The actual redirect logic might be in an Axios interceptor or
        // a global error handler. If it's not handled at the component level,
        // we can simulate the console.error for this specific component catch block.
        const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

        mockGetRequests.mockRejectedValueOnce(new Error("Unauthorized"));

        // Trigger a re-fetch by changing tabs
        fireEvent.click(screen.getByText('Em Andamento'));

        // Wait for the catch block to be hit
        await waitFor(() => {
            expect(consoleErrorSpy).toHaveBeenCalledWith("Erro ao buscar dados:", expect.any(Error));
        });

        consoleErrorSpy.mockRestore();
    });
});
