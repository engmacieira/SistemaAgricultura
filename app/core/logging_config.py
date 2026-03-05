import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler

class DateRotatingFileHandler(RotatingFileHandler):
    """
    Custom RotatingFileHandler that rotates by date (YYYY-MM-DD.txt) 
    and limits each file to a maximum size (maxBytes).
    """
    def __init__(self, log_dir, maxBytes=10*1024*1024, backupCount=10, encoding='utf-8', delay=False):
        self.log_dir = os.path.abspath(log_dir)
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        base_filename = os.path.join(self.log_dir, f"{self.current_date}.txt")
        
        super().__init__(base_filename, maxBytes=maxBytes, backupCount=backupCount, encoding=encoding, delay=delay)

    def _should_rotate_by_date(self):
        return datetime.now().strftime("%Y-%m-%d") != self.current_date

    def emit(self, record):
        """
        Check if we need to rotate by date before emitting.
        """
        if self._should_rotate_by_date():
            self.stream.close()
            self.current_date = datetime.now().strftime("%Y-%m-%d")
            self.baseFilename = os.path.abspath(os.path.join(self.log_dir, f"{self.current_date}.txt"))
            self.stream = self._open()
        
        super().emit(record)

def setup_logging():
    """
    Configures the logging system to save logs to files.
    """
    # Define the log directory (root/logs)
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    log_dir = os.path.join(root_dir, "logs")
    
    # Create the handler
    file_handler = DateRotatingFileHandler(log_dir)
    
    # Formatting
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(log_format)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    
    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Remove existing handlers to avoid duplicates during reload
    root_logger.handlers = []
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Configure Uvicorn loggers specifically to use our handler
    for logger_name in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
        uv_logger = logging.getLogger(logger_name)
        uv_logger.handlers = []
        uv_logger.addHandler(file_handler)
        uv_logger.addHandler(console_handler)
        uv_logger.propagate = False

    logging.info("Sistema de logs inicializado.")
