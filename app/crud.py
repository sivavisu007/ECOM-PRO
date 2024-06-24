from sqlalchemy.orm import Session
import models
import schemas
import depends

def get_users(db: Session):
    return db.query(models.User).all()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = depends.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.username = user_update.username
        db_user.hashed_password = depends.get_password_hash(user_update.password)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# Product CRUD operations
def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session):
    return db.query(models.Product).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_update: schemas.ProductCreate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db_product.name = product_update.name
        db_product.description = product_update.description
        db_product.price = product_update.price
        db_product.stock = product_update.stock
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product

# CartItem CRUD operations
def get_cart_items(db: Session, user_id: int):
    return db.query(models.CartItem).filter(models.CartItem.user_id == user_id).all()

def add_item_to_cart(db: Session, cart_item: schemas.CartItemCreate, user_id: int):
    db_cart_item = models.CartItem(**cart_item.dict(), user_id=user_id)
    db.add(db_cart_item)
    db.commit()
    db.refresh(db_cart_item)
    return db_cart_item

def update_cart_item(db: Session, cart_item_id: int, cart_item_update: schemas.CartItemCreate):
    db_cart_item = db.query(models.CartItem).filter(models.CartItem.id == cart_item_id).first()
    if db_cart_item:
        db_cart_item.quantity = cart_item_update.quantity
        db_cart_item.product_id = cart_item_update.product_id
        db.commit()
        db.refresh(db_cart_item)
    return db_cart_item

def delete_cart_item(db: Session, cart_item_id: int):
    db_cart_item = db.query(models.CartItem).filter(models.CartItem.id == cart_item_id).first()
    if db_cart_item:
        db.delete(db_cart_item)
        db.commit()
    return db_cart_item

# Purchase CRUD operations
def get_purchase(db: Session, purchase_id: int):
    return db.query(models.Purchase).filter(models.Purchase.id == purchase_id).first()

def get_purchases(db: Session, user_id: int):
    return db.query(models.Purchase).filter(models.Purchase.user_id == user_id).all()

def create_purchase(db: Session, purchase: schemas.PurchaseCreate, user_id: int):
    db_purchase = models.Purchase(**purchase.dict(), user_id=user_id)
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase

def update_purchase(db: Session, purchase_id: int, purchase_update: schemas.PurchaseCreate):
    db_purchase = db.query(models.Purchase).filter(models.Purchase.id == purchase_id).first()
    if db_purchase:
        db_purchase.total_price = purchase_update.total_price
        db.commit()
        db.refresh(db_purchase)
    return db_purchase

def delete_purchase(db: Session, purchase_id: int):
    db_purchase = db.query(models.Purchase).filter(models.Purchase.id == purchase_id).first()
    if db_purchase:
        db.delete(db_purchase)
        db.commit()
    return db_purchase