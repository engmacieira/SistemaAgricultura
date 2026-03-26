import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { LoginPage } from '../LoginPage';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from '../../../../core/context/AuthContext';
import { authRepository } from '../../data/AuthRepository';

// Mock Lucide icons to avoid rendering issues in JSDOM
vi.mock('lucide-react', () => ({
    Tractor: () => <div data-testid="icon-tractor" />,
    Lock: () => <div data-testid="icon-lock" />,
    Mail: () => <div data-testid="icon-mail" />,
    Loader2: () => <div data-testid="icon-loader" />,
    Users: () => <div data-testid="icon-users" />,
}));

// Mock useNavigate
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
    const actual = await vi.importActual('react-router-dom');
    return {
        ...actual,
        useNavigate: () => mockNavigate,
    };
});

// Mock AuthRepository to control login results
vi.mock('../../data/AuthRepository', () => ({
    authRepository: {
        login: vi.fn(),
        getPublicUsers: vi.fn().mockResolvedValue([]),
    },
}));

describe('LoginPage Integration', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        localStorage.clear();
    });

    const renderLoginPage = () => {
        return render(
            <AuthProvider>
                <BrowserRouter>
                    <LoginPage />
                </BrowserRouter>
            </AuthProvider>
        );
    };

    it('renders login form correctly', async () => {
        renderLoginPage();

        await waitFor(() => {
            expect(screen.getByLabelText(/selecione seu perfil/i)).toBeInTheDocument();
        });

        expect(screen.getByLabelText(/senha de acesso/i)).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /acessar painel/i })).toBeInTheDocument();
    });

    it('successfully logs in and navigates to dashboard using select', async () => {
        (authRepository.login as any).mockResolvedValue({
            user: { id: 1, email: 'admin@sistema.com', name: 'Admin' },
            access_token: 'fake-token',
        });
        (authRepository.getPublicUsers as any).mockResolvedValue([
            { name: 'Admin', email: 'admin@sistema.com' },
            { name: 'User', email: 'user@sistema.com' }
        ]);

        renderLoginPage();

        // Wait for users to load
        await waitFor(() => {
            expect(screen.getByLabelText(/selecione seu perfil/i)).toBeInTheDocument();
        });

        const selectElement = screen.getByLabelText(/selecione seu perfil/i);
        fireEvent.change(selectElement, { target: { value: 'admin@sistema.com' } });
        fireEvent.change(screen.getByLabelText(/senha de acesso/i), { target: { value: '123456' } });
        fireEvent.click(screen.getByRole('button', { name: /acessar painel/i }));

        await waitFor(() => {
            expect(authRepository.login).toHaveBeenCalledWith('admin@sistema.com', '123456');
            expect(mockNavigate).toHaveBeenCalledWith('/dashboard');
        });
    });

    it('shows error message on failed login using select', async () => {
        (authRepository.login as any).mockResolvedValue(null);
        (authRepository.getPublicUsers as any).mockResolvedValue([
            { name: 'Admin', email: 'admin@sistema.com' }
        ]);

        renderLoginPage();

        // Wait for users to load
        await waitFor(() => {
             expect(screen.getByLabelText(/selecione seu perfil/i)).toBeInTheDocument();
        });

        fireEvent.change(screen.getByLabelText(/selecione seu perfil/i), { target: { value: 'admin@sistema.com' } });
        fireEvent.change(screen.getByLabelText(/senha de acesso/i), { target: { value: 'wrongpass' } });
        fireEvent.click(screen.getByRole('button', { name: /acessar painel/i }));

        await waitFor(() => {
            expect(screen.getByText(/senha incorreta\./i)).toBeInTheDocument();
        });
    });
});
