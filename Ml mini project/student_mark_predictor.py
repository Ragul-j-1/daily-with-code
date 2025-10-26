from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error,r2_score
import pandas as pd
import numpy as np
df=pd.read_csv("score.csv")
x=df[['Hours']]
y=df['Scores']

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=40)

model=LinearRegression()

model.fit(x_train,y_train)

# y_pred=model.predict(x_test)
# mse=mean_squared_error(y_test,y_pred)

inp=float(input("enter tthe hour"))
i=model.predict([[inp]])
print(i)


