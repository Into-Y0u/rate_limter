
from fastapi import FastAPI, HTTPException, Request

from token_bucket import consume_token

app = FastAPI()


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """
    Middleware to enforce rate limiting using the token bucket algorithm.
    """
    client_ip = request.client.host  # Get the client's IP address

    if not consume_token(client_ip):
        raise HTTPException(status_code=429, detail="Too Many Requests")

    response = await call_next(request)
    return response



@app.get("/")
async def root(req : Request):
    return {"message": 'Hello Baby'}


@app.get("/test")
async def root(req : Request):
    return {"client_ip" : req.client.host}