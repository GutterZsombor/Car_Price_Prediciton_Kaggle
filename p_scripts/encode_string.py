from weight_adjustmodell import getweights
import numpy as np
def encodeCathegory(df, column, min=30):
  
    #Returns a mapping category: mean_price
    #ignoring small  

    stats = df.groupby(column)["price"].agg(["mean", "count"])

    # Only keep usable number categories
    stats = stats[stats["count"] >= min]

    # Convert to dict
    mapping = stats["mean"].to_dict()

    return mapping


def addtheEncoded(df, column, mapping):#,weight=1.0

    #replace string values with numeric values.
    # rare values = global mean price.

    #Imporve the relevancy with weights
    global_mean = df["price"].mean()

    df[column + "_enc"] = df[column].map(mapping).fillna(global_mean)

    # encoded = df[column].map(mapping).fillna(global_mean)

    # # Apply weighting factor
    # df[column + "_enc"] = encoded * weight

    return df


strings = [
   "manufacturer", #initially remove added back
    "model",
    "brand_model",
    "category",
    "fuel_type",
    "gear_box_type",
    "drive_wheels",
    "color",
    "mileage_per_year"
]

def encodeallStrings(df,min=20,drop=False):
    #Imporvements
    df = brandModell(df)
    df=yearMilageimrovement(df)
    df=dealwithlevy(df)
    df=kagleFilter(df)
    #df=decimating(df)
     #Imporve the relevancy with weights
    # color lower influence
    # stringWeights={
    #     "model"       :    1.000,
    #     "brand_model"   :  1.000,
    #     "drive_wheels"   :  0.797,
    #     "fuel_type"      :  0.794,
    #     "gear_box_type"  :  0.583,
    #     "category"       :  0.238,
    #     "manufacturer"   :  0.208

    # }
    '''WEIGHTS
model            1.000
brand_model      1.000
drive_wheels     0.797
fuel_type        0.794
gear_box_type    0.583
category         0.238
manufacturer     0.208'''


    for col in strings:
        #mapping = encodeCathegory(df, col,min)
        if col == "brand_model":
            mapping = encodeCathegory(df, col, min=5)#5 found troght trial andd error
        else:
            mapping = encodeCathegory(df, col, min=min)
            #weight = stringWeights.get(col,1.0)#one is fallback incase its not sepcified
        df = addtheEncoded(df, col, mapping)
    if not drop:
        return df
    
    return df.drop(columns=strings)



#Impovements:
#"merge" manufacturer and modell  “brand_model” 
# because: BMW 320 vs BMW X5 has huge price difference



def brandModell(df):
    df["brand_model"] = df["manufacturer"] + "_" + df["model"]
    #df.drop(columns=["manufacturer", "model"])
    
    return df

#more imporvement instead of prodyear - carage
#
def yearMilageimrovement(df):
    current_year = 2025

    df["car_age"] = current_year - df["prod_year"]

    df["mileage_per_year"] = df["mileage"] / (df["car_age"] + 1)
    
    df=df.drop(columns=["car_age"])

    #remove recent higvalue/bearly used cars and very old low value cars
    #df = df[(df["prod_year"] > 2000) & (df["prod_year"] < 2020)]


    return df

#quick filter idea came from kaggle users code
#using my distribution charts ine EDA:plotAllCategoryDistributions(cars, top=30)
#Lets drop evrithying bellow 180->entry  of manufacturer so mazda iz the last jeep doesnt qualify
#with models lets have it at 180 again

#this aleardy reduced RMSE lets filter more based on EDA

#tackle odd ball low prices because they are mainly exeptions not rule
#Price distribution
##Normal scle
# priceDistriutionPlot(cars,False)
##log scle
# priceDistriutionPlot(cars,True)
def kagleFilter(df):
    df = df[df["manufacturer"].value_counts()[df["manufacturer"]].values > 180]
    df = df[df["model"].value_counts()[df["model"]].values > 180]

    df = df[np.log(df["price"]) > 8]    # price < 1100 (7)  <1800 (7.5) based on log(price) histogram
    #remove extremly overvalued cars
    df = df[np.log(df["price"]) <= 11]


   
    return df

#levy intruducers a lot of nose based on EDA plot 
#tax doesnt effect price it effect likelyness of buying this in not our topic
#i decided tro drop levy coulm
def dealwithlevy(df):
    return df.drop(columns=["levy"])

#BAD ideas price colaration can be zore and still influen result
#final try based on EDA coleration heatmap i dropp all cathecories with lower than |0.25| coleration with price
# def decimating(df):
#     reamining = [
#     "price",
#     "model",
#     "brand_model",
#     "category",
#     "fuel_type",
#     "manufacturer",
#     "prod_year",
#     "mileage_per_year"
# ]

#     return df[reamining]
