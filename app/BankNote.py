from pydantic import BaseModel

class BankNote(BaseModel):
    varience: float 
    skewness: float
    curtosis: float
    entropy: float