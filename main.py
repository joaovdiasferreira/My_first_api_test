from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import TypedDict
app = FastAPI()

#ModelBase
class Sale(BaseModel):
    product: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0, lt=100000)
    quantity: int = Field(gt=0, lt=1000)
    #Field helps to limit space usage or possible errors

#RespondeModel or output model
class SaleResponse(Sale): #inhirits everything from Sale
    id: int
    total: float

#Input model
class SaleCreate(Sale):
    pass

class SaleDict(TypedDict):
    product: str
    price: float
    quantity: int
    total: float


#Fake database
sales: dict[int, SaleDict] = { #This turns the dict a bit restrictive
    1: {
        "product": "Keyboard",
        "price": 150.0,
        "quantity": 2,
        "total": 300.0
    },
    2: {
        "product": "Mouse",
        "price": 80.0,
        "quantity": 1,
        "total": 80.0
    },
    3: {
        "product": "Monitor",
        "price": 900.0,
        "quantity": 1,
        "total": 900.0
    },
    4: {
        "product": "Headset",
        "price": 200.0,
        "quantity": 1,
        "total": 200.0
    }
}


#Helper functions
def calculate_total(price: float, quantity: int) -> float:
    return price * quantity
    #total is calculated sometimes in the code



#Routes
@app.get("/")
def home():
    return {"message": "My first API is running!"}

@app.get("/sales", response_model=list[SaleResponse])
def get_sales():
    return [{"id": sale_id, **sale} for sale_id, sale in sales.items()]

@app.get("/sales/{sale_id}", response_model=SaleResponse)
def get_sale(sale_id: int):
    sale = sales.get(sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
        #This prevents KeyError if a sale is not found
    return {"id": sale_id, **sale}


#CREAT a sale (POST)
@app.post("/sales", response_model=SaleResponse)
def create_sale(sale: SaleCreate):
    sale_id = max(sales.keys(), default=0) + 1 #this avoids that an id repeat
    total = calculate_total(sale.price, sale.quantity)

    sales[sale_id]= {
        "product": sale.product,
        "price": sale.price,
        "quantity": sale.quantity,
        "total": total
    }
    return {"id": sale_id, **sales[sale_id]}


@app.put("/sales/{sale_id}", response_model=SaleResponse)
#UPDATE a sale (PUT)
def update_sale(sale_id: int, sale: SaleCreate):
    if sale_id not in sales:
        raise HTTPException(status_code=404, detail="Sale not found")
    total = calculate_total(sale.price, sale.quantity)

    sales[sale_id] = {
        "product": sale.product,
        "price": sale.price,
        "quantity": sale.quantity,
        "total": total
    }
    return {"id": sale_id, **sales[sale_id]}


#DELETE a sale
@app.delete("/sales/{sale_id}")
def delete_sale(sale_id: int):
    if sale_id not in sales:
        raise HTTPException(status_code=404, detail="Sale not found")
    deleted = sales.pop(sale_id) #pop() returns what was deleted
    #del sales[sale_id] is possible, but it not returns anything
    return {"message": "Sale deleted!", "data":{"id": sale_id, **deleted}}
