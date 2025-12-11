from carrecord import CarRecord
from car import Car




if __name__ == "__main__":
    cars = CarRecord.loadFromCSV("p_scripts/first150car.csv")

    print("Loaded cars:", len(cars))
    for c in cars[:10]:
        #print(c)
        print(c.toCar())