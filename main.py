from fastapi import Depends, FastAPI, HTTPException, Request # type: ignore

from rate_limiter_manager import GlobalRateLimiter, IpRateLimiter
from fastapi.responses import JSONResponse # type: ignore


app = FastAPI()

# Initialize rate limiter
# rate_limiter = RateLimiter()
global_rate_lim = GlobalRateLimiter().get_main_bucket()
ip_rate_lim = IpRateLimiter()

# Middleware for global rate limiting
@app.middleware("http")
async def global_rate_limit_middleware(request: Request, call_next):
    print("Middleware executed")  # Debug log
    try:
        client_ip = request.client.host
        if not global_rate_lim.consume():
            return JSONResponse(
                status_code=429,
                content={"detail": "Global rate limit exceeded"},
            )

        response = await call_next(request)
        return response

    except Exception as e:
        print("Error in middleware:", str(e))  # Debug log
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )


@app.get("/")
async def global_endpoint():
    print("Landing in pplace")
    return {"message": "This is a globally rate-limited endpoint."}



@app.post("/test")
async def root(req : Request):
    print("Landing in pplace")
    return {"client_ip" : req.client.host}