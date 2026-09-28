from typing import List,Dict
from pydantic import BaseModel,Field,EmailStr

class Register(BaseModel):
    name:str=Field(min_length=2,max_length=100)
    email:EmailStr
    password:str=Field(min_length=6,max_length=100)
class Login(BaseModel):
    email:EmailStr
    password:str
class Home(BaseModel):
    budget:float=Field(gt=0)
    rooms:List[str]=Field(min_length=1)
    style:str="Modern"
    notes:str=""
    quantities:Dict[str,int]={}
class Party(BaseModel):
    budget:float=Field(gt=0)
    guests:int=Field(gt=0)
    event_type:str
    venue:str="Flexible"
    city:str=""
    preferences:str=""
