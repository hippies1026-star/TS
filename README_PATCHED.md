# TreaSurv patched prototype

이번 패치의 목적은 기존 UI를 버리지 않고, 공모전 시연에서 필요한 데이터 흐름을 실제로 연결하는 것입니다.

## 주요 수정

- 사이드바를 접은 뒤 다시 펼칠 수 있도록 Streamlit 기본 collapse/expand control 복구
- 모든 데모 데이터를 `st.session_state`에 저장해 rerun 시 유지하고 세션 간 데이터 오염 방지
- Cash Position 계좌잔액 변경 → Total Cash → Runway / Survival Floor / Investable Cash 자동 재계산
- Business Plans 추가·삭제 → Forecast와 AI CFO에 즉시 반영
- Forecast를 하드코딩 이벤트에서 실제 사업계획 기반 계산으로 변경
- Base Forecast와 Stress Forecast 동시 표시
- Scenario Lab의 매출/비용 스트레스와 비상예비자금을 공통 Treasury Policy에 저장
- Overview / Survival Floor / Forecast / AI CFO가 동일한 정책을 사용
- AI CFO에 사업계획 Forecast Tool 추가
- GROQ API 키 미설정/호출 실패 시 앱 전체가 죽지 않도록 fallback 처리
- Treasury Policy 승인 → Audit Log 기록
- Reports View, Team Invite, Settings Save, Reset Demo Data 동작 구현
- 공모전 시연에서 운용가능자금이 0원이 되지 않도록 데모 현금구성 조정
- `requirements.txt`, `.env.example`, Windows 실행 배치파일 추가

## 적용 방법

### 기존 프로젝트에 덮어쓰기

`TreaSurv_patch_only.zip`의 파일을 기존 TreaSurv 프로젝트 루트에 그대로 덮어쓰는 방식이 가장 간단합니다.

기존 `.env`와 `.venv`는 유지하세요. 패치 ZIP에는 API 키가 포함되어 있지 않습니다.

### 실행

기존 가상환경이 있다면:

```bat
run_treasurv.bat
```

또는:

```bat
.venv\Scripts\activate
streamlit run app.py --server.port 8517
```

새 환경이라면:

```bat
pip install -r requirements.txt
streamlit run app.py --server.port 8517
```

## 데모 로그인

- Email: `demo@treasurv.ai`
- Password: `demo1234`

## AI CFO

기존 `.env` 파일에 아래 값이 있어야 AI CFO가 실제 호출됩니다.

```env
GROQ_API_KEY=YOUR_KEY
GROQ_MODEL=openai/gpt-oss-120b
```

API 키가 없거나 호출이 실패해도 재무 계산·Forecast·Scenario 기능은 계속 동작합니다.

## Forecast 계획 반영 규칙

프로토타입에서는 아래 규칙으로 현금흐름을 계산합니다.

- Hiring: 계획월부터 월별 반복 비용
- Revenue: 계획월부터 월별 반복 매출 증가
- Expense: 계획월의 일회성 비용
- Funding: 계획월의 일회성 현금유입

이 가정은 Forecast 화면에도 표시됩니다.
