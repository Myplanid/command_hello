#!/usr/bin/env python3
"""
Dooray Webhook 테스트 스크립트
"""

import json
import urllib.request
import urllib.error
import sys

# Dooray 웹훅 URL (여기에 실제 URL을 넣어주세요)
WEBHOOK_URL = "YOUR_DOORAY_WEBHOOK_URL_HERE"

def send_dooray_message(text, bot_name="Test Bot", bot_icon=None):
    """Dooray 웹훅으로 메시지 전송"""
    
    payload = {
        "botName": bot_name,
        "text": text
    }
    
    if bot_icon:
        payload["botIconImage"] = bot_icon
    
    data = json.dumps(payload).encode('utf-8')
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    request = urllib.request.Request(
        WEBHOOK_URL,
        data=data,
        headers=headers,
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(request) as response:
            result = response.read().decode('utf-8')
            print(f"✅ 성공! 응답: {result}")
            return True
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP 에러: {e.code} - {e.reason}")
        return False
    except urllib.error.URLError as e:
        print(f"❌ URL 에러: {e.reason}")
        return False

if __name__ == "__main__":
    if WEBHOOK_URL == "YOUR_DOORAY_WEBHOOK_URL_HERE":
        print("⚠️  웹훅 URL을 설정해주세요!")
        print("스크립트 상단의 WEBHOOK_URL 변수를 수정하거나,")
        print("아래와 같이 환경변수로 설정해주세요:")
        print("  export DOORAY_WEBHOOK_URL='https://hook.dooray.com/...'")
        sys.exit(1)
    
    # 테스트 메시지 전송
    message = "🎉 Dooray 웹훅 테스트 메시지입니다!\n\n- 1차 테스트 완료"
    
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    
    print(f"📤 메시지 전송 중: {message}")
    send_dooray_message(message, bot_name="Cursor Agent")
