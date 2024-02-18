import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

folder = 'marketplace-raw/'
file = '8th-Gen-Honda-Civic.csv'

df = pd.read_csv(folder+file)

print(df['Price'].corr(df['Mileage']))

sns.lmplot(x='Mileage', y='Price', data=df)
plt.show()

#Looking for any outliers in the data. 
