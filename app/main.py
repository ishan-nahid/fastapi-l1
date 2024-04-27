from http.client import HTTPException
from fastapi import FastAPI, Request
from dotenv import load_dotenv

from fastapi.templating import Jinja2Templates


import uvicorn


from BankNote import BankNote
import pickle
import pandas as pd
import numpy as np
from sklearn.svm import SVC

load_dotenv()
app = FastAPI()
template = Jinja2Templates(directory="templates")

pickle_in = open("classifier.pkl", "rb")
classifier = pickle.load(pickle_in)

@app.get('/')
def index(req: Request):
    return template.TemplateResponse(
        name="index.html",
        context = {"request" : req}
    )

DOGS = [{"name": "MILO", "TYPE": "GOLUMOLY"}, {"name": "MILO1", "TYPE": "GOLUMOL1"}, {"name": "MILO3", "TYPE": "GOLUMOLY3"}]
@app.get('/list')
def index(req: Request):
    return template.TemplateResponse(
        name="list.html",
        context = {"request" : req, "dogs":DOGS}
    )

@app.get('/input')
def input_form(request: Request):
    return template.TemplateResponse("input.html", {"request": request})

@app.post('/check')
def get_name(data: BankNote):
    try:
        data = data.dict()
        variense = data['varience']
        skewness = data['skewness']
        curtosis = data['curtosis']
        entropy  = data['entropy']

        prediction = classifier.predict([[variense, skewness, curtosis, entropy]])
        
        if(prediction[0] > 0.5):
            prediction = "Fake Note"
        else:
            prediction = "Bank Note"
        return {"prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    # return template.TemplateResponse(
    #     name="input.html",
    #     context={"request" : req}
    # )

if __name__ == "__main__":
    uvicorn.run("app.api:app", reload=True, port=PORT, host=HOST)