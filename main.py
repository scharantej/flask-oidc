 
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler

# load the model
model = joblib.load('model.pkl')

# create a Flask app
app = Flask(__name__)

# define the home route
@app.route('/')
def home():
    return render_template('index.html')

# define the predict route
@app.route('/predict', methods=['POST'])
def predict():
    # get the SMILES string from the request
    smiles = request.form['smiles']

    # preprocess the SMILES string
    smiles = smiles.strip()
    smiles = smiles.upper()

    # convert the SMILES string to a vector
    vectorizer = joblib.load('vectorizer.pkl')
    vector = vectorizer.transform([smiles])

    # scale the vector
    scaler = joblib.load('scaler.pkl')
    vector = scaler.transform(vector)

    # predict the toxicity of the compound
    prediction = model.predict(vector)

    # return the prediction
    return render_template('results.html', prediction=prediction)

# define the about route
@app.route('/about')
def about():
    return render_template('about.html')

# run the app
if __name__ == '__main__':
    app.run()
