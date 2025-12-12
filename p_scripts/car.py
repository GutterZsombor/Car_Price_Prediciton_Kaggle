
#Better than Car Record clean and contains neccesary functions. evritying else is hndeled in the car records

import pandas as pd

class Engine:
    def __init__(self, volume, turbo):
        self.volume = volume   # float or None
        self.turbo = turbo     # bool or None

    def __repr__(self):
        return f"Engine(volume={self.volume}, turbo={self.turbo})"

#Better than Car Record clean and contains neccesary functions. evritying else is hndeled in the car records

class Car:
    def __init__(
        self, ID, price, levy, manufacturer, model, prod_year,
        category, leather_interior, fuel_type, mileage, cylinders,
        gear_box_type, drive_wheels, doors, right_wheel, color, airbags,
        engine: Engine
    ):
        self.ID = ID
        self.price = price
        self.levy = levy
        self.manufacturer = manufacturer
        self.model = model
        self.prod_year = prod_year
        self.category = category
        self.leather_interior = leather_interior
        self.fuel_type = fuel_type
        self.mileage = mileage
        self.cylinders = cylinders
        self.gear_box_type = gear_box_type
        self.drive_wheels = drive_wheels
        self.doors = doors
        self.right_wheel = right_wheel
        self.color = color
        self.airbags = airbags
        self.engine = engine

    def __repr__(self):
        return f"Car(ID={self.ID}, model={self.model}, Price={self.price}, Rigth wheel={self.right_wheel})"
        # props = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        # return f"Car({props})"
    
    # def toDataFrame(cars):
    
    #     #Convert a list of Car objects into a pandas DataFrame.
        
    #     records = []

    #     for car in cars:
    #         records.append({
    #             "price": car.price,
    #             "manufacturer": car.manufacturer,
    #             "model": car.model,
    #             "category": car.category,
    #             "fuel_type": car.fuel_type,
    #             "gear_box_type": car.gear_box_type,
    #             "drive_wheels": car.drive_wheels,
    #             "doors": car.doors,
    #             "mileage": car.mileage,
    #             "prod_year": car.prod_year,
    #             "engine_volume": car.engine.volume if car.engine else None,
    #             "turbo": car.engine.turbo if car.engine else None,
    #         })

    #     return pd.DataFrame(records)


    # #this pipline has been used in EDA prior but i put it here as a centrelized place
    # #for the model this will conect model to everithing else prior
    # #Car object become usles now but its integral part of code but thiis is the most used part from now own
    # def createUsableData():

    #     carRecords = CarRecord.loadFromCSV("p_scripts/first150car.csv")
    #     #carRecords = CarRecord.loadFromCSV("datasets/deepcontractor/car-price-prediction-challenge/versions/1/car_price_prediction.csv")

    #     print("Loaded cars:", len(carRecords))
    #     cars=[]
    #     for c in carRecords:
    #         cars.append(c.toCar())

    #     df = carstoDataFrame(cars)
    #     #print(df.head())
    #     #print(pricebyCategory(df, "manufacturer",5))
        
    #     df_encoded = encodeallStrings(df,5,True)   #.isnull().sum()
    #     #print(df_encoded.head())

    #     return df_encoded
    
    # def heatMapforALL(df_enc,clear=False,threshold=0.30):

    #     corrM=correlationHeatmap(df_enc,clear=False,threshold=0.30)
    #     return corrM
