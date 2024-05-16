from fastapi import FastAPI, Form, Request, Body
from starlette.responses import RedirectResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
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
        cursor.execute("SELECT username FROM member WHERE username = %s", (signup_id,))
        user = cursor.fetchone()
        if user:
            error_message = quote("您欲申請的帳號已存在，無法註冊") 
            return RedirectResponse(url=f"/error?message={error_message}", status_code=303)
        else:
            cursor.execute("INSERT INTO member (name, username, password) VALUES (%s, %s, %s)",
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
        cursor.execute("SELECT id, name, username, password FROM member WHERE username = %s", (signin_id,))
        user = cursor.fetchone()
        if user and user[3] == signin_password:
            request.session['user_id'] = user[0]  
            request.session['user_name'] = user[1]  
            request.session['user_username'] = user[2]         
            # print(user) #測試
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
    request.session.pop('user_id', None)  
    request.session.pop('user_name', None)  
    request.session.pop('user_username', None)  
    return RedirectResponse(url="/", status_code=303)

@app.get("/error")
async def error_page(request: Request, message: str):
    return templates.TemplateResponse("error.html", {"request": request, "error_message": message})

@app.post("/createMessage")
async def create_message(request: Request, message: str = Form('')):
    member_id = request.session.get('user_id')
    if not member_id:
        return RedirectResponse(url="/", status_code=303) 

    cursor = app.state.connection.cursor()
    try:
        cursor.execute("INSERT INTO message (member_id, content) VALUES (%s, %s)",
                       (member_id, message))
        app.state.connection.commit()
    except mysql.connector.Error as err:
        return RedirectResponse(url="/error?message=" + quote("留言儲存失敗"), status_code=303)
    finally:
        cursor.close()

    return RedirectResponse(url="/member", status_code=303)

@app.get("/member")
async def member_page(request: Request):
    if 'user_username' not in request.session:
        return RedirectResponse(url="/", status_code=303)

    member_id = request.session.get('user_id')
    user_name = request.session.get('user_name')
    cursor = app.state.connection.cursor()
    try:
        cursor.execute("""
            SELECT member.name, message.member_id, message.content, message.id
            FROM message 
            JOIN member ON member.id = message.member_id
            ORDER BY message.time DESC
        """)
        messages = cursor.fetchall()
            
    finally:
        cursor.close()

    return templates.TemplateResponse("member.html", {"request": request, "name": user_name, "messages": messages, "current_user_id": member_id})

@app.get("/deleteMessage")
async def delete_message(request: Request, message_id: int):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse(url="/", status_code=303)

    cursor = app.state.connection.cursor()
    try:
        cursor.execute("SELECT member_id FROM message WHERE id = %s", (message_id,))
        message_user = cursor.fetchone()
        if message_user and message_user[0] == int(user_id):  
            cursor.execute("DELETE FROM message WHERE id = %s", (message_id,))
            app.state.connection.commit()
        else:
            return RedirectResponse(url="/error?message=" + quote("無權刪除該留言"), status_code=303)
    except mysql.connector.Error as err:
        return RedirectResponse(url="/error?message=" + quote("刪除失敗，內部服務器錯誤"), status_code=303)
    finally:
        cursor.close()

    return RedirectResponse(url="/member", status_code=303)

@app.get("/api/member")
async def member_query(request: Request, username: str):
    if 'user_id' not in request.session:
        return {"data": None}

    # 如果是來自瀏覽器的直接訪問或刷新，重定向到 /member 頁面
    if "text/html" in request.headers.get("accept"):
        return RedirectResponse(url="/member")

    cursor = app.state.connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, name, username FROM member WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user:
            return {"data": {"id": user['id'], "name": user['name'], "username": user['username']}} 
        else:
            return {"data": None}
    except mysql.connector.Error:
        return {"data": None}  
    finally:
        cursor.close()


class UpdateNameRequest(BaseModel):
    name: str

@app.patch("/api/member")
async def update_member_name(request: Request, update_request: UpdateNameRequest = Body(...)):
    user_id = request.session.get('user_id')
    if not user_id:
        return JSONResponse(status_code=400, content={"error": True})
    name = update_request.name
    if not name:
        return JSONResponse(status_code=400, content={"error": True})

    cursor = app.state.connection.cursor()
    try:
        cursor.execute("UPDATE member SET name = %s WHERE id = %s", (name, user_id))
        app.state.connection.commit()

        if cursor.rowcount == 0:
            return JSONResponse(status_code=404, content={"error": True})
        else:
            return JSONResponse(status_code=200, content={"ok": True})
    except mysql.connector.Error as err:
        return JSONResponse(status_code=500, content={"error": True})
    finally:
        cursor.close()

