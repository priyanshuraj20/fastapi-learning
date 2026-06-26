from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Hello,fatsApi learning"
    }

@app.get("/users/{users_id}"):
def get_user(user_id: int):
    return {"user_id": user_id}