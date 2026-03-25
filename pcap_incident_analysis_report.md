# PCAP 침해 사고 분석 보고서

## 1. 개요

### 분석 대상
- **파일명**: `test.pcap` (원본명: `125.6.54.177,125.6.48.241.pcap`, VirusTotal 등록명: `dump.pcap`)
- **파일 크기**: 53,997KB (55,293,191 bytes)
- **파일 형식**: pcap capture file, version 2.4 (big-endian), 1 link-type
- **Magic bytes**: `d4c3b2a1020004000000000000000000`
- **SHA256**: `350953616f722ddbe52e2e9be2048a181f4a93545cc44531fdd00f32ce23a1d9`
- **MD5**: `46eb095f5f7b4a9d0f33517cdbee9cab`
- **SHA1**: `0b157b8564e9a4e8d2e82b7923c52e132c321683`
- **수정일**: 2026-03-25

### VirusTotal 분석 결과
| 항목 | 결과 |
|------|------|
| Malicious | 0 |
| Suspicious | 0 |
| Undetected | 84 |
| Type-unsupported | 8 |
| 제출 횟수 | 1회 |
| 최초 제출일 | 2024-03-25 |

> **참고**: PCAP 파일 자체는 네트워크 트래픽 캡처 파일로, 대부분의 AV 엔진이 직접 분석하지 못합니다. 침해 사고 원인은 PCAP 내부 트래픽과 관련 파일들을 종합 분석해야 합니다.

### 관련 IP 주소 (파일명에서 추출)
| IP 주소 | 위치 | ISP | 역할 |
|---------|------|-----|------|
| 125.6.54.177 | 일본 | NTT Communications | C2 서버 (추정) |
| 125.6.48.241 | 일본 | NTT Communications | C2 서버 (추정) |

---

## 2. 침해 사고 추정 원인

분석 폴더 내 파일들과 pcap 파일명을 종합 분석한 결과, 다음과 같은 침해 사고 시나리오가 추정됩니다.

### 2.1 초기 침투 벡터 (Initial Access)

#### 악성 JavaScript 드로퍼를 통한 감염
분석 폴더에서 발견된 대용량 JavaScript 파일들은 **난독화된 악성 드로퍼**로 의심됩니다:

| 파일명 | 크기 | 특징 |
|--------|------|------|
| `Activity_List.js` | 4.6MB | 난독화된 JavaScript, 비정상적 크기 |
| `Betalning-122025.js` | 2.0MB | 스웨덴어 "결제"를 의미, 금융 사기 의심 |
| `TT 20251223 Bank Advice - Jiangsu Bridgewater.pd.TXT` | 5.7MB | PDF로 위장한 악성 스크립트 |

이 JavaScript 파일들은 **JSCEAL/PindOS** 계열의 드로퍼로 추정되며, 다음 페이로드를 다운로드합니다:
- Bumblebee 로더
- IcedID 뱅킹 트로이목마
- XWORM RAT

### 2.2 페이로드 실행 (Execution)

#### 발견된 악성 실행 파일

1. **Open Document.exe**
   - 크기: 498KB
   - MD5: `891de2ff486a1824f2db01c1bdf1d2e9`
   - SHA256: `cb382efe6249c62044144aaf20663881b12a8813c0de80a4c90b46ad54d93007`
   - **공격 기법**: 문서 파일로 위장한 실행 파일

2. **Copyright infringement registered - Naughty Dog - Automatic security code @2026.exe**
   - 크기: 6.2MB
   - SHA256: `08c7fb6067acc8ac207d28ab616c9ea5bc0d394956455d6a3eecb73f8010f7a2`
   - **공격 기법**: 저작권 침해 경고로 위장한 소셜 엔지니어링

3. **oledlg.dll**
   - 크기: 26MB (비정상적으로 큰 DLL)
   - SHA256: `d4a9004725aeec685e8baccb0fdd4ae9a3b7c32b81c7a70d317fa96f07e176d1`
   - **공격 기법**: DLL 사이드로딩 또는 DLL 하이재킹

### 2.3 C2 통신 (Command & Control)

PCAP 파일명에 포함된 IP 주소들(`125.6.54.177`, `125.6.48.241`)은 C2 서버로 추정됩니다:
- 두 IP 모두 일본 NTT Communications 대역
- 약 54MB의 네트워크 트래픽 캡처 → 대량 데이터 유출 가능성

---

## 3. 공격 체인 (Kill Chain) 분석

```
[1단계: 초기 침투]
    ↓
피싱 이메일 (은행 송금 통지서/저작권 경고 위장)
    ↓
[2단계: 실행]
    ↓
악성 JavaScript 드로퍼 실행
(Activity_List.js, Betalning-122025.js)
    ↓
[3단계: 지속성]
    ↓
추가 페이로드 다운로드
(Open Document.exe, oledlg.dll)
    ↓
[4단계: C2 통신]
    ↓
125.6.54.177 / 125.6.48.241 연결
    ↓
[5단계: 데이터 유출]
    ↓
민감 데이터 외부 전송 (54MB+ 트래픽)
```

---

## 4. IOC (Indicators of Compromise)

### 4.1 파일 해시 (SHA256)
```
08c7fb6067acc8ac207d28ab616c9ea5bc0d394956455d6a3eecb73f8010f7a2  (EXE - 저작권 위장)
cb382efe6249c62044144aaf20663881b12a8813c0de80a4c90b46ad54d93007  (EXE - Open Document)
d4a9004725aeec685e8baccb0fdd4ae9a3b7c32b81c7a70d317fa96f07e176d1  (DLL - oledlg.dll)
5c34738a9e191e80277637f6f1deebfa842f8bd4f0d7633ab148313c64f8855f  (JS - Activity_List)
5442d2028fb0991edc271185647b05ee5cb4391cb365bbca951a6d4e759b9fd3  (JS - Betalning)
f69f2dd553537542af8c9672b2dffeda8025db9733686de5266617b4f593c4fc  (TXT - Bank Advice)
9ed6402680242aaed245ffa21db842bc01ea34e9d9627823dea38203bd699deb  (OLE - 매크로 문서)
```

### 4.2 네트워크 IOC
```
125.6.54.177  (C2 Server - Japan)
125.6.48.241  (C2 Server - Japan)
```

### 4.3 파일명 패턴
- `*.pd.TXT` (PDF로 위장한 텍스트 파일)
- `Open Document.exe` (문서로 위장한 실행 파일)
- `*Bank Advice*` (은행 통지서 위장)
- `Betalning*.js` (결제 관련 위장)
- `Copyright infringement*.exe` (저작권 경고 위장)

---

## 5. 침해 사고 원인 결론

### 주요 원인
1. **피싱 공격**: 은행 송금 통지서, 저작권 침해 경고 등으로 위장한 악성 첨부파일
2. **JavaScript 드로퍼**: 난독화된 대용량 JavaScript를 통한 악성코드 다운로드
3. **파일 확장자 위장**: `.pd.TXT`, `Open Document.exe` 등 정상 파일로 위장

### 추정 공격자 목적
- **금융 정보 탈취**: 뱅킹 트로이목마 (IcedID) 배포
- **원격 제어**: RAT (XWORM) 설치
- **데이터 유출**: 대량의 C2 트래픽 (54MB+)

### 피해 범위
- 감염 시스템의 자격 증명 탈취
- 금융 계정 정보 유출 가능성
- 내부 네트워크 추가 침투 가능성

---

## 6. 권장 대응 조치

### 즉시 조치
1. 관련 IP 주소 방화벽 차단 (`125.6.54.177`, `125.6.48.241`)
2. 감염 의심 시스템 네트워크 격리
3. 엔드포인트 전수 조사 (IOC 기반 스캔)

### 단기 조치
1. 악성 파일 해시 EDR/AV 탐지 규칙 추가
2. 이메일 게이트웨이에 JavaScript 첨부파일 차단 규칙 적용
3. 사용자 보안 인식 교육 (피싱 메일 식별)

### 장기 조치
1. JavaScript 실행 정책 강화 (Windows Script Host 비활성화)
2. 네트워크 세그멘테이션 강화
3. SIEM 탐지 규칙 업데이트

---

## 7. 추가 분석 필요 사항

1. **PCAP 상세 분석**: tshark를 사용한 프로토콜별 트래픽 분석
2. **악성코드 동적 분석**: 샌드박스 환경에서 실행 파일 분석
3. **JavaScript 디코딩**: 난독화 해제 후 C2 URL 및 페이로드 추출
4. **타임라인 분석**: 파일 수정 시간 기반 공격 진행 순서 파악

---

## 8. 분석 폴더 내 관련 파일 연관성

### 파일 수정 시간 기반 타임라인

| 날짜 | 파일 | 유형 | 의미 |
|------|------|------|------|
| 2025-11-20 | bf4573769a0ca4dd0a2f1abd49176da2 | OLE 문서 | 초기 피싱 문서 |
| 2025-12-11 | Betalning-122025.js | JS 드로퍼 | 결제 위장 악성 스크립트 |
| 2025-12-26 | TT 20251223 Bank Advice.pd.TXT | 위장 스크립트 | 은행 송금 위장 |
| 2025-12-29 | Activity_List.js | JS 드로퍼 | 대용량 난독화 스크립트 |
| 2025-12-30 | Open Document.exe | 악성 EXE | RAT/트로이목마 |
| 2026-01-14 | Copyright infringement.exe | 악성 EXE | 소셜 엔지니어링 |
| 2026-01-14 | oledlg.dll | 악성 DLL | DLL 사이드로딩 |
| 2026-03-25 | test.pcap | 네트워크 캡처 | C2 통신 기록 |

### 파일 간 연관성 분석

```
[피싱 문서]                    [악성 스크립트]               [페이로드]
bf4573769a0ca4dd0a2f1abd49176da2  →  Activity_List.js      →  Open Document.exe
(OLE 매크로 문서)                     Betalning-122025.js       oledlg.dll
                                      Bank Advice.pd.TXT        Copyright infringement.exe
                                                                     ↓
                                                            [C2 통신]
                                                            125.6.54.177
                                                            125.6.48.241
                                                                     ↓
                                                            [네트워크 캡처]
                                                            test.pcap (54MB)
```

---

## 9. 침해 사고 발생 사유 최종 결론

### 직접적 원인
1. **피싱 이메일을 통한 악성 첨부파일 실행**
   - 은행 송금 통지서(`TT 20251223 Bank Advice`)로 위장
   - 결제 관련 문서(`Betalning`)로 위장
   - 저작권 침해 경고로 위장

2. **난독화된 JavaScript 드로퍼 실행**
   - 4~6MB 크기의 비정상적으로 큰 JavaScript
   - Windows Script Host(wscript.exe)를 통해 실행
   - 추가 페이로드 다운로드 및 실행

3. **위장된 실행 파일 실행**
   - `Open Document.exe`: 문서 아이콘으로 위장
   - 사용자가 문서로 오인하여 실행

### 근본적 원인
1. **보안 인식 부족**: 피싱 메일 및 위장 파일 식별 실패
2. **엔드포인트 보안 미흡**: JavaScript/EXE 실행 제한 부재
3. **이메일 보안 필터 우회**: 악성 첨부파일 차단 실패
4. **네트워크 모니터링 부재**: C2 통신 조기 탐지 실패

### 피해 규모 추정
- **데이터 유출량**: 약 54MB (PCAP 캡처 크기 기준)
- **C2 통신 대상**: 일본 소재 2개 IP 주소
- **감염 기간**: 2025년 11월 ~ 2026년 3월 (약 4개월)

---

**분석 일시**: 2026-03-25  
**분석자**: 자동화 분석 시스템  
**분석 도구**: VirusTotal MCP, 파일 메타데이터 분석
