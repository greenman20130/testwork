from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

from enum import Enum


class Car(BaseModel):
    brand: str
    model: str 
    manufacture_year: int
    fuel_type: str
    gearbox: str 
    mileage: int 
    price: int


class CarCreate(Car):
    id: int 


class CarId(BaseModel):
    carId: int
