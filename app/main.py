from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
#from fastapi.staticfiles import StaticFiles
#from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware

from .envConfig import Config
from .database import engine, get_db, Base
from .api_wrappers import token_required
from .routers import auth, exam, payment, user
from .feature.user.device.device_api import Device, DeviceCreate, DeviceResponse
from .feature.auth.auth_bearer import jwt_bearer

app = FastAPI()

# Sets the templates directory to the `build` folder from `npm run build`
# this is where you'll find the index.html file.
# templates = Jinja2Templates(directory="../frontend/dist")

# Mounts the `static` folder within the `build` folder to the `/static` route.
# app.mount("/assets", StaticFiles(directory="../frontend/dist/assets"), name="assets")

origins = [
   '*'
     # "http://localhost:5173",
    # "localhost:5173",
    # "http://localhost:8000",
    # "localhost:5173",
    # "http://0.0.0.0:8000",
    # "0.0.0.0:5173",
    # "http://192.168.178.43:8000",
    # "192.168.178.43:8000",
    # "http://testserver",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow these origins
    allow_credentials=True,  # Allow cookies to be sent in requests
    allow_methods=["*"],     # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],     # Allow all headers
)


print ("environment", Config.ENVIRONMENT, Config.YOUR_DOMAIN, Config.STRIPE_KEY, Config.DATABASE_URL)
    
Base.metadata.create_all(bind=engine)


# Include routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(exam.router)
app.include_router(payment.router)


# @app.post("/api/devices/", response_model=DeviceResponse)
# @token_required
# async def create_device(
#     obj_in: DeviceCreate,
#     db: Session = Depends(get_db),
#     dependencies=Depends(jwt_bearer),
# ):
#     Device.create_device(obj_in, db)


# @app.get("/api/users/{user_id}/devices/", response_model=list[DeviceResponse])
# @token_required
# async def get_device(
#     user_id: int, db: Session = Depends(get_db), dependencies=Depends(jwt_bearer)
# ):
#     Device.get_device(user_id, db)


# @app.delete("/api/devices/{device_id}", response_model=DeviceResponse)
# @token_required
# async def delete_device(
#     device_id: int, db: Session = Depends(get_db), dependencies=Depends(jwt_bearer)
# ):
#     Device.delete_device(device_id, db)


@app.get("/api/check-env")
def read_root():
    print ("environment", Config.ENVIRONMENT, Config.YOUR_DOMAIN, Config.STRIPE_KEY)
    return {
        "environment": Config.ENVIRONMENT,
        "stripe_key": Config.STRIPE_KEY,
        "your_domain": Config.YOUR_DOMAIN,
    }

# Defines a route handler for `/*` essentially.
# NOTE: this needs to be the last route defined b/c it's a catch all route
@app.get("/{rest_of_path:path}")
async def react_app(req: Request, rest_of_path: str):
    print("get tmepa")
    return {"request": req} #templates.TemplateResponse("index.html", {"request": req})
