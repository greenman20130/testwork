from typing import List
from fastapi import APIRouter, Depends
from src.car.schemas import Car, CarCreate, CarId
from src.repository import CarRepository
from fastapi import HTTPException


router = APIRouter(prefix="/car", tags=["Car"])


@router.post("")
async def add_car(car: Car = Depends()) -> CarId:
    """Add a new car to the database."""
    try:
        car_id = await CarRepository.add_car(car)
        return car_id
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while adding the car.")


@router.get("/{car_id}")
async def get_car_by_id(car_id: int) -> CarCreate:
    """Get a car by its ID."""
    try:
        car = await CarRepository.get_car(car_id)
        if car is None:
            raise HTTPException(status_code=404, detail="Car not found.")
        return car
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the car.")


@router.get("")
async def get_cars_by_filters(
    brand: str = None,
    model: str = None,
    manufacture_year: int = None,
    fuel_type: str = None,
    gearbox: str = None,
    mileage_min: int = None,
    mileage_max: int = None,
    price_min: int = None,
    price_max: int = None
) -> List[CarCreate]:
    """Get cars based on filter criteria."""
    try:
        cars = await CarRepository.get_cars(
            brand, model, manufacture_year, fuel_type, gearbox,
            mileage_min, mileage_max, price_min, price_max
        )
        return cars
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving cars.")