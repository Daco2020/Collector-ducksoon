from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.models import mongodb
from app.models.book import BookModel


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI()
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    book = BookModel(keyword="파이썬", publisher="덕순북스", price=15000, image="me.png")
    await mongodb.engine.save(book)  # save 매서드는 async(코루틴)함수이기 때문에 비동기로 작동한다.
    return templates.TemplateResponse(
        "./index.html", {"request": request, "title": "콜렉터 덕순이"}
    )


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str):
    return templates.TemplateResponse(
        "./index.html",
        {"request": request, "title": "콜렉터 덕순이"},
    )


# 서버가 시작 되었을 때 사용되는 이벤트
@app.on_event("startup")
def on_app_start():
    print("서버가 시작되었습니다.")
    mongodb.connect()


# 서버가 종료 되었을 때 사용되는 이벤트
@app.on_event("shutdown")
def on_app_shutdown():
    print("서버가 종료되었습니다.")
    mongodb.close()
