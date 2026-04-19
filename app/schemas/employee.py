from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class EmployeeBase(BaseModel):
    status: Optional[int] = 1
    
    class Config:
        populate_by_name = True


class EmployeeCreate(EmployeeBase):
    id: Optional[int] = None
    id_number: Optional[str] = Field(None, alias="idNumber")
    name: str
    phone: Optional[str] = None
    sex: Optional[str] = None
    username: str
    password: str


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    sex: Optional[str] = None
    id_number: Optional[str] = Field(None, alias="idNumber")
    status: Optional[int] = None
    
    class Config:
        populate_by_name = True


class EmployeeResponse(EmployeeBase):
    id: int
    id_number: Optional[str] = Field(None, alias="idNumber")
    name: str
    phone: Optional[str] = None
    sex: Optional[str] = None
    username: str
    create_time: datetime
    update_time: datetime
    create_user: Optional[int] = None
    update_user: Optional[int] = None
    
    class Config:
        from_attributes = True
        populate_by_name = True


class EmployeeLogin(BaseModel):
    username: str
    password: str