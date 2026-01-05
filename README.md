# 🔄 버튼식 양방향 통신

Flask-SocketIO를 사용한 실시간 양방향 통신 웹 애플리케이션입니다.

## ✨ 기능

- **실시간 양방향 통신**: WebSocket을 통한 즉각적인 메시지 송수신
- **다양한 버튼 액션**: 
  - 👋 인사하기
  - 🏓 핑 테스트
  - ⏰ 서버 시간 조회
  - 🚀 작업 시작
- **커스텀 메시지**: 직접 입력한 메시지 전송 가능
- **메시지 로그**: 송수신 메시지 기록 확인

## 🚀 시작하기

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 서버 실행

```bash
python server.py
```

### 3. 브라우저에서 접속

```
http://localhost:5000
```

## 📁 프로젝트 구조

```
/workspace
├── server.py           # Flask-SocketIO 서버
├── templates/
│   └── index.html      # 프론트엔드 UI
├── requirements.txt    # Python 의존성
└── README.md
```

## 🔧 기술 스택

- **Backend**: Python, Flask, Flask-SocketIO
- **Frontend**: HTML5, CSS3, JavaScript, Socket.IO Client
- **통신**: WebSocket (Socket.IO)

## 📡 통신 이벤트

| 이벤트 | 방향 | 설명 |
|--------|------|------|
| `client_message` | 클라이언트 → 서버 | 일반 메시지 전송 |
| `ping_server` | 클라이언트 → 서버 | 핑 테스트 |
| `request_time` | 클라이언트 → 서버 | 서버 시간 요청 |
| `server_message` | 서버 → 클라이언트 | 서버 응답 |
