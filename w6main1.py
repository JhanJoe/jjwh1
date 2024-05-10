from fastapi import FastAPI, Form, Request
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from urllib.parse import quote
import mysql.connector

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="password")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup():
    app.state.connection = mysql.connector.connect(host='localhost', port='3306', user='root', password='mysqlpw', database='website')
    print("資料庫連接成功")

@app.on_event("shutdown")
async def shutdown():
    app.state.connection.close()
    print("資料庫連接已關閉")

@app.post("/signup")
async def signup(request: Request, name: str = Form(default=""), signup_id: str = Form(default=""), signup_password: str = Form(default="")):
    if not (name and signup_id and signup_password):  
        error_message = quote("姓名、帳號、密碼不得為空")
        return RedirectResponse(url=f"/error?message={error_message}", status_code=303)
    
    cursor = app.state.connection.cursor()
    try:
        cursor.execute("SELECT username FROM week6 WHERE username = %s", (signup_id,))
        user = cursor.fetchone()
        if user:
            error_message = quote("您欲申請的帳號已存在，無法註冊") 
            return RedirectResponse(url=f"/error?message={error_message}", status_code=303)
        else:
            cursor.execute("INSERT INTO week6 (name, username, password) VALUES (%s, %s, %s)",
                           (name, signup_id, signup_password))
            app.state.connection.commit()
    except mysql.connector.Error as err:
        print("MySQL Error: ", err)
        error_message = quote("無法註冊，內部服務器錯誤")
        return RedirectResponse(url=f"/error?message={error_message}", status_code=303)
    finally:
        cursor.close()
    return RedirectResponse(url="/", status_code=303)

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/signin")
async def signin(request: Request, signin_id: str = Form(default=""), signin_password: str = Form(default="")):
    cursor = app.state.connection.cursor()
    try:
        cursor.execute("SELECT name, username, password FROM week6 WHERE username = %s", (signin_id,))
        user = cursor.fetchone()
        if user and user[2] == signin_password:
            request.session['user'] = user[1] 
            return RedirectResponse(url="/member", status_code=303)
        else:
            error_message = quote("帳號或密碼輸入錯誤")
            return RedirectResponse(url=f"/error?message={error_message}", status_code=303)
    except mysql.connector.Error as err:
        error_message = quote("登入失敗，內部服務器錯誤")
        return RedirectResponse(url=f"/error?message={error_message}", status_code=303)
    finally:
        cursor.close()

@app.get("/signout")
async def signout(request: Request):
    request.session.pop('user', None)  
    return RedirectResponse(url="/", status_code=303)

@app.get("/error")
async def error_page(request: Request, message: str):
    return templates.TemplateResponse("error.html", {"request": request, "error_message": message})

@app.post("/createMessage")
async def create_message(request: Request, message: str = Form('')):
    username = request.session.get('user')
    if not username:
        return RedirectResponse(url="/", status_code=303) 

    cursor = app.state.connection.cursor()
    try:
        cursor.execute("INSERT INTO week6message (username, message) VALUES (%s, %s)",
                       (username, message))
        app.state.connection.commit()
    except mysql.connector.Error as err:
        return RedirectResponse(url="/error?message=" + quote("留言儲存失敗"), status_code=303)
    finally:
        cursor.close()

    return RedirectResponse(url="/member", status_code=303)

@app.get("/member")
async def member_page(request: Request):
    if 'user' not in request.session:
        return RedirectResponse(url="/", status_code=303)

    username = request.session['user']
    cursor = app.state.connection.cursor()
    try:
        cursor.execute("SELECT name FROM week6 WHERE username = %s", (username,))
        user_name = cursor.fetchone()
   
        if user_name:
            cursor.execute("""
                SELECT w6.name, wm.username, wm.message, wm.message_id
                FROM week6message wm
                JOIN week6 w6 ON wm.username = w6.username
                ORDER BY wm.message_time DESC
            """)
            messages = cursor.fetchall()
        else:
            messages = []
    finally:
        cursor.close()

    return templates.TemplateResponse("member.html", {"request": request, "name": user_name[0], "messages": messages})

@app.get("/deleteMessage")
async def delete_message(request: Request, message_id: int):
    username = request.session.get('user')
    if not username:
        return RedirectResponse(url="/", status_code=303)

    cursor = app.state.connection.cursor()
    try:
        cursor.execute("SELECT username FROM week6message WHERE message_id = %s", (message_id,))
        message_user = cursor.fetchone()
        if message_user and message_user[0] == username:
            cursor.execute("DELETE FROM week6message WHERE message_id = %s", (message_id,))
            app.state.connection.commit()
        else:
            return RedirectResponse(url="/error?message=" + quote("無權刪除該留言"), status_code=303)
    except mysql.connector.Error as err:
        return RedirectResponse(url="/error?message=" + quote("刪除失敗，內部服務器錯誤"), status_code=303)
    finally:
        cursor.close()

    return RedirectResponse(url="/member", status_code=303)