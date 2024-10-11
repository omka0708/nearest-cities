from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .routers import city

app = FastAPI(title="Nearest Cities API")


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


app.include_router(
    city.router,
    prefix="/api/city",
    tags=["city"],
)
