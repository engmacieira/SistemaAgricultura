import os
import shutil
import sqlite3
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class BackupService:
    def __init__(self, db_path: str = None, backup_dir: str = None):
        from app.core.database import BASE_DIR, DB_PATH
        self.db_path = db_path or str(DB_PATH)
        self.backup_dir = backup_dir or os.path.join(str(BASE_DIR), "backups")
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def create_backup(self) -> str:
        """
        Cria um backup do banco de dados SQLite.
        Se já existir um backup para o dia de hoje, ele será sobrescrito.
        """
        today = datetime.now().strftime("%Y-%m-%d")
        backup_filename = f"backup_{today}.db"
        backup_path = os.path.join(self.backup_dir, backup_filename)

        try:
            # Usando VACUUM INTO para um backup consistente se o banco estiver em uso
            # No Windows, se o arquivo já existir, o VACUUM INTO pode falhar se não deletarmos antes
            if os.path.exists(backup_path):
                os.remove(backup_path)

            conn = sqlite3.connect(self.db_path)
            conn.execute(f"VACUUM INTO '{backup_path}'")
            conn.close()
            
            logger.info(f"Backup criado com sucesso em: {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"Erro ao criar backup: {e}")
            # Fallback para cópia simples se o VACUUM falhar por algum motivo de versão/permissão
            try:
                shutil.copy2(self.db_path, backup_path)
                logger.info(f"Backup criado via cópia de arquivo em: {backup_path}")
                return backup_path
            except Exception as e2:
                logger.error(f"Erro fatal ao criar backup (fallback falhou): {e2}")
                raise e2

    def clean_old_backups(self, days: int = 10):
        """
        Remove backups com mais de 'days' dias.
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        
        try:
            for filename in os.listdir(self.backup_dir):
                if not filename.startswith("backup_") or not filename.endswith(".db"):
                    continue
                
                # Formato esperado: backup_YYYY-MM-DD.db
                date_str = filename.replace("backup_", "").replace(".db", "")
                try:
                    file_date = datetime.strptime(date_str, "%Y-%m-%d")
                    if file_date < cutoff_date:
                        file_path = os.path.join(self.backup_dir, filename)
                        os.remove(file_path)
                        logger.info(f"Backup antigo removido: {file_path}")
                except ValueError:
                    continue
        except Exception as e:
            logger.error(f"Erro ao limpar backups antigos: {e}")

    def restore_backup(self, backup_filename: str = None) -> bool:
        """
        Restaura o banco de dados a partir de um arquivo de backup.
        Se backup_filename for None, restaura o mais recente.
        """
        if not backup_filename:
            backups = [f for f in os.listdir(self.backup_dir) if f.startswith("backup_") and f.endswith(".db")]
            if not backups:
                logger.error("Nenhum backup encontrado para restauração")
                return False
            backup_filename = sorted(backups)[-1]

        backup_path = os.path.join(self.backup_dir, backup_filename)
        if not os.path.exists(backup_path):
            logger.error(f"Arquivo de backup não encontrado: {backup_path}")
            return False

        try:
            # Para restaurar o SQLite, o ideal é fechar as conexões, mas como estamos no reload/startup
            # simplificaremos para a cópia do arquivo.
            # Nota: O sistema pode precisar ser reiniciado se o arquivo estiver travado.
            shutil.copy2(backup_path, self.db_path)
            logger.info(f"Banco de dados restaurado com sucesso a partir de: {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Erro ao restaurar backup: {e}")
            return False

    def list_backups(self):
        """Lista todos os backups disponíveis"""
        backups = [f for f in os.listdir(self.backup_dir) if f.startswith("backup_") and f.endswith(".db")]
        return sorted(backups, reverse=True)
