from fastapi.middleware.cors import CORSMiddleware
from routers import auth, grade, teacher, child, achievement
from fastapi.security import OAuth2PasswordBearer
from middlewares import AuthMiddleware
from fastapi import FastAPI


app = FastAPI(
    debug=True, 
    title="Backend часть",
    description="Список endpoint проекта",
    version="1.0.5"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuthMiddleware)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    scheme_name="Bearer",
    auto_error=False
)

@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_schema():
    schema = app.openapi()
    schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in schema["paths"].values():
        for method in path.values():
            if "security" not in method:
                method["security"] = [{"BearerAuth": []}]
    return schema

for module in (auth, grade, teacher, child, achievement):
    app.include_router(module.router)
