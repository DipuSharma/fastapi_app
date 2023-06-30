from typing import List, Optional

from pydantic import BaseModel

class CeleryTest(BaseModel):
    num1: float
    num2: float
    Operation: str