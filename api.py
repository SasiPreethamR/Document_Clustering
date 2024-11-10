import faiss
import torch
import numpy as np
import requests
import json
from traceback import format_exc
import time


def classify(zeroshot_classifier, doc):
    articles = ['technology','business', 'science','sports','current affairs']
    hypothesis_template = "This example is about {}"
    classes_verbalised = articles
    output = zeroshot_classifier(doc, classes_verbalised, hypothesis_template=hypothesis_template, multi_label=False)
    return output['labels'][0]



############################################################################################################


# FAST API SERVER


############################################################################################################


from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict
from transformers import pipeline

app = FastAPI()

zeroshot_classifier = pipeline("zero-shot-classification", model="MoritzLaurer/deberta-v3-large-zeroshot-v1.1-all-33", device=1)


class RequestModel(BaseModel):
    document: str

class ResponseModel(BaseModel):
    result: Any

@app.post("/cluster", response_model=ResponseModel)
async def t2sql(request: RequestModel):
    try:
        doc = request.document
        result = classify(zeroshot_classifier, doc)
        return {'result':result}
    except:
        format_exc()
        return {"result":{'status':'Failure'}}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=83333)
