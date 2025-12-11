import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def dispTablefromDict(dict):
   
    #Displays dictionary as a  pandas dataframe table
    
    #  dict to dataframe 
    df = pd.DataFrame.from_dict(dict, orient='index')

    # columnnames if values in lists
    if df.shape[1] > 1:
        df.columns = [f"Value{i+1}" for i in range(df.shape[1])]
    else:
        df.columns = ["Value"]

    print(df)


def priceDistriutionPlot(cars,scaleLog):



    #plot the price dist, optional log scale

    #Log scle needed because prices are high
    prices = [car.price for car in cars if car.price is not None] #None as usualy if missing hndle

    #s = pd.Series(prices) 


    #plt.figure(figsize=(10,5))
    if scaleLog:
        #on a log scale
        values = np.log(prices)
        x_label = "log(Price)"
        title = "Price Distribution (Log Scale)"

        #s.plot(kind="kde", label="KDE", linewidth=2)
    else:
       #without log
        values = prices
        x_label = "Price"
        title = "Price Distribution"

    plt.figure(figsize=(10,5))

    plt.hist(values, bins=50, alpha=0.6, density=True, label="Histogram")
    #kernel density estimate (KDE) https://en.wikipedia.org/wiki/Kernel_density_estimation
    s = pd.Series(values) 
    s.plot(kind="kde", linewidth=2, label="KDE")

    # plot details
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel("Density")
    plt.legend()
    plt.show()


def priceCorrelation(cars,efectpropertie ,heatmap=True):
    #how price efected by properties
    # correlation between price and numeric property

    # heatmap=True  correlation heatmap
    # heatmap=False  show pairplot

    #also works with nested data like engie.volume!

    data = {"price": [], efectpropertie: []}

    for car in cars:
        # price
        if car.price is None:
            continue
        
        price = car.price

        # nested properties (engine.volume)
        obj = car
        for part in efectpropertie.split("."):
            try:
                obj = getattr(obj, part)
            except AttributeError:
                obj = None
                break

        if obj is None:
            continue

        # values
        data["price"].append(price)
        data[efectpropertie].append(obj)


    #pd dataframe object
    df = pd.DataFrame(data)

    # correlation matrix https://www.w3schools.com/datascience/ds_stat_correlation_matrix.asp
    Corr_Matrix = df.corr()

    if heatmap:
        plt.figure(figsize=(6,4))
        sns.heatmap(Corr_Matrix,
                    annot=True,
                    cmap=sns.diverging_palette(50, 500, n=500),
                    square=True,
                    fmt=".2f")
        plt.title(f"Correlation Heatmap: price vs {efectpropertie}")
        plt.show()
    else:
        sns.pairplot(df)
        plt.suptitle(f"Pairplot: price vs {efectpropertie}", y=1.02)
        plt.show()


    #if Corr_Matrix needed at some point return
    return Corr_Matrix

def correlationHeatmap(df_numeric,clear=False,threshold=0.30):

    #instead of price vs single cathegori its the colaration of all
    
    Corr_Matrix = df_numeric.corr()
    if clear:
        #clean up Cor matrix only give the colaration where its meaningfull everywhere else0
        #for now threshold is set <=|30| colud be tweaked
        Corr_Matrix = Corr_Matrix.where(Corr_Matrix.abs() >= threshold, 0)
        
    plt.figure(figsize=(10, 6))
    sns.heatmap(Corr_Matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Heatmap")
    plt.show()
        #same as in price vs cathegorie collaration
        #if Corr_Matrix needed at some point return
    return Corr_Matrix
    
       


def plotCategoryDistribution(cars, attribute, top=20):
    #frequency distribution for string category.
    #eg: manufacturer and model

    values = [getattr(car, attribute) for car in cars if getattr(car, attribute) is not None]

    s = pd.Series(values)


    counts = s.value_counts().head(top)

    # Plot
    plt.figure(figsize=(10, 6))
    counts.sort_values().plot(kind="barh", color="skyblue")

    plt.title(f"Top {top} Most Common '{attribute}' Values")
    plt.xlabel("Frequency")
    plt.ylabel(attribute)

    plt.grid(axis="x", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

def plotAllCategoryDistributions(cars, top=20):


    
    #Runs plotategorydist for all categorical
    
    categorical_attributes = [
        "manufacturer",
        "model",
        "category",
        "leather_interior",
        "fuel_type",
        "gear_box_type",
        "drive_wheels",
        "doors",
        "wheel",
        "color"
    ]

    for attr in categorical_attributes:
        print(f"\n--- Plotting top {top} for {attr} ---\n")
        try:
            plotCategoryDistribution(cars, attr, top)
        except Exception as e:
            print(f"Error plotting '{attr}': {e}")