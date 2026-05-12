# 프로젝트 요약: B2B Market & Channel Scanner

**글로벌 시장 스캔을 통해 미국 시장의 채널별 sell-through 전략을 도출하는 포트폴리오 프로젝트**

> 본 프로젝트는 공개 데이터(UN Comtrade, World Bank, Google Trends)와 18개 리테일러 웹사이트의 수동 리서치를 기반으로 작성했습니다. APR 내부 매출, 마진, 재고, 바이어 데이터는 사용하지 않았습니다.

---

## 1. 프로젝트 개요

K-beauty 기업의 B2B 글로벌영업팀이 시장 진입 및 채널 확장 기회를 평가하는 분석 과정을 재현한 포트폴리오 프로젝트입니다.

미국, 유럽 6개국, CIS 3개국 총 9개국을 대상으로 글로벌 시장 스캔을 수행한 뒤, 수입 규모, 구매력, 규제 안정성, 기존 채널 존재감을 기준으로 미국을 핵심 시장으로 좁혔습니다. 유럽 및 CIS 리서치는 미국 바이어 미팅 시 크로스마켓 레퍼런스로 활용할 수 있습니다.

| 항목 | 내용 |
|---|---|
| 분석 범위 | 9개국, 18개 리테일러, 11개 Account Brief |
| 미국 채널 | Amazon, TikTok Shop, Ulta, Target |
| 유럽 벤치마크 | Douglas, Boots, DM, Rossmann, Notino, Sephora FR, Primor |
| 결과물 | Streamlit 대시보드 (4탭) + **바이어별 PDF Account Brief 자동 생성** |

---

## 2. 왜 미국인가

4개 시나리오(기본, 성장중심, 리스크통제, 채널확장)로 9개국을 평가한 결과, UAE가 진입 기회 점수 1위를 기록했지만 미국을 핵심 시장으로 선정했습니다.

그 이유는 세 가지입니다:

- **압도적 수입 규모**: HS 3304 화장품 수입액 $10.2억 (2023년 기준), 2위 대비 약 10배
- **기존 채널 존재감**: Amazon, Ulta, Target, TikTok Shop에서 Medicube/Aprilskin 리스팅 확인
- **명확한 과제**: 미국은 신규 진입이 아닌 sell-through 확대, SKU 생산성 개선, 채널 간 가격 관리가 핵심

---

## 3. 핵심 방법론

### Stage 1: 글로벌 시장 스코어링

UN Comtrade 수입 데이터, World Bank 경제지표, Google Trends 검색 신호, 규제/경쟁 전문가 평가를 결합하여 9개국의 시장 기회 점수를 산출했습니다. 4개 시나리오별 민감도 분석을 통해 순위 안정성을 검증했습니다.

### Stage 2: 리테일러 수동 검증 (18개 채널)

가장 중요한 단계입니다. 직접 리테일러 웹사이트를 방문하여 K-beauty 카테고리 구조, 브랜드 필터, Medicube/Aprilskin 입점 여부, 제품 수, 가격대를 확인했습니다.

이 수동 리서치가 초기 스코어링 가설을 뒤집은 사례들:

| 국가 | 초기 가설 | 리서치 후 변경 | 근거 |
|---|---|---|---|
| 영국 | Whitespace 후보 | 경쟁 시장 (account growth) | Boots 486제품, Medicube 13 SKU 기입점 |
| 독일 | Whitespace 후보 | 경쟁 시장 (차별화 필요) | Douglas 715제품, Rossmann ISANA PB 발견 |
| 스페인 | Whitespace 후보 | 재활성화 기회 | Primor 1,031제품, Medicube 13 SKU "Not Available" |
| 카자흐스탄 | 경쟁 거의 없음 | 마켓플레이스 기반 공급 존재 | Kaspi.kz 28,213건 (중복 보정 약 3,500-4,000) |

### Stage 3: 미국 채널 전략

미국 4개 채널(Amazon, TikTok Shop, Ulta, Target)에 대해 제품-채널 적합도 매트릭스를 작성하고, 채널 간 가격 충돌 리스크를 분석했습니다.

---

## 4. 미국 채널 우선순위

단기 성장 레버리지 기준으로 정렬했습니다 (채널 위상이 아닌 실행 가능성 기준).

| 순위 | 채널 | 역할 | 핵심 신호 |
|---|---|---|---|
| 1 | Amazon | 수요 검증 채널 | 487개 결과, Zero Pore Pad 121K+ 공개 평점/리뷰 |
| 2 | TikTok Shop | 성장 가속 채널 | 5.7M+ 공개 판매 수, Aprilskin 성장 여지 |
| 3 | Ulta | 프리미엄 리테일 | 1,338개 K-beauty 제품, Featured Brand 배치 |
| 4 | Target | 매스 리테일 확장 | 558개 K-beauty 제품, Ulta 파트너십 종료 후 전환 |
| 5 | Costco | 탐색적 가설 | 86개 Korean skincare 결과, Medicube 미확인 |

---

## 5. 주요 발견

**채널 간 가격 충돌**: TikTok Shop에서 관찰된 공격적 할인(정가 대비 50-65%)이 Amazon/Ulta/Target과의 가격 충돌 리스크를 만듭니다. TikTok 전용 번들로 포맷을 차별화하는 것을 권장합니다.

**Aprilskin TikTok 성장 갭**: Medicube 5.7M+ vs Aprilskin 53.5K (공개 판매 수 기준). Medicube의 콘텐츠 전략(번들 포맷, 높은 영상 수)을 Aprilskin에 적용할 수 있는 여지가 있는 것으로 보입니다.

**Target-Ulta 파트너십 종료**: Ulta Beauty at Target (600+ 매장, 2021년 시작)이 2026년 8월 종료됩니다. Target이 자체 뷰티 경험을 구축하는 전환기에 K-beauty 브랜드 파트너십 기회가 생길 수 있는 타이밍 신호로 볼 수 있습니다.

**유럽 크로스마켓 레퍼런스**: Amazon 121K+ 리뷰 + Notino top-rated 가시성은 신규 리테일러 피칭 시 수요 검증 근거로 활용할 수 있습니다.

---

## 6. 결과물

Streamlit 대시보드 4탭(글로벌 스캔, 미국 채널 맵, SKU x 채널 적합도, Account Brief)과 함께, **바이어별 Account Brief를 PDF로 자동 생성**할 수 있습니다.

**PDF Account Brief 구성:**

- 채널 개요 (채널 유형, 규모, K-beauty 경쟁 현황, APR 입점 상태)
- 근거 수준 표시 (Public-source validated / Public metrics observed / Partially validated 등)
- 바이어에게 요청할 핵심 액션 (Primary Buyer Ask)
- 상업 가설 (Commercial Hypothesis)
- 제품 라인업 (브랜드별 구분: Medicube / Aprilskin)
- Go/No-Go 기준
- 바이어 대응 시나리오 (Key Considerations)
- 국가 기회 점수

현재 미국 4개 채널(Amazon, TikTok Shop, Ulta, Target)과 유럽 벤치마크 7개 채널(Boots, Douglas, DM, Rossmann, Notino, Sephora France, Primor), 총 **11개 Account Brief PDF를 생성**할 수 있습니다.

---

## 7. 근거 수준 구분

| 수준 | 의미 | 예시 |
|---|---|---|
| 관찰(Observed) | 공개 리테일러 페이지에서 직접 확인 | Boots에서 Medicube 13 SKU 확인 |
| 추론(Inferred) | 관찰된 신호에 기반한 해석 | Sephora France 에디토리얼 갭 |
| 제안(Proposed) | 바이어 대화용 영업 가설 | AGE-R 디바이스 인스토어 데모 파일럿 |

---

