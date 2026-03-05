from fastapi import APIRouter, Depends, Query, Response
from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.infrastructure.repositories.execucao_repository import ExecucaoRepository
from app.infrastructure.repositories.pagamento_repository import PagamentoRepository
from app.infrastructure.repositories.produtor_repository import ProdutorRepository
from app.use_cases.relatorio_use_cases import RelatorioUseCases

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])

def get_relatorio_use_cases(db: Session = Depends(get_db)):
    exec_repo = ExecucaoRepository(db)
    pag_repo = PagamentoRepository(db)
    prod_repo = ProdutorRepository(db)
    return RelatorioUseCases(exec_repo, pag_repo, prod_repo)

@router.get("/servicos-executados")
def get_servicos_executados(
    start_date: str = Query(..., description="Data de início (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data de fim (YYYY-MM-DD)"),
    format: str = Query("pdf", description="Formato do relatório (pdf ou excel)"),
    use_cases: RelatorioUseCases = Depends(get_relatorio_use_cases)
):
    if format == "pdf":
        content = use_cases.gerar_servicos_executados_pdf(start_date, end_date)
        return Response(
            content=content,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=servicos_{start_date}_{end_date}.pdf"}
        )
    # Excel implementation could be added if needed, user only asked for PDF for this block
    return {"message": "Formato não suportado para este relatório"}

@router.get("/faturamento")
def get_faturamento(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    producers: Optional[List[str]] = Query(None),
    use_cases: RelatorioUseCases = Depends(get_relatorio_use_cases)
):
    content = use_cases.gerar_faturamento_pdf(start_date, end_date, producers)
    return Response(
        content=content,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=faturamento.pdf"}
    )

@router.get("/produtores")
def get_produtores(
    producer_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    regiao: Optional[str] = Query(None),
    use_cases: RelatorioUseCases = Depends(get_relatorio_use_cases)
):
    content = use_cases.gerar_produtores_pdf(producer_id, status, regiao)
    return Response(
        content=content,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=produtores.pdf"}
    )
