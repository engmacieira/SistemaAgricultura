import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { Modal } from '../Modal';

describe('Modal', () => {
    const defaultProps = {
        isOpen: true,
        onClose: vi.fn(),
        title: 'Test Modal',
    };

    it('renders when isOpen is true', () => {
        render(
            <Modal {...defaultProps}>
                <div data-testid="modal-content">Modal Content</div>
            </Modal>
        );
        expect(screen.getByText('Test Modal')).toBeInTheDocument();
        expect(screen.getByTestId('modal-content')).toBeInTheDocument();
    });

    it('does not render when isOpen is false', () => {
        render(
            <Modal {...defaultProps} isOpen={false}>
                <div>Modal Content</div>
            </Modal>
        );
        expect(screen.queryByText('Test Modal')).not.toBeInTheDocument();
    });

    it('calls onClose when close button is clicked', () => {
        render(
            <Modal {...defaultProps}>
                <div>Content</div>
            </Modal>
        );
        const closeButton = screen.getByLabelText('Fechar modal');
        fireEvent.click(closeButton);
        expect(defaultProps.onClose).toHaveBeenCalledTimes(1);
    });

    it('renders children correctly', () => {
        render(
            <Modal {...defaultProps}>
                <p>Child Element</p>
            </Modal>
        );
        expect(screen.getByText('Child Element')).toBeInTheDocument();
    });
});
