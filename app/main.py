from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.models import mongodb
from app.models.book import BookModel
from app.book_scraper import NaverBookScraper


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # book = BookModel(keyword="파이썬", publisher="덕순북스", price=15000, image="me.png")
    # await mongodb.engine.save(book)  # save 매서드는 async(코루틴)함수이기 때문에 비동기로 작동한다.
    return templates.TemplateResponse(
        "./index.html", {"request": request, "title": "콜렉터 덕순이"}
    )


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str):
    keyword = q

    if not keyword:
        context = {"request": request, "title": "콜렉터 덕순이"}
        return templates.TemplateResponse("./index.html", context)

    if await mongodb.engine.find_one(
        BookModel, BookModel.keyword == keyword
    ):  # (첫번째 모델, 두번째 조건문)
        books = await mongodb.engine.find(BookModel, BookModel.keyword == keyword)
        return templates.TemplateResponse(
            "./index.html",
            {"request": request, "title": "콜렉터 덕순이", "books": books},
        )
    book_scraper = NaverBookScraper()
    books = await book_scraper.search(keyword, 10)
    book_models = []

    for book in books:
        book_model = BookModel(
            keyword=keyword,
            publisher=book["publisher"],
            price=book["price"],
            image=book["image"],
        )
        book_models.append(book_model)
    await mongodb.engine.save_all(book_models)

    return templates.TemplateResponse(
        "./index.html",
        {"request": request, "title": "콜렉터 덕순이", "books": books},
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


"""
주요로직
1. 쿼리에서 키워드를 가져오기
2. 수집기로 데이터를 가져오기
3. 데이터를 디비에 저장하기 

예외처리
1. 검색어가 없다면 사용자에게 요구하기
2. 
"""
