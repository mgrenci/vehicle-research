import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
from sklearn.metrics import mean_absolute_error

folder = 'marketplace-raw/'
file = '8th-Gen-Honda-Civic.csv'
new_folder = 'marketplace-cleaned/'
fig_file = '8th-Gen-Honda-Civic.png'

df = pd.read_csv(folder+file)
df = df.sort_values(by=['Mileage'])

X = df['Mileage']
y = df['Price']

X = np.array(X).reshape(-1,1)
y = np.array(y).reshape(-1,1)

poly_features = PolynomialFeatures(degree=3, include_bias=False)
X_poly = poly_features.fit_transform(X)

lr = LinearRegression()
lr.fit(X_poly, y)

X_vals = poly_features.transform(X)

y_pred = lr.predict(X_vals)

mae = mean_absolute_error(y, y_pred)

df['Retail'] = lr.predict(X_vals)
df['Retail'] = round(df['Retail'],2)
df['Upper'] = round(df['Retail'] + mae, 2)
df['Lower'] = round(df['Retail'] - mae, 2)

plt.scatter(X, y)
plt.plot(X, y_pred, color='r')
plt.plot(X, df['Upper'], label="Upper Variance", color='b', alpha=0.5)
plt.plot(X, df['Lower'], label="Lower Variance", color='b', alpha=0.5)
plt.savefig(new_folder+fig_file)
plt.show()

df['Return'] = round(df['Retail'] - df['Price'],2)
df['ROI'] = round((df['Retail'] / df['Price']), 2)
df = df.sort_values(by='Return', ascending=False)

df.to_csv(new_folder+file)

