import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import nltk
import string
"""nltk.download('stopwords')
nltk.download('wordnet')
"""

df = pd.read_csv(r"D:\mater ai\Ml mini project\Datasets\spam.csv",encoding='latin1')
lem=WordNetLemmatizer()

def preprocessing_text(text):
    text=re.sub(r'[!@#$%^&*]',"",text)
    
    text=re.sub(r'http\S+|www\S+|https\S+',"",text)
    text=re.sub(r'\d+',"",text)
    text = re.sub(r'[{}]'.format(re.escape(string.punctuation)), " ", text)
    
    text=text.lower()
    stopword=set(stopwords.words('english'))
    words=[word for word in text.split() if word not in stopword  ]
    words = [lem.lemmatize(word) for word in words]
    return " ".join(words)

from sklearn.feature_extraction.text import TfidfVectorizer
def vectorisation(text_data):
    
    vectoriser = TfidfVectorizer()
    X_vectors = vectoriser.fit_transform(text_data)  # convert text to numeric
    return vectoriser, X_vectors
    

df['cleaned_message']=df['message'].apply(preprocessing_text)



vectoriser, X = vectorisation(df['cleaned_message'])

y=df['label']




from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=40)

from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

model=MultinomialNB()

model.fit(x_train,y_train)

y_pred=model.predict(x_test)

print(y_pred)
print("accuracy:",accuracy_score(y_pred,y_test))

# Take input
new_message = input("Enter the message: ")

# Preprocess
pp_input = preprocessing_text(new_message)

# Transform using the already fitted vectoriser
vectorised_input = vectoriser.transform([pp_input])  # note: list []

# Predict
new_pred = model.predict(vectorised_input)
print("Prediction:", new_pred[0])
