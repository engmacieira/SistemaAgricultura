from typing import List, Optional
import pandas as pd
from fpdf import FPDF
from io import BytesIO
from app.infrastructure.repositories.execucao_repository import ExecucaoRepository
from app.infrastructure.repositories.pagamento_repository import PagamentoRepository
from app.infrastructure.repositories.produtor_repository import ProdutorRepository

class RelatorioUseCases:
    def __init__(
        self, 
        execucao_repo: ExecucaoRepository,
        pagamento_repo: PagamentoRepository,
        produtor_repo: ProdutorRepository
    ):
        self.execucao_repo = execucao_repo
        self.pagamento_repo = pagamento_repo
        self.produtor_repo = produtor_repo

    def gerar_servicos_executados_pdf(self, start_date: str, end_date: str) -> bytes:
        execucoes = self.execucao_repo.get_by_date_range(start_date, end_date)
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, "Relatório de Serviços Executados", ln=True, align="C")
        pdf.set_font("Helvetica", "", 12)
        pdf.cell(0, 10, f"Período: {start_date} a {end_date}", ln=True, align="C")
        pdf.ln(10)
        
        # Table Header
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(30, 10, "Data", 1)
        pdf.cell(60, 10, "Produtor", 1)
        pdf.cell(50, 10, "Serviço", 1)
        pdf.cell(20, 10, "Qtd", 1)
        pdf.cell(30, 10, "Valor Total", 1)
        pdf.ln()
        
        pdf.set_font("Helvetica", "", 10)
        total_geral = 0
        for ex in execucoes:
            pdf.cell(30, 10, str(ex.date), 1)
            pdf.cell(60, 10, str(ex.producerName)[:25], 1)
            pdf.cell(50, 10, str(ex.serviceName)[:20], 1)
            pdf.cell(20, 10, f"{ex.quantity} {ex.unit}", 1)
            pdf.cell(30, 10, f"R$ {ex.totalValue:.2f}", 1)
            pdf.ln()
            total_geral += ex.totalValue
            
        pdf.ln(5)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, f"Total Geral: R$ {total_geral:.2f}", ln=True, align="R")
        
        return bytes(pdf.output())

    def gerar_faturamento_pdf(self, start_date: Optional[str], end_date: Optional[str], producers: Optional[List[str]]) -> bytes:
        pagamentos = self.pagamento_repo.get_by_filters(start_date, end_date, producers)
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, "Relatório de Faturamento", ln=True, align="C")
        if start_date or end_date:
            pdf.set_font("Helvetica", "", 12)
            pdf.cell(0, 10, f"Período: {start_date or '...'} a {end_date or '...'}", ln=True, align="C")
        pdf.ln(10)
        
        # Table Header
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(50, 10, "Produtor", 1)
        pdf.cell(40, 10, "Serviço", 1)
        pdf.cell(25, 10, "Vencimento", 1)
        pdf.cell(25, 10, "Valor", 1)
        pdf.cell(25, 10, "Pago", 1)
        pdf.cell(25, 10, "Status", 1)
        pdf.ln()
        
        pdf.set_font("Helvetica", "", 8)
        total_devido = 0
        total_pago = 0
        for p in pagamentos:
            pdf.cell(50, 10, str(p.producerName)[:25], 1)
            pdf.cell(40, 10, str(p.serviceName)[:20], 1)
            pdf.cell(25, 10, str(p.dueDate), 1)
            pdf.cell(25, 10, f"R$ {p.amount:.2f}", 1)
            pdf.cell(25, 10, f"R$ {p.paidAmount:.2f}", 1)
            pdf.cell(25, 10, p.status, 1)
            pdf.ln()
            total_devido += p.amount
            total_pago += p.paidAmount
            
        pdf.ln(5)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 8, f"Total Devido: R$ {total_devido:.2f}", ln=True, align="R")
        pdf.cell(0, 8, f"Total Pago: R$ {total_pago:.2f}", ln=True, align="R")
        pdf.cell(0, 8, f"Saldo Pendente: R$ {(total_devido - total_pago):.2f}", ln=True, align="R")
        
        return bytes(pdf.output())

    def gerar_produtores_pdf(self, producer_id: Optional[str], status: Optional[str], regiao: Optional[str]) -> bytes:
        produtores = self.produtor_repo.get_by_filters(producer_id, status, regiao)
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, "Relatório de Produtores", ln=True, align="C")
        pdf.ln(10)
        
        for p in produtores:
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 10, f"Produtor: {p.name} ({p.apelido_produtor or 'N/A'})", ln=True)
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(0, 8, f"CPF/CNPJ: {p.cpfCnpj}", ln=True)
            pdf.cell(0, 8, f"Propriedade: {p.property}", ln=True)
            pdf.cell(0, 8, f"Comunidade: {p.regiao_referencia or 'N/A'}", ln=True)
            pdf.cell(0, 8, f"Telefone: {p.telefone_contato or 'N/A'}", ln=True)
            pdf.cell(0, 8, f"Status: {p.status}", ln=True)
            pdf.ln(5)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(5)
            
        return bytes(pdf.output())
