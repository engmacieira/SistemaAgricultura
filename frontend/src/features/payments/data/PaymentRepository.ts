import { Payment } from "../domain/Payment";

const API_URL = "/pagamentos";

export class PaymentRepository {
  async getPayments(): Promise<Payment[]> {
    const response = await fetch(API_URL);
    if (!response.ok) throw new Error("Failed to fetch payments");
    return response.json();
  }

  async updatePayment(id: string, payment: Partial<Payment>): Promise<Payment | undefined> {
    const response = await fetch(`${API_URL}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payment),
    });
    if (!response.ok) throw new Error("Failed to update payment");
    return response.json();
  }

  async payPayment(id: string): Promise<Payment | undefined> {
    const response = await fetch(`${API_URL}/${id}/pagar`, {
      method: "POST",
    });
    if (!response.ok) throw new Error("Failed to pay payment");
    return response.json();
  }
}
