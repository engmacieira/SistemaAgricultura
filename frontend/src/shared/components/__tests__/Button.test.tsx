import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { Button } from '../Button';

describe('Button', () => {
    it('renders correctly with default props', () => {
        render(<Button>Click me</Button>);
        const button = screen.getByRole('button', { name: /click me/i });
        expect(button).toBeInTheDocument();
        expect(button).toHaveClass('bg-blue-800'); // primary variant
    });

    it('renders with different variants', () => {
        const { rerender } = render(<Button variant="danger">Delete</Button>);
        let button = screen.getByRole('button', { name: /delete/i });
        expect(button).toHaveClass('bg-red-700');

        rerender(<Button variant="secondary">Cancel</Button>);
        button = screen.getByRole('button', { name: /cancel/i });
        expect(button).toHaveClass('bg-gray-200');
    });

    it('renders with different sizes', () => {
        const { rerender } = render(<Button size="sm">Small</Button>);
        let button = screen.getByRole('button', { name: /small/i });
        expect(button).toHaveClass('h-10');

        rerender(<Button size="lg">Large</Button>);
        button = screen.getByRole('button', { name: /large/i });
        expect(button).toHaveClass('h-14');
    });

    it('calls onClick handler when clicked', () => {
        const handleClick = vi.fn();
        render(<Button onClick={handleClick}>Click me</Button>);
        const button = screen.getByRole('button', { name: /click me/i });
        fireEvent.click(button);
        expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it('is disabled when disabled prop is true', () => {
        render(<Button disabled>Disabled</Button>);
        const button = screen.getByRole('button', { name: /disabled/i });
        expect(button).toBeDisabled();
        expect(button).toHaveClass('disabled:opacity-50');
    });
});
