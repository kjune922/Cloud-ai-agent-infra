# Cloud AI Agent Infra Project

from Fastapi import FastAPI, Request
-> FastAPI: 웹 서버 프레임워크
-> Request: HTTP 요청 객체
from pydantic import BaseModel
-> BaseModel : 요청 데이터 검증

from src.celery_app import add, get_task_result, save_webhook_event
-> Celery 관련 함수 import

from src.db.models import SessionLocal, TaskResult, WebhookEvent

DB관련 import -> SessionLocal (DB연결세션), TaskResult / WebhookEvent (DB 테이블 매핑모델)

1. app = FastAPI()
-> FastAPI 앱 인스턴스 생성 -> uvicorn이 실행할 대상이된다

2. @app.get("/")
def read_root():
  return {"message" : "Hello~~~이경준~~~"}
  -> /경로에 GET 요청이오면 간단한 문자열 리턴하는 코드

3. @app.get("/bye/{name}")
def say_bye(name:str)
  return {"message": f"굿바이, {name}"}
  -> 주소창에 name을 인식

4. @app.get("/items")
def read_item(item_id: int, q: str= None):
  return {"item_id" : item_id, "q": q}
  -> /item?item_id=10&q=hello -> {"item_id":10, "q": "hello"}
  쿼리파라미터 예시임

5. 본격적인 리퀘스트 예시

class Item(BaseModel):
  name: str
  price: float

@app.post("/items")
def create_item(item:Item):
  return {"name": item.name, "price": item.price}

-> 이렇게하면 postman에서 /items 요청시 JSON Body에 {"name": "Book", "price": 12.5} 라고 넣으면
-> 자동으로 Item모델로 변환해서 name과 price를 리턴해줌

## Celery Task 등록과 결과조회

@app.get("/add_task/")
def run_add_task(x:int,y:int)
  task = add.delay(x,y) # Celery워커에 작업등록
  return {"task_id":task.id}

/add-task/?x=3&y=4 -> Redis큐에 작업넣어놓고, task_id 변환

@app.get("/task-result/{task_id}")
def check_task_result(task_id: str):
  return get_task_result(task_id)
  -> AsyncResult로 상태랑 결과 조회함

# DB에서 Task 결과조회

@app.get("/db-results/")
def get_db_results():
  db = SessionLocal() # DB연결세션 생성
  try:
    results = db.query(TaskResult).all() --> select * from task_results
        for r in results:    # results에 있는 TaskResult 객체들을 하나씩 꺼냄
      row = {          # 각 객체에서 필요한 값만 뽑아서 딕셔너리 생성
        "task_id": r.task_id,
        "status": r.status,
        "result": r.result
      }
      response_data.append(row)   # 리스트에 추가

    return response_data
  finally:  # 작업 끝나면 DB닫음
    db.close()

### Webhook 처리
@app.post("/webhook")
async def receive_webhook(request: Request):
    data = await request.json()  # POST Body JSON 읽기
    event_type = data.get("type", "unknown")  # type 키 없으면 unknown
    task = save_webhook_event.delay(event_type, data)  # Celery에 Task 등록
    return {"task_id": task.id, "status": "받았음"}

### Webhook 이벤트 저장 테이블

class WebhookEvent(Base):
    __tablename__ = "webhook_events"

    id = Column(Integer, primary_key=True, index=True)   # 기본키
    event_type = Column(String, nullable=False)          # 이벤트 타입 (ex: user_signup)
    payload = Column(JSON, nullable=False)               # 원본 JSON 데이터