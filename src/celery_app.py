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