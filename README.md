# Daily English Conversation

> 매일 아침 7시, AI가 엄선한 영어회화 표현 15개가 웹으로 배달됩니다.

<p align="center">
  <img src="https://img.shields.io/badge/Gemini_3_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Gemini">
  <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white" alt="Actions">
  <img src="https://img.shields.io/badge/GitHub_Pages-222222?style=for-the-badge&logo=githubpages&logoColor=white" alt="Pages">
</p>

---

## Features

**AI 콘텐츠 생성**
- Google Gemini 3 Flash Preview로 매일 새로운 표현 15개 생성
- 단어, 구문, 숙어, 구동사를 균형 있게 혼합
- 한글 발음 표기, 자연스러운 한국어 뜻과 설명
- 예문 2개 이상 + 유의어/반의어 제공

**간격 반복 학습 (Spaced Repetition)**
- Leitner 5-Box 시스템으로 과학적 복습 스케줄링
- Box 1(1일) → Box 2(3일) → Box 3(7일) → Box 4(14일) → Box 5(30일) → 완료
- 하루 최대 15개 복습, 낮은 Box 우선

**웹 버전 (GitHub Pages)**
- 카드 슬라이드 UI로 한 장씩 넘기며 학습
- 학습/복습 탭 분리
- Web Speech API로 모든 표현, 예문, 유의어, 반의어 발음 듣기
- 키보드 화살표 + 버튼 네비게이션
- 날짜별 네비게이션

**완전 자동화**
- GitHub Actions 크론으로 매일 KST 07:00 실행
- 서버 불필요, 100% 무료 운영

---

## Architecture

```
GitHub Actions (cron: KST 07:00)
        │
        ▼
  ┌─────────────┐     ┌──────────────┐
  │ Gemini API  │────▶│   15 표현     │
  │ (JSON 생성)  │     │  (JSON data) │
  └─────────────┘     └──────┬───────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
        ┌──────────┐                ┌──────────────┐
        │   Web    │                │   History     │
        │ (HTML+JS)│                │ (Leitner Box) │
        └────┬─────┘                └──────────────┘
             │
             ▼
       GitHub Pages
```

---

## Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/kCMI113/english-daily.git
cd english-daily
conda env create -f environment.yml
conda activate english-daily
```

### 2. Local Test

```bash
export GEMINI_API_KEY="your-api-key"
python -m src.main              # 오늘 날짜로 생성
python -m src.main 2025-01-15   # 특정 날짜로 생성
```

생성된 파일:
- `docs/{date}.html` - 웹 버전

### 3. GitHub Actions 설정

Repository Settings > Secrets and variables > Actions:

| Secret | Description |
|--------|-------------|
| `GEMINI_API_KEY` | Google AI Studio API Key |

### 4. GitHub Pages 설정

Settings > Pages > Source: **Deploy from a branch** > Branch: `main` / Folder: `/docs`

---

## Configuration

`config.yaml`에서 학습 설정을 조정할 수 있습니다:

```yaml
study:
  difficulty: intermediate  # beginner, intermediate, advanced
  expressions_per_day: 15
  max_review_items: 15

category:
  name: daily_conversation
  label_ko: "일상 영어회화"

spaced_repetition:
  intervals:
    1: 1    # Box 1 → 1일 후 복습
    2: 3    # Box 2 → 3일 후 복습
    3: 7    # Box 3 → 7일 후 복습
    4: 14   # Box 4 → 14일 후 복습
    5: 30   # Box 5 → 30일 후 완료
```

---

## Project Structure

```
english-daily/
├── .github/workflows/
│   └── daily-english.yml    # GitHub Actions 스케줄링
├── src/
│   ├── main.py              # 오케스트레이터
│   ├── llm_client.py        # Gemini API 래퍼
│   ├── content_generator.py # 프롬프트 엔지니어링 + 파싱
│   ├── spaced_repetition.py # Leitner Box 시스템
│   └── web_builder.py       # 웹 페이지 생성
├── templates/
│   └── web_template.html    # 웹 Jinja2 템플릿 (카드 UI + TTS)
├── data/
│   ├── history.json         # 학습 이력 (자동 커밋)
│   └── content_log.json     # 생성 콘텐츠 아카이브
├── docs/                    # GitHub Pages (자동 생성)
├── config.yaml              # 학습 설정
├── environment.yml          # Conda 환경
└── requirements.txt         # pip 의존성
```

---

## Tech Stack

| Component | Technology | Cost |
|-----------|-----------|------|
| LLM | Google Gemini 3 Flash Preview | Free |
| Scheduling | GitHub Actions | Free |
| Web Hosting | GitHub Pages | Free |
| TTS | Web Speech API (browser built-in) | Free |

---

## License

MIT
