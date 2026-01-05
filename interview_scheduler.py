"""
인터뷰 스케줄링 시스템
- 인터뷰 가능 시간 설정
- 인터뷰 예약
- 인터뷰 목록 조회
"""

from datetime import datetime, timedelta
from typing import Optional
import json
import os

DATA_FILE = "interview_data.json"


class InterviewScheduler:
    """인터뷰 스케줄링을 관리하는 클래스"""
    
    def __init__(self):
        self.available_slots: list[dict] = []  # 가능한 시간대
        self.scheduled_interviews: list[dict] = []  # 예약된 인터뷰
        self._load_data()
    
    def _load_data(self):
        """저장된 데이터 로드"""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.available_slots = data.get('available_slots', [])
                self.scheduled_interviews = data.get('scheduled_interviews', [])
    
    def _save_data(self):
        """데이터 저장"""
        data = {
            'available_slots': self.available_slots,
            'scheduled_interviews': self.scheduled_interviews
        }
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_available_slot(self, date: str, start_time: str, end_time: str, interviewer: str = "면접관") -> dict:
        """
        인터뷰 가능 시간대 추가
        
        Args:
            date: 날짜 (YYYY-MM-DD 형식)
            start_time: 시작 시간 (HH:MM 형식)
            end_time: 종료 시간 (HH:MM 형식)
            interviewer: 면접관 이름
            
        Returns:
            생성된 슬롯 정보
        """
        slot = {
            'id': len(self.available_slots) + 1,
            'date': date,
            'start_time': start_time,
            'end_time': end_time,
            'interviewer': interviewer,
            'is_booked': False,
            'created_at': datetime.now().isoformat()
        }
        self.available_slots.append(slot)
        self._save_data()
        return slot
    
    def get_available_slots(self, date: Optional[str] = None) -> list[dict]:
        """
        예약 가능한 시간대 조회
        
        Args:
            date: 특정 날짜로 필터링 (선택)
            
        Returns:
            예약 가능한 슬롯 목록
        """
        available = [s for s in self.available_slots if not s['is_booked']]
        if date:
            available = [s for s in available if s['date'] == date]
        return available
    
    def schedule_interview(self, slot_id: int, candidate_name: str, candidate_email: str, 
                          position: str = "일반") -> Optional[dict]:
        """
        인터뷰 예약
        
        Args:
            slot_id: 예약할 시간대 ID
            candidate_name: 지원자 이름
            candidate_email: 지원자 이메일
            position: 지원 포지션
            
        Returns:
            예약된 인터뷰 정보 (실패시 None)
        """
        # 해당 슬롯 찾기
        slot = None
        for s in self.available_slots:
            if s['id'] == slot_id and not s['is_booked']:
                slot = s
                break
        
        if not slot:
            return None
        
        # 슬롯을 예약됨으로 변경
        slot['is_booked'] = True
        
        # 인터뷰 정보 생성
        interview = {
            'id': len(self.scheduled_interviews) + 1,
            'slot_id': slot_id,
            'date': slot['date'],
            'start_time': slot['start_time'],
            'end_time': slot['end_time'],
            'interviewer': slot['interviewer'],
            'candidate_name': candidate_name,
            'candidate_email': candidate_email,
            'position': position,
            'status': 'scheduled',
            'scheduled_at': datetime.now().isoformat()
        }
        self.scheduled_interviews.append(interview)
        self._save_data()
        return interview
    
    def get_scheduled_interviews(self, date: Optional[str] = None) -> list[dict]:
        """
        예약된 인터뷰 목록 조회
        
        Args:
            date: 특정 날짜로 필터링 (선택)
            
        Returns:
            예약된 인터뷰 목록
        """
        interviews = self.scheduled_interviews
        if date:
            interviews = [i for i in interviews if i['date'] == date]
        return interviews
    
    def cancel_interview(self, interview_id: int) -> bool:
        """
        인터뷰 취소
        
        Args:
            interview_id: 취소할 인터뷰 ID
            
        Returns:
            취소 성공 여부
        """
        for interview in self.scheduled_interviews:
            if interview['id'] == interview_id:
                interview['status'] = 'cancelled'
                # 슬롯 다시 열기
                for slot in self.available_slots:
                    if slot['id'] == interview['slot_id']:
                        slot['is_booked'] = False
                        break
                self._save_data()
                return True
        return False


def main():
    """데모 실행"""
    scheduler = InterviewScheduler()
    
    print("=" * 50)
    print("🗓️  인터뷰 스케줄링 시스템")
    print("=" * 50)
    
    # 가능한 시간대 추가
    print("\n📅 인터뷰 가능 시간대 설정...")
    slot1 = scheduler.add_available_slot("2026-01-06", "10:00", "11:00", "김면접관")
    slot2 = scheduler.add_available_slot("2026-01-06", "14:00", "15:00", "김면접관")
    slot3 = scheduler.add_available_slot("2026-01-07", "09:00", "10:00", "이면접관")
    
    print(f"  ✅ 슬롯 추가됨: {slot1['date']} {slot1['start_time']}-{slot1['end_time']} ({slot1['interviewer']})")
    print(f"  ✅ 슬롯 추가됨: {slot2['date']} {slot2['start_time']}-{slot2['end_time']} ({slot2['interviewer']})")
    print(f"  ✅ 슬롯 추가됨: {slot3['date']} {slot3['start_time']}-{slot3['end_time']} ({slot3['interviewer']})")
    
    # 가능한 시간대 조회
    print("\n📋 현재 예약 가능한 시간대:")
    available = scheduler.get_available_slots()
    for slot in available:
        print(f"  [{slot['id']}] {slot['date']} {slot['start_time']}-{slot['end_time']} | 면접관: {slot['interviewer']}")
    
    # 인터뷰 예약
    print("\n📝 인터뷰 예약 중...")
    interview = scheduler.schedule_interview(
        slot_id=1,
        candidate_name="홍길동",
        candidate_email="hong@example.com",
        position="백엔드 개발자"
    )
    if interview:
        print(f"  ✅ 인터뷰 예약 완료!")
        print(f"     지원자: {interview['candidate_name']}")
        print(f"     포지션: {interview['position']}")
        print(f"     일시: {interview['date']} {interview['start_time']}-{interview['end_time']}")
        print(f"     면접관: {interview['interviewer']}")
    
    # 예약된 인터뷰 목록
    print("\n📊 예약된 인터뷰 목록:")
    scheduled = scheduler.get_scheduled_interviews()
    for i in scheduled:
        status_emoji = "✅" if i['status'] == 'scheduled' else "❌"
        print(f"  {status_emoji} [{i['id']}] {i['candidate_name']} - {i['position']}")
        print(f"       일시: {i['date']} {i['start_time']}-{i['end_time']}")
    
    # 남은 가능 시간대
    print("\n📅 남은 예약 가능 시간대:")
    remaining = scheduler.get_available_slots()
    for slot in remaining:
        print(f"  [{slot['id']}] {slot['date']} {slot['start_time']}-{slot['end_time']} | 면접관: {slot['interviewer']}")
    
    print("\n" + "=" * 50)
    print("✨ 인터뷰 스케줄링 시스템 준비 완료!")
    print("=" * 50)


if __name__ == "__main__":
    main()
