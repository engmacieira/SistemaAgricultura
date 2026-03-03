import React from "react";
import { cn } from "../../core/utils";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "danger" | "ghost";
  size?: "default" | "sm" | "lg";
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "default", ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          "inline-flex items-center justify-center rounded-md text-sm font-bold transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-white",
          {
            "bg-blue-800 text-white hover:bg-blue-900 focus-visible:ring-blue-800": variant === "primary",
            "bg-gray-200 text-gray-900 hover:bg-gray-300 focus-visible:ring-gray-500": variant === "secondary",
            "bg-red-700 text-white hover:bg-red-800 focus-visible:ring-red-700": variant === "danger",
            "hover:bg-gray-100 hover:text-gray-900 text-gray-700": variant === "ghost",
            "h-12 px-6 py-2": size === "default", // 48px min height for accessibility
            "h-10 px-4 rounded-md": size === "sm",
            "h-14 px-8 rounded-md text-base": size === "lg",
          },
          className
        )}
        {...props}
      />
    );
  }
);
Button.displayName = "Button";
