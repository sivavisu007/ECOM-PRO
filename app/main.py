from fastapi import FastAPI
import service.database as database
from router.routers import router

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Ecommerce Application", 
    description="E-commerce API created with FastAPI and JWT Authentication"
    )

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)