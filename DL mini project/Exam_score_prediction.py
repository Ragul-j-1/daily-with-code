import torch as pt
import torch.nn as nn 
import pandas as pd

df=pd.read_csv(r"D:\mater ai\DL mini project\datasets\Exam_Score_Prediction.csv")
x=df[["study_hours"]].values
y=df[["exam_score"]].values


X=pt.tensor(x,dtype=pt.float32)
Y=pt.tensor(y,dtype=pt.float32).view(-1,1)

n_samples,n_features=X.shape

input_size=n_features
output_size=n_features

model=nn.Linear(input_size,output_size)

loss=nn.MSELoss()



n_iteration=100
learning_rate=0.01
optimization=pt.optim.SGD(model.parameters(),lr=learning_rate)

for epoch in range(n_iteration):
    y_pred=model(X)
    
    l=loss(y_pred,Y)
    
    l.backward()
    
    optimization.step()
    
    optimization.zero_grad()
    
    if epoch % 10 ==0:
        [w,b]=model.parameters()
        print(f"epoch {epoch+1}:w={w[0][0].item():.3f},loss={l:.8f}")