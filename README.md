Car Price Prediction

A data-driven regression project using feature engineering and scikit-learn.

Overview

This project predicts used car prices using the Car Price Prediction Challenge dataset from Kaggle.
The goal was to build a model capable of achieving 80% prediction precision using real, messy market data.

The workflow covers:

Data handling and cleaning

Exploratory data analysis (EDA)

Custom mean-price encoder

Feature engineering

Linear Regression and Random Forest models

Evaluation using RMSE and relative precision

A complete PDF report is included in the repository.

Repository Structure
Car-Price-Prediction/
│
├── src/
│   ├── EDA.py
│   ├── encoder.py
│   ├── weight_adjustmodell.py
│   ├── train_models.py
│   └── utils/
│
├── figures/
├── data/
│
├── report/
│   └── Programming_Assignment_2025.pdf
│
└── README.md

Key Components
1. Custom Mean-Price Encoder

Categorical columns (manufacturer, model, fuel type, gearbox, etc.) are encoded using the
mean price of each category rather than integer labels.
This avoids introducing false numerical orderings and stabilizes regression performance.

2. Feature Engineering

Several engineered features significantly improved prediction quality:

brand_model — distinguishes within-brand price variation (e.g., BMW X5 vs BMW 3-series)

car_age — captures depreciation

mileage_per_year — normalizes mileage by age

These became some of the strongest predictors for both models.

3. Filtering & Outlier Removal

The price distribution is extremely skewed. Using log-price thresholds helps isolate realistic listings:

ln(price) > 7 → removes cars under ~1100 USD

ln(price) > 8 → removes cars under ~3000 USD

This excludes scrap-value cars and extreme outliers that distort regression.

4. Exploratory Data Analysis (EDA)

Key visualizations include:

Full correlation heatmap

Price distribution histogram

Manufacturer frequency distribution

Pairwise relationships

These guided every filtering and encoding decision.

Models Used

Both models were implemented with scikit-learn:

Linear Regression

Simple, interpretable baseline

Coefficients allow insight into feature influence

Struggles with non-linear relationships and outliers

Random Forest Regression

Non-linear ensemble model

Handles heterogeneous, noisy data better

Consistently stronger performance in RMSE and relative precision

Results Summary
Metrics used

RMSE (root mean squared error)

Mean absolute relative error

Median absolute relative error

Relative precision = 100% − error

Best model

Random Forest Regression with ln(price) > 7

RMSE ≈ 4600–5000

Median precision ≈ 90%

Best balance between dataset size and prediction stability

Linear Regression

Median precision ~70–75%

Mean precision much lower due to rare but very large errors

Did not reach the 80% target without heavy filtering

Lessons Learned

Data quality determines accuracy more than the choice of model

Mean-price encoding is far more effective than integer encoding

Pairwise correlations hide indirect relationships exposed in the full heatmap

Many online examples reach 80% precision only by extreme filtering, which reduces realism

Random Forest is much better suited to this dataset than Linear Regression

Future Work

Deploy a car-pricing web API (prototype started; production delayed until accuracy improves)

Separate models for low-, mid-, and high-value vehicles

Combine multiple datasets for richer training data

Improve OOP structure for scalability

Explore more advanced models (Gradient Boosting, XGBoost, CatBoost, etc.)

Running the Project
Install dependencies


Train the models
python linearregression.py 
or
python randomforest.py 


Dataset

Kaggle: Car Price Prediction Challenge
https://www.kaggle.com/datasets/deepcontractor/car-price-prediction-challenge

Full Report + REFERENCES

See:
.pdf
