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

def carstoDataFrame(cars):
    records = []

    for car in cars:
        records.append({
            "price": car.price,
            "levy": car.levy,
            "manufacturer": car.manufacturer,
            "model": car.model,
            "category": car.category,
            "fuel_type": car.fuel_type,
            "gear_box_type": car.gear_box_type,
            "drive_wheels": car.drive_wheels,
            "doors": car.doors,
            "mileage": car.mileage,
            "prod_year": car.prod_year,
            "engine_volume": car.engine.volume if car.engine else None,
            "turbo": 1 if car.engine.turbo else 0,
            "cylinders": car.cylinders,
            "airbags": car.airbags,
            "color": car.color,
            "rightw": 1 if car.right_wheel else 0,
            "leather":1 if car.leather_interior else 0
        })
    

    return pd.DataFrame(records)

def pricebyCategory(df, column, min=50):
    
    #rturns mean price per category if there is more than min amount of them .
    
    grp = df.groupby(column)["price"].agg(["mean", "median", "count"]).sort_values("mean", ascending=False)
    return grp[grp["count"] >= min]

def numericDF(df):
    numeric_columns = [
        "price", "mileage", "prod_year", "engine_volume", "turbo",
        "cylinders", "airbags", "levy", "doors" ,"rightw","leather"
    ]

    return df[numeric_columns ]



if __name__ == "__main__":
    carRecords = CarRecord.loadFromCSV("p_scripts/first150car.csv")
    #carRecords = CarRecord.loadFromCSV("datasets/deepcontractor/car-price-prediction-challenge/versions/1/car_price_prediction.csv")

    print("Loaded cars:", len(carRecords))
    cars=[]
    for c in carRecords:
        #print(c.toCar().right_wheel)
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

    #Manufacturer and model distribution
    #plotCategoryDistribution(cars,"manufacturer",20)
    #plotCategoryDistribution(cars,"model",20)
    #plotCategoryDistribution(cars, "category", top=20)
    #plotCategoryDistribution(cars, "gear_box_type", top=20)
    
    #plotCategoryDistribution(cars, "right_wheel", top=20)

    #plotAllCategoryDistributions(cars, top=20)

    #price chategorie colaration:
    df = carstoDataFrame(cars)
    #print(pricebyCategory(df, "manufacturer",5))
    df_numeric=numericDF(df)
    correlationHeatmap(df_numeric,True)
