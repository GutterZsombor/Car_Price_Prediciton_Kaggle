from carrecord import CarRecord
from car import Car




if __name__ == "__main__":
    cars = CarRecord.loadFromCSV("datasets/deepcontractor/car-price-prediction-challenge/versions/1/car_price_prediction.csv")

    print("Loaded cars:", len(cars))
    for c in cars[:10]:
        print(c)
        print(c.toCar())