from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm  
from sqlalchemy.orm import Session
import crud
import schemas
import depends
import database

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Ecommerce Application", description="E-commerce API created with FastAPI and JWT Authentication")

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(depends.get_db)):
    user = depends.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token = depends.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# User Endpoints
@app.get("/users", response_model=list[schemas.User], tags=["USER"])
def read_users(db: Session = Depends(depends.get_db)):
    return crud.get_users(db)

@app.post("/users", response_model=schemas.UserWithToken, tags=["USER"])
async def create_user(user: schemas.UserCreate, db: Session = Depends(depends.get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    created_user = crud.create_user(db=db, user=user)
    access_token = depends.create_access_token(data={"sub": created_user.username})
    return {"user": created_user, "access_token": access_token, "token_type": "bearer"}

@app.put("/users/{user_id}", response_model=schemas.User, tags=["USER"])
async def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(depends.get_db), current_user: schemas.User =Depends(depends.get_current_user)):
    db_user = crud.update_user(db, user_id, user)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user

@app.delete("/users/{user_id}", response_model=schemas.User, tags=["USER"])
async def delete_user(user_id: int, db: Session = Depends(depends.get_db), current_user: schemas.User =Depends(depends.get_current_user)):
    db_user = crud.delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user

# Product Endpoints
@app.get("/products", response_model=list[schemas.Product], tags=["PRODUCT"])
async def read_products(db: Session = Depends(depends.get_db), current_user: schemas.User =Depends(depends.get_current_user)):
    return crud.get_products(db)

@app.post("/products", response_model=schemas.Product, tags=["PRODUCT"])
async def create_product(product: schemas.ProductCreate, db: Session = Depends(depends.get_db),current_user: schemas.User =Depends(depends.get_current_user)):
    return crud.create_product(db=db, product=product)

@app.put("/products/{product_id}", response_model=schemas.Product, tags=["PRODUCT"])
async def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(depends.get_db), current_user: schemas.User =Depends(depends.get_current_user)):
    db_product = crud.update_product(db, product_id, product)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return db_product

@app.delete("/products/{product_id}", response_model=schemas.Product, tags=["PRODUCT"])
async def delete_product(product_id: int, db: Session = Depends(depends.get_db), current_user: schemas.User =Depends(depends.get_current_user)):
    db_product = crud.delete_product(db, product_id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return db_product

# CartItem Endpoints
@app.get("/carts/{user_id}", response_model=list[schemas.CartItem], tags=["CART"])
async def read_cart(user_id: int, db: Session = Depends(depends.get_db),current_user: schemas.User =Depends(depends.get_current_user)):
    return crud.get_cart_items(db, user_id=user_id)

@app.post("/carts/{user_id}", response_model=schemas.CartItem, tags=["CART"])
async def add_item_to_cart(cart_item: schemas.CartItemCreate, user_id: int, db: Session = Depends(depends.get_db), current_user: schemas.User =Depends(depends.get_current_user)):
    return crud.add_item_to_cart(db=db, cart_item=cart_item, user_id=user_id)

@app.put("/carts/{cart_item_id}", response_model=schemas.CartItem, tags=["CART"])
async def update_cart_item(cart_item_id: int, cart_item: schemas.CartItemCreate, db: Session = Depends(depends.get_db),current_user: schemas.User =Depends(depends.get_current_user)):
    db_cart_item = crud.update_cart_item(db, cart_item_id, cart_item)
    if db_cart_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    return db_cart_item

@app.delete("/carts/{cart_item_id}", response_model=schemas.CartItem, tags=["CART"])
async def delete_cart_item(cart_item_id: int, db: Session = Depends(depends.get_db),current_user: schemas.User =Depends(depends.get_current_user)):
    db_cart_item = crud.delete_cart_item(db, cart_item_id)
    if db_cart_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    return db_cart_item

# Purchase Endpoints
@app.get("/purchases/{user_id}", response_model=list[schemas.Purchase], tags=["PURCHASE"])
async def read_purchases(user_id: int, db: Session = Depends(depends.get_db), current_user: schemas.User =Depends(depends.get_current_user)):
    return crud.get_purchases(db, user_id=user_id)

@app.post("/purchases/{user_id}", response_model=schemas.Purchase, tags=["PURCHASE"])
async def create_purchase(purchase: schemas.PurchaseCreate, user_id: int, db: Session = Depends(depends.get_db), current_user: schemas.User =Depends(depends.get_current_user)):
    return crud.create_purchase(db=db, purchase=purchase, user_id=user_id)

@app.put("/purchases/{purchase_id}", response_model=schemas.Purchase, tags=["PURCHASE"])
async def update_purchase(purchase_id: int, purchase: schemas.PurchaseCreate, db: Session = Depends(depends.get_db), current_user: schemas.User =Depends(depends.get_current_user)):
    db_purchase = crud.update_purchase(db, purchase_id, purchase)
    if db_purchase is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purchase not found"
        )
    return db_purchase

@app.delete("/purchases/{purchase_id}", response_model=schemas.Purchase, tags=["PURCHASE"])
async def delete_purchase(purchase_id: int, db: Session = Depends(depends.get_db),current_user: schemas.User =Depends(depends.get_current_user)):
    db_purchase = crud.delete_purchase(db, purchase_id)
    if db_purchase is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purchase not found"
        )
    return db_purchase


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
