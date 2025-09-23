from celery import Celery

# Redis를 브로커로 사용하는 Celery 인스턴스 생성
celery_app = Celery(
  "Worker",
  broker = "redis://localhost:6379/0",
  backend= "redis://localhost:6379/0"
)



@celery_app.task
def add(x,y):
  return x + y

## Celery 작업 결과 확인 함수 만들어보쟈잉

from celery.result import AsyncResult


def get_task_result(task_id: str):
  result = AsyncResult(task_id, app=celery_app)
  return {
    "task_id": task_id,
    "status": result.status,
    "result": result.result
  }


## 이제는 celery_app.task의 작업이 끝나면 DB에 저장하도록 바꿔보자
from src.db.models import SessionLocal, TaskResult

@celery_app.task
def add(x,y):
  result_value = x + y
  
  # DB연결
  db = SessionLocal()
  try:
    task_result = TaskResult(
      task_id = add.request.id, # Celery가 생성한 고유 TaskID
      status = "성공입니다",
      result = str(result_value) 
    )
    db.add(task_result)
    db.commit()
  finally:
    db.close()
    
  return result_value

from src.db.models import SessionLocal, WebhookEvent

@celery_app.task
def save_webhook_event(event_type: str, payload: dict):
  db = SessionLocal()
  try:
    event = WebhookEvent(
      event_type = event_type,
      payload = payload
    )
    db.add(event)
    db.commit()
  finally:
    db.close()
  return {"status":"saved","event_type":event_type}