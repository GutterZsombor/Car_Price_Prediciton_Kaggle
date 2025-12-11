from carrecord import CarRecord
from car import Car
import statistics
from presentdata import *


#if only one categorie needed
def meanMedianforCategorie(cars,categorie):
    #return mean, median for "important" numerical values (categorie)
    # eg.: price, levy, milage, prod_year, engine.volume or anything else
    # engione.volume is nested so special treatment

    atributes=categorie.split(".")#for engine.volume

    values = []
    for car in cars:
        try:
            obj = car
            for p in atributes:      #nested attributes
                obj = getattr(obj, p)

            if obj is not None:
                values.append(obj)

        except AttributeError:
            continue  # skip missing fields

    # no values
    if not values:
        return None, None

    # statistics safely
    mean_val = statistics.mean(values)
    median_val = statistics.median(values)

    return mean_val, median_val

#more efficvient if a lot needed
def meanMedianallImportant(cars):
    #Compute mean and median for important numerical fields:
    #price, levy, mileage, prod_year, engine.volume

    """{
        "price": (mean, median),
        "levy": (mean, median),
        "mileage": (mean, median),
        "prod_year": (mean, median),
        
    }"""
    
    data = {
        "price": [],
        "levy": [],
        "mileage": [],
        "prod_year": [],
        
    }

    for car in cars:
        if car.price is not None:
            data["price"].append(car.price)

        if car.levy is not None:
            data["levy"].append(car.levy)

        if car.mileage is not None:
            data["mileage"].append(car.mileage)

        if car.prod_year is not None:
            data["prod_year"].append(car.prod_year)

    returndict = {}
    for key, values in data.items():
        if values:
            returndict[key] = (
                statistics.mean(values),
                statistics.median(values)
            )
        else:
            returndict[key] = (None, None)

    return returndict





if __name__ == "__main__":
    carRecords = CarRecord.loadFromCSV("p_scripts/first150car.csv")

    print("Loaded cars:", len(carRecords))
    cars=[]
    for c in carRecords:
        #print(c)
        cars.append(c.toCar())
    #print(cars)

    #print("Mean, Median statistics:")
    #print(meanMedianallImportant(cars))
    #dict_stats=meanMedianallImportant(cars)
    #dispTablefromDict(dict_stats)

    #Price distribution
    #Normal scle
    #priceDistriutionPlot(cars,False)
    #log scle
    #priceDistriutionPlot(cars,True)

    #Price correlation 
    # price_vs_milage_corr=priceCorrelation(cars, "mileage", heatmap=True)
    # price_vs_prod_year_corr=priceCorrelation(cars, "prod_year", heatmap=True)
    # price_vs_levy_corr=priceCorrelation(cars, "levy", heatmap=True)
    # price_vs_evolume_corr=priceCorrelation(cars, "engine.volume", heatmap=True)