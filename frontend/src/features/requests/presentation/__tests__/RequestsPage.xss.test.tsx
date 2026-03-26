import { render, screen, waitFor } from '@testing-library/react';
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

describe('RequestsPage XSS Vulnerability Test', () => {
    beforeEach(() => {
        vi.clearAllMocks();

        // Setup default mocks
        mockGetProducers.mockResolvedValue({
            items: [{ id: 'prod1', name: 'João Produtor' }]
        });

        mockGetServices.mockResolvedValue({
            items: [{ id: 'serv1', name: 'Aração', unit: 'Horas', basePrice: 150 }]
        });

        const xssPayload = "<script>alert('XSS')</script><img src='x' onerror='alert(\"XSS\")'>";

        mockGetRequests.mockImplementation((params: any) => {
            return Promise.resolve([
                {
                    id: 'req1',
                    producerName: `João Produtor ${xssPayload}`,
                    prioridade: 1,
                    data_solicitacao: '2023-10-27T00:00:00.000Z',
                    observacoes: `Observação perigosa: ${xssPayload}`,
                    status: params?.status_filtro || 'PENDENTE'
                }
            ]);
        });
    });

    it('escapes XSS payloads in request display properly', async () => {
        render(<RequestsPage />);

        // Wait for data to load
        await waitFor(() => {
            // Check if the script tags are rendered as text content rather than executed
            expect(screen.getByText(/João Produtor <script>alert\('XSS'\)<\/script>/i)).toBeInTheDocument();
            expect(screen.getByText(/Observação perigosa: <script>alert\('XSS'\)<\/script>/i)).toBeInTheDocument();
        });

        // Ensure no unexpected elements are injected
        const scripts = document.querySelectorAll('script');

        // We might have some scripts injected by the test runner itself, but we shouldn't have the one we injected
        // Just as an extra precaution, check that our specific payload isn't in the innerHTML of any script.
        scripts.forEach(script => {
             expect(script.innerHTML).not.toContain("alert('XSS')");
        });

        // Ensure no broken images from our payload
        const images = document.querySelectorAll('img');
        images.forEach(img => {
            expect(img.getAttribute('src')).not.toBe('x');
        });
    });
});
