"""
버튼식 양방향 통신 서버
Flask-SocketIO를 사용한 실시간 양방향 통신
"""
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# 메시지 카운터
message_count = 0


@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')


@socketio.on('connect')
def handle_connect():
    """클라이언트 연결 시"""
    print('클라이언트가 연결되었습니다!')
    emit('server_message', {
        'type': 'info',
        'message': '서버에 연결되었습니다! 버튼을 눌러 메시지를 보내세요.',
        'timestamp': datetime.now().strftime('%H:%M:%S')
    })


@socketio.on('disconnect')
def handle_disconnect():
    """클라이언트 연결 해제 시"""
    print('클라이언트 연결이 해제되었습니다.')


@socketio.on('client_message')
def handle_client_message(data):
    """클라이언트에서 메시지를 받았을 때"""
    global message_count
    message_count += 1
    
    print(f"클라이언트로부터 받은 메시지: {data}")
    
    # 서버에서 응답 생성
    response = {
        'type': 'response',
        'original_message': data.get('message', ''),
        'server_reply': f"'{data.get('message', '')}'에 대한 서버 응답입니다!",
        'message_number': message_count,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }
    
    # 클라이언트에게 응답 전송
    emit('server_message', response)


@socketio.on('ping_server')
def handle_ping():
    """핑 요청 처리"""
    emit('server_message', {
        'type': 'pong',
        'message': '퐁! 서버가 응답합니다.',
        'timestamp': datetime.now().strftime('%H:%M:%S')
    })


@socketio.on('request_time')
def handle_time_request():
    """현재 시간 요청 처리"""
    emit('server_message', {
        'type': 'time',
        'message': f"현재 서버 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        'timestamp': datetime.now().strftime('%H:%M:%S')
    })


if __name__ == '__main__':
    print('🚀 양방향 통신 서버를 시작합니다...')
    print('📡 http://localhost:5000 에서 접속 가능합니다.')
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
