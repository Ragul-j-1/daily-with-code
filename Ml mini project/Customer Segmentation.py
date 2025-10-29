import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


df = pd.read_csv(r"D:\mater ai\Ml mini project\Datasets\Mall_Customers.csv")


x = df[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']]


scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)


model = KMeans(n_clusters=3, random_state=42)
df['cluster'] = model.fit_predict(x_scaled)


plt.scatter(df['Annual Income (k$)'], df['Spending Score (1-100)'], 
            c=df['cluster'], cmap='viridis')
plt.xlabel('Annual Income (k$)')
plt.ylabel('Spending Score (1-100)')
plt.title('Customer Segmentation using K-Means')
plt.show()
