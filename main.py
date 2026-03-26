from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
app = FastAPI()


#Model
class Sale(BaseModel):
    product: str
    price: float = Field(gt=0)
    quantity: int = Field(gt=0)


#Fake database
sales = {
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


#Routers
@app.get("/")
def home():
    return {"My first API is running!"}

@app.get("/sales")
def get_sales():
    return sales

@app.get("/sales/{sale_id}")
def get_sale(sale_id: int):
    if sale_id not in sales:
        raise HTTPException(status_code=404, detail="Sale not found")
        #This prevents KeyError if a sale is not found

    return sales[sale_id]


#CREAT a sale (POST)
@app.post("/sales")
def create_sale(sale: Sale):
    sale_id = len(sales)+1
    total = sale.price * sale.quantity

    sales[sale_id]= {
        "product": sale.product,
        "price": sale.price,
        "quantity": sale.quantity,
        "total": total
    }
    return {"id": sale_id, "sale": sales[sale_id]}

#DELETE a sale
@app.delete("/sales/{sale_id}")
def delete_sale(sale_id: int):
    if sale_id not in sales:
        raise HTTPException(status_code=404, detail="Sale not found")
    deleted = sales.pop(sale_id) #pop() returns what was deleted
    #del sales[sale_id] is possible, but it don't returns anything
    return {"message": "Sale deleted!", "sale": deleted}

@app.put("/sales/{sale_id}")
def update_sale(sale_id: int, sale: Sale):
    if sale_id not in sales:
        raise HTTPException(status_code=404, detail="Sale not found")
    sales[sale_id] = {
        "product": sale.product,
        "price": sale.price,
        "quantity": sale.quantity,
        "total": sale.price * sale.quantity
    }
    return {"message": "Sale updated!", "sale": sales[sale_id]}

print(sales)
