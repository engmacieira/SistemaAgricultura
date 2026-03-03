import { Payment } from "../domain/Payment";
import { apiFetch } from "../../../core/api";

const PATH = "/pagamentos";

export class PaymentRepository {
  async getPayments(): Promise<Payment[]> {
    return apiFetch(PATH);
  }

  async updatePayment(id: string, payment: Partial<Payment>): Promise<Payment | undefined> {
    return apiFetch(`${PATH}/${id}`, {
      method: "PUT",
      body: JSON.stringify(payment),
    });
  }

  async payPayment(id: string): Promise<Payment | undefined> {
    return apiFetch(`${PATH}/${id}/pagar`, {
      method: "POST",
    });
  }
}
