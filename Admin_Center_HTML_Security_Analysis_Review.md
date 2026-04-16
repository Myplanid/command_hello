# Admin_Center_privacy1_MSA_355472266792553__(1).htm 보안 분석 검증 보고서

## 1. 분석 개요

| 항목 | 내용 |
|------|------|
| **파일명** | Admin_Center_privacy1_MSA_355472266792553__(1).htm |
| **파일 크기** | 17,584 bytes (17.2 KB) |
| **파일 형식** | HTML 문서 |
| **SHA256** | c75a8372613f1128107a92e47fa4af221f8ca2c7dbb1345ddf02da80093e91e2 |
| **MD5** | 0ef80feea69482774bb3d3f35662ddb9 |
| **최종 위험도** | **High (높음)** - 피싱 공격용 HTML 파일로 확인 |

---

## 2. 이전 AI 분석 검증 결과

### 2.1 MCP 도구 호출 결과 검토

이전 AI가 사용한 MCP 도구 호출은 다음과 같은 오류를 반환했습니다:

| 도구 | 결과 |
|------|------|
| `list_methods` (Ghidra) | Connection refused - Ghidra 서버 미연결 |
| `list_strings` (Ghidra) | Connection refused - Ghidra 서버 미연결 |
| `list_imports` (Ghidra) | Connection refused - Ghidra 서버 미연결 |
| `list_exports` (Ghidra) | Connection refused - Ghidra 서버 미연결 |
| `list_segments` (Ghidra) | Connection refused - Ghidra 서버 미연결 |
| `list_classes` (Ghidra) | Connection refused - Ghidra 서버 미연결 |
| `search_cve_by_keyword` | 결과 없음 (0건) |

**검증 의견**: 
- Ghidra MCP 도구는 HTML 파일 분석에 적합하지 않습니다. Ghidra는 바이너리 실행 파일(PE, ELF 등) 역공학 분석용 도구이므로, HTML 문서 분석에는 사용이 불필요합니다.
- CVE 검색에 "해주세요"라는 한국어 키워드를 사용한 것은 부적절한 쿼리였습니다.
- **결론**: MCP 도구 선택은 부적절했으나, HTML 파일 분석 자체는 파일 내용 기반으로 수행되어 영향 없음.

### 2.2 이전 분석 결론 검증

| 분석 항목 | 이전 AI 결론 | 검증 결과 | 평가 |
|-----------|--------------|-----------|------|
| 위험도 판정 | High | **정확함** | ✅ |
| 공격 유형 | Phishing | **정확함** | ✅ |
| Microsoft 브랜딩 사칭 | 확인됨 | **정확함** | ✅ |
| 파일 해시 정보 | "해당 데이터 없음" | **부정확** - 파일 정보에서 해시 제공됨 | ⚠️ |
| VirusTotal 탐지율 | "해당 데이터 없음" | 추가 조회 필요 | ⚠️ |
| 스크립트/폼 분석 | "나머지 파일에 있을 수 있음" | 부분 분석만 수행됨 | ⚠️ |

---

## 3. 보완 분석

### 3.1 파일 정적 분석 (제공된 HTML 코드 기반)

#### 3.1.1 HTML 메타데이터 분석

```html
<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="description" content="Admin Center SSO Portal">
    <title>Admin Center SSO</title>
```

**발견사항**:
- `lang="en"`: 영어권 사용자 대상
- `Admin Center SSO Portal`: Microsoft 365 관리 센터 SSO를 사칭
- 파일명에 `MSA` (Microsoft Account) 포함 → Microsoft 계정 피싱 의도 명확

#### 3.1.2 Microsoft 브랜드 위장 CSS 분석

```css
/* Logo Grid - Same as Original */
.logo-grid {
    width: 88px;
    height: 88px;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(2, 1fr);
    gap: 6px;
}

.logo-panel:nth-child(1) { background: #F25022; }  /* 주황색 - Microsoft 로고 색상 */
.logo-panel:nth-child(2) { background: #7FBA00; }  /* 녹색 - Microsoft 로고 색상 */
.logo-panel:nth-child(3) { background: #00A4EF; }  /* 파란색 - Microsoft 로고 색상 */
.logo-panel:nth-child(4) { background: #FFB900; }  /* 노란색 - Microsoft 로고 색상 */
```

**발견사항**:
- CSS로 Microsoft 4색 로고(Windows/Microsoft 365 로고)를 완벽히 재현
- 실제 Microsoft 색상 코드와 동일 → 고도로 정교한 피싱 기법

#### 3.1.3 진행률 표시 UI (로딩 오버레이)

```css
.progress-bar {
    width: 100%;
    height: 2px;
    background: #E8E8E8;
    border-radius: 2px;
    overflow: hidden;
}

.progress-fill {
    width: 0%;
    height: 100%;
```

**발견사항**:
- 가짜 로딩 화면 구현 → 사용자 경계심 완화 목적
- Microsoft 스타일의 Fluent Design 적용
- `user-scalable=no`: 모바일에서 확대/축소 방지 → 피싱 페이지 특성

#### 3.1.4 보안 관련 CSS 설정

```css
* {
    -webkit-user-select: none;
    user-select: none;
    -webkit-tap-highlight-color: transparent;
}

body {
    position: fixed;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
}
```

**발견사항**:
- `user-select: none`: 텍스트 선택 방지 → 소스코드 복사 방해
- `position: fixed` + `overflow: hidden`: 스크롤 방지 → 페이지 조작 방지
- 이는 피싱 페이지에서 사용자가 의심스러운 요소를 검사하지 못하도록 하는 일반적인 기법

### 3.2 추정되는 악성 동작 (미확인 영역)

파일 전체(17,584자)의 일부만 제공되었으므로, 나머지 영역에 다음이 포함될 가능성이 높습니다:

1. **자격 증명 탈취 폼**
   - 이메일/사용자명 입력 필드
   - 비밀번호 입력 필드
   - "로그인" 버튼

2. **악성 JavaScript**
   - 입력된 자격 증명을 외부 서버로 전송
   - Base64/난독화된 URL 사용
   - Telegram Bot API 또는 Discord Webhook으로 데이터 전송 가능성

3. **리다이렉션 로직**
   - 자격 증명 제출 후 실제 Microsoft 사이트로 리다이렉션
   - 피해자가 속았다는 것을 인지하지 못하게 함

---

## 4. 위협 인텔리전스

### 4.1 IoC (Indicators of Compromise)

| 유형 | 값 | 설명 |
|------|-----|------|
| 파일명 패턴 | `Admin_Center_*_MSA_*.htm` | Microsoft Admin Center 사칭 |
| SHA256 | c75a8372613f1128107a92e47fa4af221f8ca2c7dbb1345ddf02da80093e91e2 | 파일 해시 |
| MD5 | 0ef80feea69482774bb3d3f35662ddb9 | 파일 해시 |
| HTML Title | `Admin Center SSO` | 피싱 지표 |
| CSS 색상 코드 | #F25022, #7FBA00, #00A4EF, #FFB900 | Microsoft 로고 사칭 |

### 4.2 MITRE ATT&CK 매핑

| Technique ID | 기술명 | 설명 |
|--------------|--------|------|
| T1566.001 | Phishing: Spearphishing Attachment | HTML 첨부파일 형태의 피싱 |
| T1566.002 | Phishing: Spearphishing Link | 링크를 통한 피싱 페이지 접근 |
| T1598.003 | Phishing for Information: Spearphishing Link | 자격 증명 수집 목적 |
| T1204.001 | User Execution: Malicious Link | 사용자가 파일을 열도록 유도 |
| T1036.005 | Masquerading: Match Legitimate Name | Microsoft 서비스명 사칭 |

### 4.3 관련 피싱 캠페인 특성

이 파일은 **"HTML Smuggling"** 또는 **"로컬 HTML 피싱"** 기법의 일종으로 보입니다:

- 이메일 첨부파일 또는 다운로드 링크로 배포
- 브라우저에서 로컬로 실행되어 URL 기반 탐지 우회
- 정교한 CSS/JavaScript로 실제 Microsoft 로그인 페이지와 유사하게 구현

---

## 5. 대응 권고사항

### 5.1 즉시 조치

1. **파일 격리**: 해당 파일을 격리하고 삭제
2. **사용자 확인**: 파일을 열어본 사용자가 있다면 자격 증명 변경 권고
3. **이메일 검색**: 동일 파일명 패턴(`Admin_Center*MSA*.htm`)으로 조직 내 이메일 검색

### 5.2 방어 조치

| 영역 | 권고 사항 |
|------|----------|
| **이메일 보안** | `.htm`, `.html` 첨부파일 필터링 강화 |
| **엔드포인트** | HTML 파일 실행 시 경고 표시 |
| **사용자 교육** | Microsoft 브랜드 사칭 피싱 인식 교육 |
| **MFA** | 모든 계정에 다단계 인증 적용 |
| **SIEM 규칙** | `Admin_Center`, `SSO`, `MSA` 키워드 포함 HTML 파일 탐지 |

### 5.3 추가 분석 권고

- **전체 파일 분석**: 제공되지 않은 나머지 14,000+ 자의 코드 분석 필요
- **네트워크 분석**: 파일 실행 시 연결되는 외부 도메인/IP 확인
- **샌드박스 실행**: 격리된 환경에서 실제 동작 확인

---

## 6. 결론

### 6.1 이전 분석 평가

| 항목 | 평가 |
|------|------|
| **위험도 판정** | ✅ 정확 (High) |
| **공격 유형 분류** | ✅ 정확 (Phishing) |
| **정적 분석** | ⚠️ 부분 정확 (일부 누락) |
| **MCP 도구 활용** | ❌ 부적절 (Ghidra는 HTML 분석 부적합) |
| **해시 정보** | ⚠️ 누락됨 (실제로는 제공됨) |
| **대응 권고** | ✅ 적절함 |

### 6.2 최종 판정

**이 파일은 Microsoft 365 Admin Center SSO를 사칭한 피싱 HTML 파일입니다.**

- 정교한 CSS로 Microsoft 브랜드 로고를 재현
- 로딩 화면으로 사용자 경계심 완화
- 텍스트 선택/스크롤 방지로 분석 방해
- 자격 증명 탈취를 목적으로 제작된 것으로 판단됨

**위험도: High (높음)** - 즉시 삭제 및 관련 사용자 알림 필요

---

## 7. 분석 메타데이터

| 항목 | 내용 |
|------|------|
| 분석 일시 | 2026-04-16 |
| 분석자 | Cloud Agent (자동화 분석) |
| 분석 유형 | 이전 AI 분석 검증 및 보완 |
| 사용된 도구 | 정적 코드 분석, 웹 검색 |

---

*이 보고서는 제공된 파일 내용의 일부(약 17%)를 기반으로 작성되었습니다. 전체 파일 분석을 위해서는 완전한 파일 접근이 필요합니다.*
