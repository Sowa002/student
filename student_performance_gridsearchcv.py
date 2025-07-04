from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, GridSearchCV

from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import BayesianRidge
from catboost import CatBoostRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.linear_model import HuberRegressor
from sklearn.linear_model import TheilSenRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

from sklearn.metrics import mean_squared_error, r2_score

df = pd.read_csv("StudentPerformanceFactors.csv")
df

df.shape

df.info()

df.describe()

cols_with_nulls = df.columns[df.isnull().sum() > 0]

df = df.dropna(subset=cols_with_nulls).reset_index(drop=True)
df

df.duplicated().sum()

df.nunique()

object_features = df.select_dtypes(include='object')
numerical_features = df.select_dtypes(exclude='object')

fig, axes = plt.subplots(nrows=len(numerical_features.columns),figsize=(5,30))
axes = axes.flatten()
fig.subplots_adjust(hspace=.1)
for i,col in enumerate(numerical_features.columns):
    ax = axes[i]
    ax.boxplot(numerical_features[col],flierprops=dict(marker='o', color='red', markersize=5))
    ax.set_title(col)
    ax.set_xlabel(col)
    ax.set_ylabel("Frequency")

fig, axes = plt.subplots(nrows=len(numerical_features.columns),figsize=(5,30))
axes = axes.flatten()
fig.subplots_adjust(hspace=.1)
for i,col in enumerate(numerical_features.columns):
    ax = axes[i]
    ax.hist(numerical_features[col],bins=50,alpha=0.7,edgecolor='black')
    ax.set_title(col)
    ax.set_xlabel(col)
    ax.set_ylabel("Frequency")

z = np.abs((numerical_features - numerical_features.mean()) / numerical_features.std())
threshold = 3
numerical_features= numerical_features[(z < threshold).all(axis=1)]
object_features = object_features.iloc[numerical_features.index]

encoder = LabelEncoder()
for col in object_features.columns:
    object_features[col] = encoder.fit_transform(object_features[col])

df = pd.concat([object_features,numerical_features],axis=1).reset_index(drop=True)

plt.figure(figsize=(10, 10))
sns.heatmap(df.corr(), annot=True, fmt=".2f", cbar=False, xticklabels=df.columns, yticklabels=df.columns)
plt.show()

X = df.drop("Exam_Score",axis=1)
y = df['Exam_Score']

# 3. Split data menjadi train dan test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

"""**1. Linier Regression**"""

# 4. Definisi model dan parameter grid
lr_param_grid = {'fit_intercept': [True, False]}
lr_grid = GridSearchCV(LinearRegression(), lr_param_grid, scoring='r2', cv=5)

# 5. Fit model dengan grid search
lr_grid.fit(X_train, y_train)

preds = lr_grid.predict(X_test)
print("LinierR Best Params:", lr_grid.best_params_)
lr_grid_score = r2_score(y_test, preds)
lr_grid_mse = mean_squared_error(y_test, preds)
lr_grid_rmse = np.sqrt(mean_squared_error(y_test, preds))

print("LinierR Test R²:", round(lr_grid_score,2))
print("LinierR Test MSE:", round(lr_grid_mse,5))
print("LinierR Test RMSE:", round(lr_grid_rmse,5))

"""**2. SVM**"""

SVM_param_grid = {'C': [0.1, 1, 10], 'epsilon': [0.1, 0.2], 'kernel': ['linear', 'rbf']}
SVM_grid = GridSearchCV(SVR(), SVM_param_grid, scoring='r2', cv=5)

SVM_grid.fit(X_train, y_train)

preds = SVM_grid.predict(X_test)
print("SVM Best Params:", SVM_grid.best_params_)
SVM_grid_score = r2_score(y_test, preds)
SVM_grid_mse = mean_squared_error(y_test, preds)
SVM_grid_rmse = np.sqrt(mean_squared_error(y_test, preds))

print("LinierR Test R²:", round(SVM_grid_score,2))
print("LinierR Test MSE:", round(SVM_grid_mse,5))
print("LinierR Test RMSE:", round(SVM_grid_rmse,5))

"""**3. Decision Tree Regressor**"""

DT_param_grid = {'max_depth': [3, 5, None], 'min_samples_split': [2, 10]}
DT_grid = GridSearchCV(DecisionTreeRegressor(random_state=42), DT_param_grid, scoring='r2', cv=5)

DT_grid.fit(X_train, y_train)

preds = DT_grid.predict(X_test)
print("DT Best Params:", DT_grid.best_params_)
DT_grid_score = r2_score(y_test, preds)
DT_grid_mse = mean_squared_error(y_test, preds)
DT_grid_rmse = np.sqrt(mean_squared_error(y_test, preds))

print("Decission Tree Test R²:", round(DT_grid_score,2))
print("Decission Tree Test MSE:", round(DT_grid_mse,5))
print("Decission Tree Test RMSE:", round(DT_grid_rmse,5))

"""**4. Random Forest Regressor**"""

RF_param_grid = {'n_estimators': [50, 100], 'max_depth': [3, 5, None]}
RF_grid = GridSearchCV(RandomForestRegressor(random_state=42), RF_param_grid, scoring='r2', cv=5)

RF_grid.fit(X_train, y_train)

preds = RF_grid.predict(X_test)
print("RF Best Params:", RF_grid.best_params_)
RF_grid_score = r2_score(y_test, preds)
RF_grid_mse = mean_squared_error(y_test, preds)
RF_grid_rmse = np.sqrt(mean_squared_error(y_test, preds))

print("Random Forest Test R²:", round(RF_grid_score,2))
print("Random Forest Test MSE:", round(RF_grid_mse,5))
print("Random Forest Test RMSE:", round(RF_grid_rmse,5))

"""**5. XGBoost Regressor**"""

XGB_param_grid = {'n_estimators': [50, 100], 'learning_rate': [0.01, 0.1], 'max_depth': [3, 5]}
XGB_grid = GridSearchCV(XGBRegressor(random_state=42), XGB_param_grid, scoring='r2', cv=5)

XGB_grid.fit(X_train, y_train)

preds = XGB_grid.predict(X_test)
print("XGB Best Params:", XGB_grid.best_params_)
XGB_grid_score = r2_score(y_test, preds)
XGB_grid_mse = mean_squared_error(y_test, preds)
XGB_grid_rmse = np.sqrt(mean_squared_error(y_test, preds))

print("XGBoost Test R²:", round(XGB_grid_score,2))
print("XGBoost Test MSE:", round(XGB_grid_mse,5))
print("XGBoost Test RMSE:", round(XGB_grid_rmse,5))

"""**6. LightGBM Regressor**"""

LGB_param_grid = {'n_estimators': [50, 100], 'learning_rate': [0.01, 0.1], 'num_leaves': [20, 31]}
LGB_grid = GridSearchCV(LGBMRegressor(random_state=42), LGB_param_grid, scoring='r2', cv=5)

LGB_grid.fit(X_train, y_train)

preds = LGB_grid.predict(X_test)
print("LGB Best Params:", LGB_grid.best_params_)
LGB_grid_score = r2_score(y_test, preds)
LGB_grid_mse = mean_squared_error(y_test, preds)
LGB_grid_rmse = np.sqrt(mean_squared_error(y_test, preds))

print("LGB Test R²:", round(LGB_grid_score,2))
print("LGB Test MSE:", round(LGB_grid_mse,5))
print("LGB Test RMSE:", round(LGB_grid_rmse,5))

"""**7. K-Nearest Neighbors (KNN) Regressor**"""

KNN_param_grid = {'n_neighbors': [3, 5, 7], 'weights': ['uniform', 'distance']}
KNN_grid = GridSearchCV(KNeighborsRegressor(), KNN_param_grid, scoring='r2', cv=5)

KNN_grid.fit(X_train, y_train)

preds = KNN_grid.predict(X_test)
print("KNN Best Params:", KNN_grid.best_params_)
KNN_grid_score = r2_score(y_test, preds)
KNN_grid_mse = mean_squared_error(y_test, preds)
KNN_grid_rmse = np.sqrt(mean_squared_error(y_test, preds))

print("KNN Test R²:", round(KNN_grid_score,2))
print("KNN Test MSE:", round(KNN_grid_mse,5))
print("KNN Test RMSE:", round(KNN_grid_rmse,5))

"""**8. Ridge Regression**"""

Ridge_param_grid = {'alpha': [0.1, 1.0, 10.0]}
Ridge_grid = GridSearchCV(Ridge(), Ridge_param_grid, scoring='r2', cv=5)

Ridge_grid.fit(X_train, y_train)

preds = Ridge_grid.predict(X_test)
print("Ridge Best Params:", Ridge_grid.best_params_)
Ridge_grid_score = r2_score(y_test, preds)
Ridge_grid_mse = mean_squared_error(y_test, preds)
Ridge_grid_rmse = np.sqrt(mean_squared_error(y_test, preds))

print("Ridge Test R²:", round(Ridge_grid_score,2))
print("Ridge Test MSE:", round(Ridge_grid_mse,5))
print("Ridge Test RMSE:", round(Ridge_grid_rmse,5))

"""**9. Lasso Regression**"""

Lasso_param_grid = {'alpha': [0.01, 0.1, 1.0]}
Lasso_grid = GridSearchCV(Lasso(max_iter=10000), Lasso_param_grid, scoring='r2', cv=5)

Lasso_grid.fit(X_train, y_train)

preds = Lasso_grid.predict(X_test)
print("Lasso Best Params:", Lasso_grid.best_params_)
Lasso_grid_score = r2_score(y_test, preds)
Lasso_grid_mse = mean_squared_error(y_test, preds)
Lasso_grid_rmse = np.sqrt(mean_squared_error(y_test, preds))

print("Lasso Test R²:", round(Lasso_grid_score,2))
print("Lasso Test MSE:", round(Lasso_grid_mse,5))
print("Lasso Test RMSE:", round(Lasso_grid_rmse,5))

"""**10. ElasticNet Regression**"""

Elastic_param_grid = {'alpha': [0.01, 0.1, 1.0], 'l1_ratio': [0.3, 0.5, 0.7]}
Elastic_grid = GridSearchCV(ElasticNet(max_iter=10000), Elastic_param_grid, scoring='r2', cv=5)

Elastic_grid.fit(X_train, y_train)

preds = Elastic_grid.predict(X_test)
print("Elastic Best Params:", Elastic_grid.best_params_)
Elastic_grid_score = r2_score(y_test, preds)
Elastic_grid_mse = mean_squared_error(y_test, preds)
Elastic_grid_rmse = np.sqrt(mean_squared_error(y_test, preds))

print("Elastic Test R²:", round(Elastic_grid_score,2))
print("Elastic Test MSE:", round(Elastic_grid_mse,5))
print("Elastic Test RMSE:", round(Elastic_grid_rmse,5))

"""**11. Gradient Boosting Regressor**"""

GBR_param_grid = {'n_estimators': [50, 100], 'learning_rate': [0.01, 0.1], 'max_depth': [3, 5]}
GBR_grid = GridSearchCV(GradientBoostingRegressor(random_state=42), GBR_param_grid, scoring='r2', cv=5)

GBR_grid.fit(X_train, y_train)

preds = GBR_grid.predict(X_test)
print("GBR Best Params:", GBR_grid.best_params_)
GBR_grid_score = r2_score(y_test, preds)
GBR_grid_mse = mean_squared_error(y_test, preds)
GBR_grid_rmse = np.sqrt(mean_squared_error(y_test, preds))

print("GBR Test R²:", round(GBR_grid_score,2))
print("GBR Test MSE:", round(GBR_grid_mse,5))
print("GBR Test RMSE:", round(GBR_grid_rmse,5))

"""**12. Bayesian Ridge Regression**"""

Bayes_param_grid = {'alpha_1': [1e-6, 1e-5], 'lambda_1': [1e-6, 1e-5]}
Bayes_grid = GridSearchCV(BayesianRidge(), Bayes_param_grid, scoring='r2', cv=5)

Bayes_grid.fit(X_train, y_train)

preds = Bayes_grid.predict(X_test)
print("Bayes Best Params:", Bayes_grid.best_params_)
Bayes_grid_score = r2_score(y_test, preds)
Bayes_grid_mse = mean_squared_error(y_test, preds)
Bayes_grid_rmse = np.sqrt(mean_squared_error(y_test, preds))

print("Bayes Test R²:", round(Bayes_grid_score,2))
print("Bayes Test MSE:", round(Bayes_grid_mse,5))
print("Bayes Test RMSE:", round(Bayes_grid_rmse,5))

"""**13. CatBoost Regressor**"""

Catboost_param_grid = {'iterations': [50, 100], 'learning_rate': [0.01, 0.1], 'depth': [4, 6]}
Catboost_grid = GridSearchCV(CatBoostRegressor(silent=True), Catboost_param_grid, scoring='r2', cv=5)

Catboost_grid.fit(X_train, y_train)

preds = Catboost_grid.predict(X_test)
print("CatBoost Best Params:", Catboost_grid.best_params_)
Catboost_grid_score = r2_score(y_test, preds)
Catboost_grid_mse = mean_squared_error(y_test, preds)
Catboost_grid_rmse = np.sqrt(mean_squared_error(y_test, preds))

print("CatBoost Test R²:", round(Catboost_grid_score,2))
print("CatBoost Test MSE:", round(Catboost_grid_mse,5))
print("CatBoost Test RMSE:", round(Catboost_grid_rmse,5))

"""**14. MLP Regressor (Neural Network)**"""

MLP_param_grid = {'hidden_layer_sizes': [(50,), (100,)], 'activation': ['relu', 'tanh'], 'alpha': [0.001, 0.01]}
MLP_grid = GridSearchCV(MLPRegressor(max_iter=1000, random_state=42), MLP_param_grid, scoring='r2', cv=5)

MLP_grid.fit(X_train, y_train)

preds = MLP_grid.predict(X_test)
print("MLP Best Params:", MLP_grid.best_params_)
MLP_grid_score = r2_score(y_test, preds)
MLP_grid_mse = mean_squared_error(y_test, preds)
MLP_grid_rmse = np.sqrt(mean_squared_error(y_test, preds))

print("MLP Test R²:", round(MLP_grid_score,2))
print("MLP Test MSE:", round(MLP_grid_mse,5))
print("MLP Test RMSE:", round(MLP_grid_rmse,5))

"""**15. AdaBoost Regressor**"""

Adaboost_param_grid = {'n_estimators': [50, 100], 'learning_rate': [0.01, 0.1]}
Adaboost_grid = GridSearchCV(AdaBoostRegressor(random_state=42), Adaboost_param_grid, scoring='r2', cv=5)

Adaboost_grid.fit(X_train, y_train)

preds = Adaboost_grid.predict(X_test)
print("AdaBoost Best Params:", Adaboost_grid.best_params_)
Adaboost_grid_score = r2_score(y_test, preds)
Adaboost_grid_mse = mean_squared_error(y_test, preds)
Adaboost_grid_rmse = np.sqrt(mean_squared_error(y_test, preds))

print("AdaBoost Test R²:", round(Adaboost_grid_score,2))
print("AdaBoost Test MSE:", round(Adaboost_grid_mse,5))
print("AdaBoost Test RMSE:", round(Adaboost_grid_rmse,5))

"""**16. Huber Regressor**"""

Huber_param_grid = {'epsilon': [1.1, 1.35, 1.5], 'alpha': [0.0001, 0.001]}
Huber_grid = GridSearchCV(HuberRegressor(max_iter=1000), Huber_param_grid, scoring='r2', cv=5)

Huber_grid.fit(X_train, y_train)

preds = Huber_grid.predict(X_test)
print("Huber Best Params:", Huber_grid.best_params_)
Huber_grid_score = r2_score(y_test, preds)
Huber_grid_mse = mean_squared_error(y_test, preds)
Huber_grid_rmse = np.sqrt(mean_squared_error(y_test, preds))

print("Huber Test R²:", round(Huber_grid_score,2))
print("Huber Test MSE:", round(Huber_grid_mse,5))
print("Huber Test RMSE:", round(Huber_grid_rmse,5))

"""**17. Theil-Sen Regressor**"""

TheilSen_param_grid = {'fit_intercept': [True, False]}
TheilSen_grid = GridSearchCV(TheilSenRegressor(random_state=42), TheilSen_param_grid, scoring='r2', cv=5)

TheilSen_grid.fit(X_train, y_train)

preds = TheilSen_grid.predict(X_test)
print("KNN Best Params:", TheilSen_grid.best_params_)
TheilSen_grid_score = r2_score(y_test, preds)
TheilSen_grid_mse = mean_squared_error(y_test, preds)
TheilSen_grid_rmse = np.sqrt(mean_squared_error(y_test, preds))

print("TheilSen Test R²:", round(TheilSen_grid_score,2))
print("TheilSen Test MSE:", round(TheilSen_grid_mse,5))
print("TheilSen Test RMSE:", round(TheilSen_grid_rmse,5))

"""**18. Polynomial Regression**"""

degrees = [1, 2]
best_r2 = -np.inf
best_degree = 1

poly_models = {}

for d in degrees:
    # Buat model pipeline
    model = make_pipeline(PolynomialFeatures(degree=d, include_bias=False),
                          LinearRegression())
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    # Hitung metrik
    poly_score = r2_score(y_test, preds)
    poly_mse = mean_squared_error(y_test, preds)
    poly_rmse = np.sqrt(poly_mse)

    # Simpan ke dictionary
    poly_models[f"Poly_deg_{d}"] = {
        "model": model,
        "score": poly_score,
        "mse": poly_mse,
        "rmse": poly_rmse
    }

# Print hasil
print(f"Poly Degree {d} Test R²: {poly_score:.2f}, MSE: {poly_mse:.5f}, RMSE: {poly_rmse:.5f}")

"""# **Evaluasi**"""

results = pd.DataFrame({
    "Model": [
        "LR", "SVR", "DTREE", "RF", "XGB", "LGB", "KNN", "Ridge", "Lasso",
        "ElasticNet", "Gradient Boosting", "Bayesian Ridge", "CatBoost",
        "MLP", "AdaBoost", "Huber", "TheilSen", "Polynomial"
    ],
    "R2_Scores": [
        lr_grid_score, SVM_grid_score, DT_grid_score, RF_grid_score, XGB_grid_score, LGB_grid_score,
        KNN_grid_score, Ridge_grid_score, Lasso_grid_score, Elastic_grid_score,
        GBR_grid_score, Bayes_grid_score, Catboost_grid_score, MLP_grid_score,
        Adaboost_grid_score, Huber_grid_score, TheilSen_grid_score, poly_score
    ],
    "MSE": [
        lr_grid_mse, SVM_grid_mse, DT_grid_mse, RF_grid_mse, XGB_grid_mse,
        LGB_grid_mse, KNN_grid_mse, Ridge_grid_mse, Lasso_grid_mse, Elastic_grid_mse,
        GBR_grid_mse, Bayes_grid_mse, Catboost_grid_mse, MLP_grid_mse,
        Adaboost_grid_mse, Huber_grid_mse, TheilSen_grid_mse, poly_mse
    ],
    "RMSE": [
        lr_grid_rmse, SVM_grid_rmse, DT_grid_rmse, RF_grid_rmse, XGB_grid_rmse, LGB_grid_rmse,
        KNN_grid_rmse, Ridge_grid_rmse, Lasso_grid_rmse, Elastic_grid_rmse,
        GBR_grid_rmse, Bayes_grid_rmse, Catboost_grid_rmse, MLP_grid_rmse,
        Adaboost_grid_rmse, Huber_grid_rmse, TheilSen_grid_rmse, poly_rmse
    ],
})

import matplotlib.pyplot as plt
import seaborn as sns

# Setup figure
plt.figure(figsize=(12, 6))

# Definisi palet warna
palette = sns.color_palette("pastel", len(results['Model'].unique()))

# Plot R² Scores
sns.barplot(x="Model", y="R2_Scores", data=results, palette=palette, edgecolor='k')
plt.title("R² Scores", fontsize=14)
plt.xlabel("Model", fontsize=12)
plt.ylabel("R² Score", fontsize=12)
plt.xticks(rotation=45)

# Tampilkan grafik
plt.tight_layout()
plt.show()

# Setup figure baru
plt.figure(figsize=(12, 6))

# Plot Mean Squared Error (MSE)
sns.barplot(x="Model", y="MSE", data=results, palette=palette, edgecolor='k')
plt.title("Mean Squared Error (MSE)", fontsize=14)
plt.xlabel("Model", fontsize=12)
plt.ylabel("MSE", fontsize=12)
plt.xticks(rotation=45)

# Tampilkan grafik
plt.tight_layout()
plt.show()

# Setup figure baru
plt.figure(figsize=(12, 6))

# Plot Root Mean Squared Error (RMSE)
sns.barplot(x="Model", y="RMSE", data=results, palette=palette, edgecolor='k')
plt.title("Root Mean Squared Error (RMSE)", fontsize=14)
plt.xlabel("Model", fontsize=12)
plt.ylabel("RMSE", fontsize=12)
plt.xticks(rotation=45)

# Tampilkan grafik
plt.tight_layout()
plt.show()
