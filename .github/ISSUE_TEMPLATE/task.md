목표

1. PostgreSQL 컨테이너 실행 -> Docker사용
2. SQLAlchemy 기본설정해봄 
3. TaskResult 모델 만들고 결과조회해봄
4. 테이블생성된거 확인했음

공부한것

쿼리 파라미터 공부 "POST"

Path parameter: URL 일부로 데이터 받음

Query parameter: ?key=value 형식으로 데이터 받음

POST + JSON Body: 구조화된 데이터 받음 (Pydantic으로 검증 가능)


- Celery는 비동기 작업 처리 (백그라운드 작업 큐)를 가능하게
해주는 툴

- Redis는 그 메세지 브로커역할을 함

오늘작업결과

docker exec -it pg psql -U kjune922 -d cloud_ai 로 
 Schema |     Name     | Type  |  Owner
--------+--------------+-------+----------
 public | task_results | table | kjune922
 이렇게 확인했음
 