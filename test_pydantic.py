from pydantic import BaseModel
from typing import Optional
import datetime

class ExecucaoUpdate(BaseModel):
    date: Optional[datetime.date] = None

try:
    obj = ExecucaoUpdate(date="2026-03-03")
    print(f"Success: {obj.date}")
except Exception as e:
    print(f"Error: {e}")
