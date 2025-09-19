## 목표
- PostgreSQL 컨테이너 실행 (Docker)
- SQLAlchemy ORM 기본 설정 (engine, Base, SessionLocal)
- TaskResult 모델 정의
- 테이블 생성 및 확인

## 작업 내역
- `docker run` 으로 PostgreSQL 컨테이너 실행
- `src/db/models.py` 파일 생성 및 SQLAlchemy 연결 코드 작성
- `TaskResult` 모델 정의 (task_results 테이블)
- Python 셸에서 `Base.metadata.create_all(bind=engine)` 실행 → DB에 테이블 생성 성공 확인

## 확인 결과
- PostgreSQL 내부에서 `\dt` 실행 시 `task_results` 테이블 확인됨 ✅

## 다음 단계
- Celery 작업이 끝날 때마다 결과를 DB에 기록하도록 수정
- FastAPI API에서 DB에 저장된 TaskResult 조회 기능 추가
