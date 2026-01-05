"""
웹훅 테스트 스크립트 - 1차 테스트용
웹훅 서버에 테스트 요청을 보내는 스크립트입니다.
"""

import requests
import json
import sys

BASE_URL = "http://localhost:5000"


def test_health_check():
    """서버 상태 확인 테스트"""
    print("\n📋 테스트 1: 서버 상태 확인")
    print("-" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"상태 코드: {response.status_code}")
        print(f"응답: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        assert response.status_code == 200
        assert response.json()['status'] == 'healthy'
        print("✅ 테스트 통과!")
        return True
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
        return False


def test_webhook_json():
    """JSON 웹훅 수신 테스트"""
    print("\n📋 테스트 2: JSON 웹훅 수신")
    print("-" * 40)
    
    payload = {
        "event": "test_event",
        "data": {
            "message": "안녕하세요! 웹훅 테스트입니다.",
            "user_id": 12345,
            "action": "create"
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/webhook",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"상태 코드: {response.status_code}")
        print(f"응답: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        assert response.status_code == 200
        assert response.json()['success'] == True
        print("✅ 테스트 통과!")
        return True
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
        return False


def test_webhook_logs():
    """웹훅 로그 조회 테스트"""
    print("\n📋 테스트 3: 웹훅 로그 조회")
    print("-" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/webhook/logs")
        print(f"상태 코드: {response.status_code}")
        data = response.json()
        print(f"총 로그 수: {data['total_count']}")
        
        assert response.status_code == 200
        assert 'logs' in data
        print("✅ 테스트 통과!")
        return True
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
        return False


def test_multiple_webhooks():
    """여러 웹훅 수신 테스트"""
    print("\n📋 테스트 4: 여러 웹훅 수신")
    print("-" * 40)
    
    events = [
        {"event": "user.created", "user_id": 1},
        {"event": "user.updated", "user_id": 2},
        {"event": "user.deleted", "user_id": 3},
    ]
    
    success_count = 0
    try:
        for i, event in enumerate(events, 1):
            response = requests.post(f"{BASE_URL}/webhook", json=event)
            if response.status_code == 200:
                success_count += 1
                print(f"  이벤트 {i}: {event['event']} - 수신 완료")
        
        assert success_count == len(events)
        print(f"✅ 테스트 통과! ({success_count}/{len(events)} 성공)")
        return True
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
        return False


def run_all_tests():
    """모든 테스트 실행"""
    print("=" * 50)
    print("🧪 웹훅 1차 테스트 시작")
    print("=" * 50)
    
    results = []
    results.append(("서버 상태 확인", test_health_check()))
    results.append(("JSON 웹훅 수신", test_webhook_json()))
    results.append(("웹훅 로그 조회", test_webhook_logs()))
    results.append(("여러 웹훅 수신", test_multiple_webhooks()))
    
    print("\n" + "=" * 50)
    print("📊 테스트 결과 요약")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 통과" if result else "❌ 실패"
        print(f"  {name}: {status}")
    
    print("-" * 40)
    print(f"결과: {passed}/{total} 테스트 통과")
    
    if passed == total:
        print("\n🎉 모든 테스트가 성공했습니다!")
        return 0
    else:
        print("\n⚠️ 일부 테스트가 실패했습니다.")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
