from odmantic import AIOEngine, Model


class BookModel(Model):
    keyword: str
    publisher: str
    price: int
    image: str

    class Config:
        collection = "books"


"""        
db fastapi-pj -> collection books -> document {
    keyword : 
    publisher :
    price :
    image :
}
모델 외의 데이터는 받지 않는다.
"""
