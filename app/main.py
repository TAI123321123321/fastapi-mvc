from fastapi import FastAPI

from app.core import lifespan
# from app.controllers.pages import page_controller
from app.controllers.api import auth_controller
from app.controllers.api import user_controller

from app.core.middlewares import cors_middleware
from app.exceptions import handler
import logging



# apps
app = FastAPI(lifespan=lifespan.lifespan) # jinja2 templates
api = FastAPI(lifespan=lifespan.lifespan) # api for json

# custom exception handlers
handler.add_html(app)
handler.add_json(api)

# add middlewares
cors_middleware.add(api)

# include page routers
# app.include_router(page_controller.router)

# include api routers
api.include_router(auth_controller.router)
api.include_router(user_controller.router)

# mount api app
app.mount("/api", api)

