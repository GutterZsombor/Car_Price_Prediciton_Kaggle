from carrecord import CarRecord 
import statistics
from presentdata import *
from encode_string import encodeallStrings


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
            #Numeric
            "price": car.price,
            "levy": car.levy,
            "doors": car.doors,
            "mileage": car.mileage,
            "prod_year": car.prod_year,
            "engine_volume": car.engine.volume if car.engine else None,
            "turbo": 1 if car.engine.turbo else 0,
            "cylinders": car.cylinders,
            "airbags": car.airbags,
            "rightw": 1 if car.right_wheel else 0,
            "leather":1 if car.leather_interior else 0,

            #string
            "manufacturer": car.manufacturer,
            "model": car.model,
            "category": car.category,
            "fuel_type": car.fuel_type,
            "gear_box_type": car.gear_box_type,
            "drive_wheels": car.drive_wheels,
            "color": car.color

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


#this pipline has been used in EDA prior but i put it here as a centrelized place
#for the model this will conect model to everithing else prior
#Car object become usles now but its integral part of code but thiis is the most used part from now own
def createUsableData():

    #carRecords = CarRecord.loadFromCSV("p_scripts/first150car.csv")
    carRecords = CarRecord.loadFromCSV("datasets/deepcontractor/car-price-prediction-challenge/versions/1/car_price_prediction.csv")

    print("Loaded cars:", len(carRecords))
    cars=[]
    for c in carRecords:
        cars.append(c.toCar())

    df = carstoDataFrame(cars)
    #print(df.head())
    #print(pricebyCategory(df, "manufacturer",5))
    
    df_encoded = encodeallStrings(df,5,True)   #.isnull().sum()
    #print(df_encoded.head())
    #print(df_encoded.dtypes)

    return df_encoded
    
def heatMapforALL(df_enc,clear=False,threshold=0.30,show=False):

    corrM=correlationHeatmap(df_enc,clear,threshold,show)
    return corrM




if __name__ == "__main__":
    # carRecords = CarRecord.loadFromCSV("p_scripts/first150car.csv")
    carRecords = CarRecord.loadFromCSV("datasets/deepcontractor/car-price-prediction-challenge/versions/1/car_price_prediction.csv")

    print("Loaded cars:", len(carRecords))
    cars=[]
    for c in carRecords:
        #print(c.toCar().right_wheel)
        cars.append(c.toCar())
    # #print(cars)

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
    #price_vs_prod_year_corr=priceCorrelation(cars, "prod_year", heatmap=True)
    # price_vs_levy_corr=priceCorrelation(cars, "levy", heatmap=True)
    # price_vs_evolume_corr=priceCorrelation(cars, "engine.volume", heatmap=True)

    #Manufacturer and model distribution
    #plotCategoryDistribution(cars,"manufacturer",20)
    #plotCategoryDistribution(cars,"model",20)
    #plotCategoryDistribution(cars, "category", top=20)
    #plotCategoryDistribution(cars, "gear_box_type", top=20)
    
    #plotCategoryDistribution(cars, "levy", top=50)

    #plotAllCategoryDistributions(cars, top=30)

    # #price chategorie colaration:
    # df = carstoDataFrame(cars)
    # print(df.head())
    # print(pricebyCategory(df, "manufacturer",5))
    # #df_numeric=numericDF(df)
    # #correlationHeatmap(df_numeric,True)
    # df_encoded = encodeallStrings(df,5,True)
    # print(df_encoded.head())

    df_enc=createUsableData()
    corrM=heatMapforALL(df_enc,False,0.25, True)
