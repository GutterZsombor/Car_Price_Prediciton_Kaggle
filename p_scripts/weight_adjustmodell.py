from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import mutual_info_regression



#weight based on feature importance

def temporaryLinReg(df):
    
    #train a  baseline linear reg on the encoded dataset.
    #extract feature importance scores.
    #use those scores as weights for the categorical encodings.
    X = df.drop(columns=["price","color_enc"]) #color had to be tropped it trow everityng off
    y = df["price"]
    

    model = LinearRegression()
    model.fit(X, y)
   

    
    coefs = model.coef_

    return dict(zip(X.columns, abs(coefs)))


def categoryWeights(featurecoefs):
    weights = {}
    for name, importance in featurecoefs.items():
        if name.endswith("_enc"):
            col = name.replace("_enc", "")
            weights[col] = importance
    return weights


def normalizeWeights(weights):
    max_importance = max(weights.values())
    
    normalized = {
        col: importance / max_importance
        for col, importance in weights.items()
    }
    return normalized


def getweights(df):
    print("training temporary linreg for feature weighting.")

    #  feature importances
    coef = temporaryLinReg(df)
    
    
    cat_weights = categoryWeights(coef)

    normalized = normalizeWeights(cat_weights)


    print("\nWEIGHTS")
    for col, weight in sorted(normalized.items(), key=lambda x: -x[1]):
        print(f"{col:15s}  {weight:.3f}")
    print("\n")

    #I dont want it to run a lot of times but it can be integrated
    #return normalized

