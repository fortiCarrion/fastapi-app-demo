from typing import Union

from fastapi import FastAPI, Query
from pydantic import BaseModel
import requests

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool] = None

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.get('/api/restaurantes/')
def get_restaurantes(restaurante: str = Query(None)):
    '''
    Endpoint para ver os cardápios dos restaurantes  
    
    '''
    url = 'https://guilhermeonrails.github.io/api-restaurantes/restaurantes.json'
    response = requests.get(url)

    if response.status_code == 200:
        dados_json = response.json()
        if restaurante is None:
            return dados_json
        
        dados_restaurantes = []
        for item in dados_json:
            if item["Company"] == restaurante:
                dados_restaurantes.append(
                    {
                        "item": item["Item"],
                        "price": item["price"],
                        "description": item["description"]
                    }
                )
        return {"Restaurante": restaurante, "Cardapio": dados_restaurantes}
    
    else:
        print(f"O erro foi {response.status_code} - {response.text}")

