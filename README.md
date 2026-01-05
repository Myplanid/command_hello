# 인터뷰 스케줄링 시스템

인터뷰 가능 시간을 설정하고 관리하는 시스템입니다.

## 기능

- ✅ **인터뷰 가능 시간대 설정** - 면접관이 가능한 시간대를 등록
- ✅ **인터뷰 예약** - 지원자가 가능한 시간대에 인터뷰 예약
- ✅ **인터뷰 목록 조회** - 예약된 인터뷰 및 가능한 시간대 조회
- ✅ **인터뷰 취소** - 예약된 인터뷰 취소

## 사용법

```python
from interview_scheduler import InterviewScheduler

scheduler = InterviewScheduler()

# 가능한 시간대 추가
scheduler.add_available_slot("2026-01-06", "10:00", "11:00", "김면접관")

# 가능한 시간대 조회
available = scheduler.get_available_slots()

# 인터뷰 예약
scheduler.schedule_interview(
    slot_id=1,
    candidate_name="홍길동",
    candidate_email="hong@example.com",
    position="백엔드 개발자"
)

# 예약된 인터뷰 조회
scheduled = scheduler.get_scheduled_interviews()

# 인터뷰 취소
scheduler.cancel_interview(interview_id=1)
```

## 실행

```bash
python interview_scheduler.py
```
