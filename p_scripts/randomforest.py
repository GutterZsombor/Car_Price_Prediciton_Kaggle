from EDA import createUsableData,heatMapforALL 
from sklearn.model_selection import train_test_split

from sklearn.metrics import mean_squared_error
import numpy as np
import pandas as pd
import math
from sklearn.ensemble import RandomForestRegressor
from encode_string import encodeallStrings
from weight_adjustmodell import getweights

if __name__ == "__main__":
    
    df_enc=createUsableData()
    corrM=heatMapforALL(df_enc,True,0.25)#,sgow:True
    #print(corrM)

    #Split into (scalr)y=price (vectro) X variable
    #now on scalr is lowercase 
    #vector/matrix Upper
    y = df_enc["price"]
    X = df_enc.drop(columns=["price"])
    # y_log = np.log1p(y)
    # X_train, X_test, y_train_log, y_test_log = train_test_split(
    # X,
    # y_log,
    # test_size=0.2,
    # random_state=42
    # )

    X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42)
    #imporve rf

    rf = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    max_depth=20, #significant improvement form None-30-20
    n_jobs=-1,
    
    )
    # #imporvement1 DIDNT WORK
    # rf = RandomForestRegressor(
    # n_estimators=600, #reduces noise
    # max_depth=None,
    # min_samples_split=8, #prevents splits on too small samples
    # min_samples_leaf=3,
    # max_features="sqrt", #"best for regression RF" not sure
    # bootstrap=True,
    # n_jobs=-1,
    # random_state=42
    # )

    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test)
    #imporvement 2 -DIDnt WOKR
    #log prices
    # rf.fit(X_train, y_train_log)

    # # predict in LOG scale
    # y_pred_log = rf.predict(X_test)

    # #convert back to real scale
    # y_test_real = np.expm1(y_test_log)
    # y_pred_real = np.expm1(y_pred_log)

    mse=mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)

    print("Random Forest RMSE:", rmse)

    results = pd.DataFrame({
    "actual":y_test.values,
    "predicted": y_pred,
    "difference": y_test.values-y_pred
    })

    print(results.head(20))
    #getweights(df_enc)
