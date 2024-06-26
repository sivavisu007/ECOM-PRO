from fastapi import FastAPI
import service.database as database
from router.routers import router
from config.config import logger

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Ecommerce Application", 
    description="E-commerce API created with FastAPI and JWT Authentication"
    )

app.include_router(router)


@app.on_event("startup")
async def startup():
    logger.info("application startup")

@app.on_event("shutdown")
async def startup():
    logger.info("application shutdown")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)