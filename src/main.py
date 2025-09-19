from fastapi import FastAPI

# FastAPI 앱 인스턴스 생성하는거임

app = FastAPI()

# 기본 라우트

#@app.get("/")
 #def read_root():
   #return {"message": "Hello Cloud-AI-Agent-Infra Project"}

@app.get("/hello/{name}")
def say_hello(name: str):
  return {"message": f"Hello,{name}"}

@app.get("/bye/{name}")
def say_bye(name:str):
  return {"message": f"GoodBye, {name}"}

@app.get("/next")
def say_next():
  return {
    "message" : "This is Next Page"
  }
  
### 혼자 추가로 라우팅공부

# Query Parameter (쿼리 스트링)

@app.get("/items")
def read_item(item_id: int, q: str = None):
  return {"item_id": item_id, "q": q}

## 클라이언트가 보내는 JSON 데이터를 받는 방법
# 이때 Pydantic 모델을 사용한다.

from pydantic import BaseModel

class Item(BaseModel):
  name: str
  price: float
  
@app.post("/items")
def create_item(item: Item):
  return {"name" : item.name, "price": item.price}

## FastAPI에서 Celery Task호출해보기

from src.celery_app import add, get_task_result


@app.get("/")
def read_root():
  return{
    "message": "Hello 이경준의 클라우드 인프라 프로젝트"
  }
  
@app.get("/add-task/")
def run_add_task(x: int, y:int):
  task = add.delay(x,y)
  return {
    "task_id":task.id
  }
  
@app.get("/task-result/{task_id}")
def check_task_result(task_id: str):
  return get_task_result(task_id)