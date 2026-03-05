from typing import Dict, Any
from datetime import datetime

class AdministradorUseCases:
    def __init__(self, configuracao_repository, backup_service=None):
        self.configuracao_repository = configuracao_repository
        self.backup_service = backup_service # Serviço externo para lidar com o dump do banco

    def obter_configuracoes(self) -> Dict[str, Any]:
        return self.configuracao_repository.get_configuracoes()

    def atualizar_configuracoes(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.configuracao_repository.update_configuracoes(data)

    def realizar_backup(self) -> Dict[str, Any]:
        """Inicia o processo de dump do banco de dados"""
        if not self.backup_service:
            raise ValueError("Serviço de backup não configurado")
            
        backup_path = self.backup_service.create_backup()
        return {
            "status": "sucesso",
            "message": "Backup realizado com sucesso",
            "timestamp": datetime.now().isoformat(),
            "file_url": backup_path
        }

    def restaurar_backup(self, file_url: str = None) -> Dict[str, Any]:
        """Inicia o processo de restauração do banco de dados"""
        if not self.backup_service:
            raise ValueError("Serviço de backup não configurado")
            
        success = self.backup_service.restore_backup(file_url)
        if not success:
            raise ValueError("Falha ao restaurar backup. Verifique se o arquivo existe.")

        return {
            "status": "sucesso",
            "message": "Banco de dados restaurado com sucesso",
            "timestamp": datetime.now().isoformat(),
            "file_url": file_url or "latest"
        }
