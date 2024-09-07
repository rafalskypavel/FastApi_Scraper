import logging
from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from routers import suppliers, auth, dashboard, data_view, scraping, test, settings

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("main")

application = FastAPI()

application.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

application.include_router(suppliers.router, prefix="/suppliers", tags=["suppliers"])
application.include_router(auth.router, prefix="/auth", tags=["auth"])
application.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
application.include_router(data_view.router, prefix="/data-view", tags=["data_view"])
application.include_router(scraping.router, prefix="/scraping", tags=["scraping"])
application.include_router(test.router, prefix="/test", tags=["test"])
application.include_router(settings.router, prefix="/settings", tags=["settings"])

@application.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:application", host="0.0.0.0", port=8000, reload=True)
