# Tirage_Valu.pdf 최종 보안 분석 보고서

**작성일**: 2026-04-20  
**보고서 유형**: 최종 검토 보고서  
**분석 대상**: Tirage_Valu.pdf

---

## 파일 분석 최종 결과

| 항목 | 내용 |
|---|---|
| **파일명** | Tirage_Valu.pdf |
| **위험도** | ⚠️ **낮음~중간** (추가 분석 필요) |
| **파일 크기** | 246.3KB (252,221 bytes) |
| **파일 형식** | PDF 1.7 |
| **파일 해시** | |
| - MD5 | `4f7302d85571593e80b0a6eb1caa75a1` |
| - SHA256 | `2381b931f2da435d56bdbb538f7f5ce998d4f3548be330ac05fe1828666f8352` |
| **Magic Bytes** | `%PDF-1.7` (25 50 44 46 2d 31 2e 37) |
| **수정일** | 2026-04-20T05:25:20.087Z |

---

## 백신 탐지 여부

| 항목 | 상태 |
|---|---|
| VirusTotal 조회 | ⚠️ **MCP 연결 실패로 미확인** |
| 권장 조치 | SHA256 해시로 수동 VirusTotal 조회 필요 |

**참고**: Ghidra MCP 서버가 `127.0.0.1:8080`에서 연결 거부 상태이며, VirusTotal MCP 도구도 직접 호출이 불가하여 자동화된 악성코드 탐지 결과를 확보하지 못함.

---

## 정적 분석 결과

### PDF 구조 분석 (Hex Preview 기반)

| 분석 항목 | 결과 |
|---|---|
| **PDF 버전** | 1.7 (표준) |
| **객체 구조** | 정상적인 PDF 객체 구조 확인 |
| **압축 필터** | `/Filter/` 존재 (FlateDecode 예상) |

### 내부 요소 분석

| 요소 | 상세 내용 |
|---|---|
| **이미지 객체** | Image6, Image11, Image12, Image13, Image36, Image40, Image41 (7개) |
| **폰트** | F1~F9 (9개 폰트 정의) |
| **페이지 크기** | 594.96 x 841.92 pts (A4 규격) |
| **ProcSet** | `/PDF/Text/ImageB/ImageC/ImageI` (표준) |
| **Group** | Transparency/DeviceRGB (투명도 그룹) |
| **Annots** | ⚠️ `/Annots 22 0 R` - **주석 객체 존재** |

### 보안 관심 키워드 검사 (500바이트 프리뷰 범위)

| 키워드 | 탐지 여부 | 위험도 |
|---|---|---|
| `/JavaScript` | ❌ 미탐지 | - |
| `/JS` | ❌ 미탐지 | - |
| `/OpenAction` | ❌ 미탐지 | - |
| `/Launch` | ❌ 미탐지 | - |
| `/EmbeddedFile` | ❌ 미탐지 | - |
| `/URI` | ❌ 미탐지 | - |
| `/Annots` | ⚠️ **탐지됨** | 중간 |

---

## MCP 도구 원본 데이터 검증

### 이전 AI 분석 vs MCP 원본 결과 대조

| 도구 | 이전 AI 해석 | MCP 원본 결과 | 검증 결과 |
|---|---|---|---|
| `list_methods` | "유의미한 결과 없을 것" | **Connection Refused** | ⚠️ 실제로는 연결 실패 |
| `list_strings` | "문자열 추출 가능" | **Connection Refused** | ⚠️ 실제로는 연결 실패 |
| `list_imports` | "유의미한 결과 없을 것" | **Connection Refused** | ⚠️ 실제로는 연결 실패 |
| `list_exports` | - | **Connection Refused** | 연결 실패 |
| `list_segments` | - | **Connection Refused** | 연결 실패 |
| `list_classes` | - | **Connection Refused** | 연결 실패 |
| `search_cve_by_keyword` | "해주세요" 키워드 0건 | 0건 (정상) | ✅ 정확 |

### 검증 결론

**이전 AI의 오류 사항:**
1. **해시값 누락 주장 오류**: 이전 AI는 "파일의 SHA256 해시값이 제공되지 않아 VirusTotal 보고서를 가져올 수 없습니다"라고 기술했으나, **파일 정보에 SHA256이 명시되어 있음** (`2381b931f2da435d56bdbb538f7f5ce998d4f3548be330ac05fe1828666f8352`)
2. **Ghidra 분석 가능성 오해**: 이전 AI는 Ghidra 도구가 PDF에 부적합하다고 "예상"했으나, 실제로는 **MCP 서버 연결 자체가 실패**하여 분석이 불가능했음
3. **CVE 키워드 검색 오류**: "해주세요"라는 무관한 키워드로 검색 수행 (의미 없는 결과)

---

## 관련 CVE 정보

### CVE-2026-25755 (jsPDF Object Injection)

| 항목 | 내용 |
|---|---|
| **CVE ID** | CVE-2026-25755 |
| **심각도** | CVSS 8.8 (High) |
| **영향** | PDF JavaScript 실행을 통한 임의 코드 실행 |
| **취약 버전** | jsPDF < 4.2.0 |
| **공격 벡터** | `/OpenAction` 및 `/JS` 객체 인젝션 |

**참고**: 본 파일에서 직접적인 jsPDF 생성 흔적이나 해당 취약점 악용 패턴은 500바이트 프리뷰에서 확인되지 않았으나, 전체 파일 분석이 필요함.

---

## 위험 평가

### 잠재적 위험 요소

| 위험 요소 | 상세 | 위험 수준 |
|---|---|---|
| `/Annots` 객체 | 주석에 JavaScript 또는 악성 링크 포함 가능 | ⚠️ 중간 |
| 이미지 객체 다수 | 스테가노그래피 또는 익스플로잇 가능성 | 🔵 낮음 |
| PDF 1.7 버전 | JavaScript 지원 버전 | 🔵 낮음 |
| 파일 크기 | 246KB - 일반 문서 범위 | ✅ 정상 |

### 미확인 사항 (추가 분석 필요)

- [ ] 전체 파일 스트림에서 `/JavaScript`, `/JS`, `/OpenAction` 키워드 존재 여부
- [ ] `/Annots 22 0 R` 객체의 구체적 내용 (URL, 액션 포함 여부)
- [ ] VirusTotal 탐지 결과 (SHA256 수동 조회 필요)
- [ ] 임베디드 파일 또는 스트림 내 악성 페이로드 여부

---

## 행위 시나리오 (잠재적)

PDF 악성코드의 일반적인 공격 시나리오:

```
1. 사용자가 PDF 파일 오픈
          ↓
2. /OpenAction 또는 /Annots 내 JavaScript 자동 실행
          ↓
3. 외부 URL 접속 또는 추가 페이로드 다운로드
          ↓
4. 시스템 권한 탈취 또는 정보 유출
```

**본 파일 적용**: 현재 500바이트 프리뷰에서는 자동 실행 액션이 확인되지 않았으나, `/Annots` 객체로 인해 사용자 클릭 유도형 공격 가능성 존재.

---

## 주요 발견 사항

### 핵심 IoC

| IoC 유형 | 값 |
|---|---|
| SHA256 | `2381b931f2da435d56bdbb538f7f5ce998d4f3548be330ac05fe1828666f8352` |
| MD5 | `4f7302d85571593e80b0a6eb1caa75a1` |
| 파일명 | Tirage_Valu.pdf |

### MITRE ATT&CK 매핑 (잠재적)

| Tactic | Technique | ID |
|---|---|---|
| Initial Access | Spearphishing Attachment | T1566.001 |
| Execution | User Execution: Malicious File | T1204.002 |
| Execution | Exploitation for Client Execution | T1203 |

---

## 대응 권고

### 즉시 조치

1. **VirusTotal 수동 조회**
   - URL: `https://www.virustotal.com/gui/file/2381b931f2da435d56bdbb538f7f5ce998d4f3548be330ac05fe1828666f8352`
   - SHA256 해시로 기존 탐지 이력 확인

2. **격리된 환경에서 분석**
   - 샌드박스 환경에서 파일 오픈하여 동적 분석 수행
   - 네트워크 트래픽 모니터링

3. **PDF 전체 구조 분석**
   ```bash
   # 권장 도구
   pdfid.py Tirage_Valu.pdf        # 의심 키워드 탐지
   pdf-parser.py Tirage_Valu.pdf   # 객체 구조 분석
   peepdf -i Tirage_Valu.pdf       # 인터랙티브 분석
   ```

### 예방 조치

| 조치 | 상세 |
|---|---|
| PDF 뷰어 업데이트 | Adobe Reader, Foxit 최신 버전 사용 |
| JavaScript 비활성화 | PDF 리더에서 JavaScript 실행 차단 |
| 이메일 필터링 | 알 수 없는 발신자의 PDF 첨부 차단 |
| 사용자 교육 | 의심 파일 열기 전 IT 부서 확인 |

---

## 결론

### 최종 판정

| 항목 | 결과 |
|---|---|
| **현재 위험도** | ⚠️ **낮음~중간** |
| **확정 악성 여부** | ❓ **미확정** (추가 분석 필요) |
| **분석 완료도** | 약 30% (MCP 연결 실패로 제한적 분석) |

### 이전 AI 분석과의 차이점

| 항목 | 이전 AI | 최종 검토 | 근거 |
|---|---|---|---|
| SHA256 가용성 | "제공되지 않음" | **제공됨** | 파일 정보에 명시 |
| Ghidra 분석 | "부적합할 것" | **연결 실패** | MCP 오류 로그 |
| VirusTotal | "조회 불가" | **수동 조회 가능** | 해시값 존재 |
| CVE 검색 | "해주세요" 검색 | **PDF CVE 조사** | 관련 키워드 사용 |

### 최종 권고

본 PDF 파일은 500바이트 프리뷰 범위에서 명확한 악성 지표가 발견되지 않았으나, `/Annots` 객체의 존재로 인해 **잠재적 위험이 존재**합니다. MCP 도구(Ghidra, VirusTotal) 연결이 모두 실패하여 심층 분석이 제한되었습니다.

**필수 후속 조치:**
1. VirusTotal에서 SHA256 해시 수동 조회
2. 전체 PDF 스트림 파싱 및 JavaScript/액션 키워드 검색
3. 격리 환경에서 동적 분석 수행

---

*보고서 종료*
