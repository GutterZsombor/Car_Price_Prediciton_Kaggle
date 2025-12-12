from EDA import createUsableData,heatMapforALL 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
import pandas as pd
import math
from weight_adjustmodell import getweights

from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Lasso
from sklearn.linear_model import LassoCV

if __name__ == "__main__":
    
    df_enc=createUsableData()
    corrM=heatMapforALL(df_enc,True,0.25)#,sgow:True

    #getweights(df_enc)

    #print(corrM)

   

    #Split into (scalr)y=price (vectro) X variable
    #now on scalr is lowercase 
    #vector/matrix Upper
    y = df_enc["price"]
    X = df_enc.drop(columns=["price"])
    X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42)
    #I tried Lasso
    #Did not effect performance
    #kept att bottm of file if needed

    
    
    #Linear Regression Modell
    linreg = LinearRegression()
    linreg.fit(X_train, y_train)
    y_pred = linreg.predict(X_test)
    #lets try polinomil instead of hyperplne 
    # degree 2: not big imporvement most of the stuff is already prety linear thats what is expected
    #degree 3: explodes
    #degree 4: better than 3 but still about x1000 times wors than linear wont persue
    # poly_lr = Pipeline([
    #     ("scale", StandardScaler()),
    #     ("poly", PolynomialFeatures(
    #         degree=4,        #  try 3 later
    #         include_bias=False
    #     )),
    #     ("model", LinearRegression())
    # ])

    # poly_lr.fit(X_train, y_train)

    # y_pred = poly_lr.predict(X_test)


    mse = mean_squared_error(y_test, y_pred)
    rmse = math.sqrt(mse)

    print("Linear Regression MSE:", mse)
    print("Linear Regression RMSE:", rmse)
    #Linear Regression RMSE: 40574.71690623211

    results = pd.DataFrame({
    "actual": y_test.values,
    "predicted": y_pred,
    "difference": y_test.values-y_pred
    })

    print(results.head(20))
#     '''
#     Loaded cars: 19237
#     Linear Regression RMSE: 40574.71690623211
#         actual     predicted
#     0   27284.0   7073.938135
#     1   10349.0  32446.388160
#     2   40769.0 -11057.207664
#     3   38737.0  48161.375703
#     4   42102.0  37053.620118
#     5   42400.0  39351.268551
#     6   18817.0  10863.246394
#     7   12858.0  24438.674140
#     8   10820.0  35363.096092
#     9   15367.0  41190.902640
#     10    627.0  19677.270962
#     11  16935.0  10320.066141
#     12    392.0   8211.114150
#     13   1725.0  23227.007036
#     14  49751.0  13755.001670
#     15  18817.0  29041.851721
#     16  34497.0  32641.183495
#     17  20071.0  23544.354675
#     18     90.0  19539.796445
#     19  18817.0   7703.134329
# '''

#Failed because car prices are non linear
#Pattern:

#Cheap cars  massively overpredicted

#Expensive cars  massively underpredicted

#Coleration heat map shows its not linear relation ship
#because manufacturer, model, cathegorie all correlate strongly with each other.
#No single feature has a strong linear correlation with price.
# price correlations are weak/moderate (0.25–0.39 range)


# Strong correlations appear BETWEEN categorical encodings:
# manufacturer_enc  model_enc
# model_enc  category_enc
# gear_box_type_enc prod_year and engine_volume
#  relationships are nonlinear and distort Linear Regression.

# engine volume and cylinders correlate strongly, but both correlate weakly with price.




#without certain values

    # y = df_enc["price"]
    # X = df_enc.drop(columns=["price","manufacturer_enc","model_enc","category_enc"])
    # X_train, X_test, y_train, y_test = train_test_split(
    # X,
    # y,
    # test_size=0.2,
    # random_state=42)

    # #Linear Regression Modell
    # linreg = LinearRegression()
    # linreg.fit(X_train, y_train)
    # y_pred = linreg.predict(X_test)

    # mse = mean_squared_error(y_test, y_pred)
    # rmse = math.sqrt(mse)

    # print("Linear Regression colums manu..., model, cat... dropped MSE:", mse)
    # print("Linear Regression manu..., model, cat... dropped RMSE:", rmse)
    # results = pd.DataFrame({
    # "actual": y_test.values,
    # "predicted": y_pred
    # })

    # #print(results.head(20))

    #Impoves linnear regression but still terrible


    #terrible beacuse of polinomility it exploed

    #  #Optimize linear reg with weight and log scale
    # #standardization / weighting of features

    # #polynomial  (degree=2)

    # y = np.log1p(df_enc["price"])   # log-transform
    # X = df_enc.drop(columns=["price"])
    # X_train, X_test, y_train, y_test = train_test_split(
    #     X, y, test_size=0.2, random_state=42
    # )

    # # Pipeline with polynomial interactions
    # model = Pipeline([
    #     ("scale", StandardScaler()),
    #     ("poly", PolynomialFeatures(degree=2, include_bias=False, interaction_only=True)),
    #     ("reg", Ridge(alpha=1.0))
    # ])
    # model.fit(X_train, y_train)

    # # Predict in log scale
    # y_pred_log = model.predict(X_test)

    # # Convert back
    # y_pred = np.expm1(y_pred_log)
    # y_test_real = np.expm1(y_test)

    # mse=mean_squared_error(y_test_real, y_pred)
    # rmse = math.sqrt(mse)
    # print("Optimized Linear Regression RMSE:", rmse)




    # #Lasso automatically zero-out useless coefficients
    # # lasso = Lasso(alpha=0.1)
    # # lasso.fit(X_train, y_train)

    # # keep_features = X.columns[lasso.coef_ != 0]

    # #same but with best alpha

    # lasso_cv = Pipeline([
    # ("scaler", StandardScaler()),
    # ("model", LassoCV(
    #     alphas=[0.0001, 0.0003, 0.001, 0.003, 0.01],
    #     cv=5,
    #     max_iter=10000
    #     ))
    # ])

    # lasso_cv.fit(X_train, y_train)

    # print("Best alpha:", lasso_cv.named_steps["model"].alpha_)

    #  # Extract coefficients from the CV model
    # scaler = lasso_cv.named_steps["scaler"]
    # lasso_model = lasso_cv.named_steps["model"]

    # coef = lasso_model.coef_
    # feature_names = X.columns

    # # Features LASSO keeps
    # usable = feature_names[np.abs(coef) > 1e-6]
    # #drop = feature_names[np.abs(coef) <= 1e-6]

    # X_train_reduced = X_train[usable]
    # X_test_reduced = X_test[usable]
