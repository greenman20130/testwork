from pydantic import ValidationError
from src.database import new_session, CarOrm
from src.car.schemas import Car, CarCreate
from sqlalchemy import select


class CarRepository:
    @classmethod
    async def add_car(cls, data: CarCreate) -> dict:
        try:
            async with new_session() as session:
                car_dict = data.model_dump()
                car = CarOrm(**car_dict)
                session.add(car)
                await session.flush()  # to get the id
                await session.commit()

                return {'carId': int(car.id)}
        except ValidationError as e:
            # Handle validation errors
            print(f"Validation error: {e}")
            return {"error": "Invalid car data"}
        except Exception as e:
            # Handle other errors
            print(f"An error occurred: {e}")
            return {"error": "An error occurred while adding the car"}

    @classmethod
    async def get_car(cls, car_id: int) -> CarOrm:
        try:
            async with new_session() as session:
                query = select(CarOrm).where(CarOrm.id == car_id)
                result = await session.execute(query)
                car_model = result.scalars().first()

                if car_model is None:
                    raise Exception("Car not found")

                return car_model
        except Exception as e:
            # Handle other errors
            print(f"An error occurred: {e}")
            return None

    @classmethod
    async def get_cars(
        cls,
        brand: str = None,
        model: str = None,
        manufacture_year: int = None,
        fuel_type: str = None,
        gearbox: str = None,
        mileage_min: int = None,
        mileage_max: int = None,
        price_min: int = None,
        price_max: int = None
    ) -> list:
        try:
            async with new_session() as session:
                query = select(CarOrm)

                filters = []
                if brand:
                    filters.append(CarOrm.brand == brand)
                if model:
                    filters.append(CarOrm.model == model)
                if manufacture_year:
                    filters.append(CarOrm.manufacture_year == manufacture_year)
                if fuel_type:
                    filters.append(CarOrm.fuel_type == fuel_type)
                if gearbox:
                    filters.append(CarOrm.gearbox == gearbox)
                if mileage_min is not None and mileage_max is not None:
                    filters.append(CarOrm.mileage.between(mileage_min, mileage_max))
                if price_min is not None and price_max is not None:
                    filters.append(CarOrm.price.between(price_min, price_max))

                # Apply all filters to the query
                if filters:
                    query = query.where(*filters)

                result = await session.execute(query)
                car_models = result.scalars().all()

                return car_models
        except Exception as e:
            # Handle other errors
            print(f"An error occurred: {e}")
            return []
        
    @classmethod
    async def delete_car(cls, car_id: int) -> bool:
        try:
            async with new_session() as session:
                query = select(CarOrm).where(CarOrm.id == car_id)
                result = await session.execute(query)
                car_model = result.scalars().first()

                if car_model is None:
                    raise Exception("Car not found")

                await session.delete(car_model)
                await session.commit()

                return True
            
        except Exception as e:
            # Handle other errors
            print(f"An error occurred: {e}")
            return False
    
    @classmethod
    async def update_car(cls, car_id: int, data: CarCreate) -> bool:
        try:
            async with new_session() as session:
                query = select(CarOrm).where(CarOrm.id == car_id)
                result = await session.execute(query)
                car_model = result.scalars().first()

                if car_model is None:
                    raise Exception("Car not found")

                car_dict = data.model_dump()
                for key, value in car_dict.items():
                    setattr(car_model, key, value)

                await session.commit()

                return True
            
        except ValidationError as e:
            # Handle validation errors
            print(f"Validation error: {e}")
            return False
        
        except Exception as e:
            # Handle other errors
            print(f"An error occurred: {e}")
            return False