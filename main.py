from fastapi import FastAPI
import uvicorn
from key import Keyword_Spotting_Service
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
def Hello():
    return {'Hello':'Hello'}

@app.post('/predict')
def predict(path:str):
    kss = Keyword_Spotting_Service()
    keyword1,keyword2= kss.prediction(path)
    return {"prediction":keyword1}

# @app.post('/value')
# def value(path:Path):
#     kss = Keyword_Spotting_Service()
#     keyword1,keyword2 = kss.prediction(path.path)
#     return keyword2


if __name__ == "__main__":
    uvicorn.run(app,host='127.0.0.1',port=8000)