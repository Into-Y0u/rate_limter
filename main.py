from fastapi import Depends, FastAPI, HTTPException, Request

from rate_limiter_manager import RateLimiter


app = FastAPI()


# Initialize rate limiter
rate_limiter = RateLimiter()


# Middleware for global rate limiting
@app.middleware("http")
async def global_rate_limit_middleware(request: Request, call_next):
    try :
        
        global_bucket_key = "global"
        if not rate_limiter.check_limit("global", global_bucket_key, max_tokens=5, refill_rate=.1):
            raise HTTPException(status_code=429, detail="Global rate limit exceeded")
        
        user_id = request.headers.get("X-User-ID", "anonymous")
        if not rate_limiter.check_limit("user", user_id, max_tokens=1, refill_rate=0.0005):
            raise HTTPException(status_code=429, detail=f"User {user_id} rate limit exceeded")
        
        client_ip = request.client.host
        if not rate_limiter.check_limit("ip", client_ip, max_tokens=1, refill_rate=0.00002):
            raise HTTPException(status_code=429, detail=f"IP {client_ip} rate limit exceeded")
    except Exception as ex :
        print(" Exception caught {} ".format(ex) )
    
    response = await call_next(request)
    return response


# Dependency for user-specific rate limiting
def user_rate_limit(request: Request):
    user_id = request.headers.get("X-User-ID", "anonymous")
    if not rate_limiter.check_limit("user", user_id, max_tokens=5, refill_rate=0.0005):
        raise HTTPException(status_code=429, detail=f"User {user_id} rate limit exceeded")


# Dependency for IP-specific rate limiting
def ip_rate_limit(request: Request):
    client_ip = request.client.host
    if not rate_limiter.check_limit("ip", client_ip, max_tokens=3, refill_rate=0.0002):
        raise HTTPException(status_code=429, detail=f"IP {client_ip} rate limit exceeded")


# Routes
@app.get("/user", dependencies=[Depends(user_rate_limit)])
async def user_specific_endpoint(request: Request):
    user_id = request.headers.get("X-User-ID", "anonymous")
    return {"message": f"Hello, user {user_id}! This is a user-specific endpoint."}


@app.get("/ip", dependencies=[Depends(ip_rate_limit)])
async def ip_specific_endpoint(request: Request):
    client_ip = request.client.host
    return {"message": f"Hello, client {client_ip}! This is an IP-specific endpoint."}


@app.get("/")
async def global_endpoint():
    return {"message": "This is a globally rate-limited endpoint."}

@app.post("/")
async def global_endpoint():
    return {"message": "This is a globally rate-limited endpoint."}




@app.get("/test")
async def root(req : Request):
    return {"client_ip" : req.client.host}