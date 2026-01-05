"""
웹훅 테스트 서버 - 1차 테스트용
Flask를 사용한 간단한 웹훅 수신 서버입니다.
"""

from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# 수신된 웹훅 기록 저장
webhook_logs = []


@app.route('/health', methods=['GET'])
def health_check():
    """서버 상태 확인 엔드포인트"""
    return jsonify({
        'status': 'healthy',
        'message': '웹훅 서버가 정상 작동 중입니다.',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/webhook', methods=['POST'])
def receive_webhook():
    """웹훅 수신 엔드포인트"""
    try:
        # 요청 데이터 파싱
        if request.is_json:
            payload = request.get_json()
        else:
            payload = request.data.decode('utf-8')
        
        # 웹훅 로그 기록
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'headers': dict(request.headers),
            'payload': payload,
            'method': request.method,
            'path': request.path
        }
        webhook_logs.append(log_entry)
        
        print(f"[{log_entry['timestamp']}] 웹훅 수신됨!")
        print(f"페이로드: {json.dumps(payload, indent=2, ensure_ascii=False)}")
        
        return jsonify({
            'success': True,
            'message': '웹훅이 성공적으로 수신되었습니다.',
            'received_at': log_entry['timestamp']
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/webhook/logs', methods=['GET'])
def get_logs():
    """수신된 웹훅 로그 조회"""
    return jsonify({
        'total_count': len(webhook_logs),
        'logs': webhook_logs[-10:]  # 최근 10개만 반환
    })


@app.route('/webhook/clear', methods=['POST'])
def clear_logs():
    """웹훅 로그 초기화"""
    global webhook_logs
    webhook_logs = []
    return jsonify({
        'success': True,
        'message': '로그가 초기화되었습니다.'
    })


if __name__ == '__main__':
    print("=" * 50)
    print("🚀 웹훅 테스트 서버 시작")
    print("=" * 50)
    print("엔드포인트:")
    print("  - GET  /health        : 서버 상태 확인")
    print("  - POST /webhook       : 웹훅 수신")
    print("  - GET  /webhook/logs  : 웹훅 로그 조회")
    print("  - POST /webhook/clear : 로그 초기화")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
