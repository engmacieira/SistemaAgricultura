import { Payment, PaymentTransaction } from "../domain/Payment";
import { apiFetch } from "../../../core/api"; // This import will likely need to change to 'api' if 'apiFetch' is replaced by 'api.get/post/put/delete'

const PATH = "/pagamentos";

export class PaymentRepository {
  async getPayments(page: number = 0, limit: number = 10, sortBy: string = "dueDate", order: string = "desc", search: string = ""): Promise<{ items: Payment[], total: number }> {
    const skip = page * limit;
    return apiFetch(`${PATH}/?skip=${skip}&limit=${limit}&sort_by=${sortBy}&order=${order}&search=${search}`);
  }

  async getPayment(id: string): Promise<Payment> {
    return apiFetch(`${PATH}/${id}`);
  }

  async updatePayment(id: string, data: Partial<Payment>): Promise<Payment> {
    return apiFetch(`${PATH}/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  }

  async payPayment(id: string, amountToPay: number, paymentDate?: string): Promise<Payment> {
    return apiFetch(`${PATH}/${id}/pagar`, {
      method: "POST",
      body: JSON.stringify({ amountToPay, paymentDate }),
    });
  }

  async getPaymentHistory(id: string): Promise<PaymentTransaction[]> {
    return apiFetch(`${PATH}/${id}/historico`);
  }

  async deletePayment(id: string): Promise<void> {
    await apiFetch(`${PATH}/${id}`, {
      method: "DELETE"
    });
  }

  async getDebtsByProducer(search: string = ""): Promise<{ records: any[], totalGeneral: number }> {
    return apiFetch(`${PATH}/debitos-por-produtor?search=${search}`);
  }

  async updateTransaction(id: string, data: { amount?: number, date?: string }): Promise<PaymentTransaction> {
    return apiFetch(`${PATH}/transacoes/${id}`, {
      method: "PUT",
      body: JSON.stringify(data)
    });
  }

  async deleteTransaction(id: string): Promise<void> {
    await apiFetch(`${PATH}/transacoes/${id}`, {
      method: "DELETE"
    });
  }
}
