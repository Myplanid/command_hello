# command_hello

## 웹훅 1차 테스트

간단한 웹훅 수신 서버와 테스트 스크립트입니다.

### 설치 방법

```bash
pip install -r requirements.txt
```

### 사용 방법

#### 1. 웹훅 서버 실행

```bash
python webhook_server.py
```

서버가 `http://localhost:5000`에서 실행됩니다.

#### 2. 테스트 실행

새 터미널에서:

```bash
python test_webhook.py
```

### 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/health` | 서버 상태 확인 |
| POST | `/webhook` | 웹훅 수신 |
| GET | `/webhook/logs` | 수신된 웹훅 로그 조회 |
| POST | `/webhook/clear` | 로그 초기화 |

### 수동 테스트 예시

```bash
# 서버 상태 확인
curl http://localhost:5000/health

# 웹훅 전송
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{"event": "test", "message": "Hello!"}'

# 로그 조회
curl http://localhost:5000/webhook/logs
```
