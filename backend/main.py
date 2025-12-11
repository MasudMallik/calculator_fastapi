from fastapi import FastAPI,Request,Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app=FastAPI()

app.mount("/static",StaticFiles(directory="frontend/static"),name="static")
template=Jinja2Templates(directory="frontend/templates")

global ans,operator,first,second
ans=0
first=""
second=""
operator=""
@app.get("/")
async def home(request:Request):
    return template.TemplateResponse("home.html",{"request":request,"result":ans})
@app.post("/press",response_class=HTMLResponse)
async def cal(request:Request,key:str=Form(...)):
    global ans,operator,first,second
    if key=="C":
        first=""
        operator=""
        second=""
        ans=0
        return template.TemplateResponse("home.html",{"request":request,"result":ans})
    elif key not in ["+","*","/","-","="]:
        if operator =="":
            first+=key
            return template.TemplateResponse("home.html",{"request":request,"result":first})
        else:
            second+=key
            return template.TemplateResponse("home.html",{"request":request,"result":second})
    elif key in ["+","*","/","-"]:
        operator=key
        key=""
        return template.TemplateResponse("home.html",{"request":request,"result":operator})
    elif key=="=":
        try:
            ans=eval(f"{first}{operator}{second}")
        except ZeroDivisionError as e:
            return template.TemplateResponse("home.html",{"request":request,"result":e})
        else:
            
            first=ans
            second=""
            ans=0
        return template.TemplateResponse("home.html",{"request":request,"result":first})
