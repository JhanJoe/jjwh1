from fastapi import FastAPI, Depends, Form, HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse, HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from urllib.parse import quote

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="pengpeng")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.post("/signin")
async def signin(request: Request, username: str = Form(""), password: str = Form("")):
    if not username or not password:
        error_message = "請輸入帳號和密碼"
        encoded_message = quote(error_message)  
        return RedirectResponse(url=f"/error?message={encoded_message}", status_code=303)
    elif username == "test" and password == "test":
        request.session['SIGNED-IN'] = True  
        return RedirectResponse(url="/member", status_code=303)
    else:
        error_message = "帳號、或密碼輸入錯誤"
        encoded_message = quote(error_message)  
        return RedirectResponse(url=f"/error?message={encoded_message}", status_code=303)

@app.get("/error")
async def error_page(request: Request, message: str):
    return templates.TemplateResponse("error.html", {"request": request, "error_message": message})

@app.get("/member")
async def member(request: Request):
    if not request.session.get('SIGNED-IN', False):  
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("member.html", {"request": request})

@app.get("/signout")
async def signout(request: Request):
    request.session['SIGNED-IN'] = False 
    return RedirectResponse(url="/", status_code=303)

@app.get("/square/{num}", response_class=HTMLResponse)
async def calculate_square(request: Request, num: int):
    square_number = num * num
    return templates.TemplateResponse("square.html", {"request": request, "square_number": square_number})

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
