from fastapi import FastAPI
from db.database import Base, engine
from routers import auth,agent_websocket,mattress_router
from fastapi.middleware.cors import CORSMiddleware
# from security import user

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)


# Include routers
app.include_router(auth.router)
app.include_router(agent_websocket.router)
app.include_router(mattress_router.router)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Can restrict this to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)