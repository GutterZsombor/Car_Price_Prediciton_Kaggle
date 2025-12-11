from EDA import *


if __name__ == "__main__":
    carRecords = CarRecord.loadFromCSV("p_scripts/first150car.csv")
    #carRecords = CarRecord.loadFromCSV("datasets/deepcontractor/car-price-prediction-challenge/versions/1/car_price_prediction.csv")

    print("Loaded cars:", len(carRecords))
    cars=[]
    for c in carRecords:
        cars.append(c.toCar())

    df = carstoDataFrame(cars)

    #print(df.head())
    #print(df.shape)
