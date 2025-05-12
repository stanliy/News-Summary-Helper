# 📰 News Summary Helper (CLI 기반)

콘솔에서 뉴스 기사 URL을 입력하면,
본문을 자동으로 추출하고 언어를 감지해  
한국어/영어 기사에 대해 AI 모델로 요약과 제목을 생성해주는 CLI 프로그램입니다.

---

## 💡 기능 요약

- ✅ 뉴스 URL로 본문 자동 추출 (newspaper3k)
- ✅ 언어 자동 감지 (langdetect)
- ✅ 한국어 기사:
  - KoBART 요약
  - KoBART 헤드라인 생성
- ✅ 영어 기사:
  - BART 요약
  - T5 헤드라인 생성

---

## 🧪 실행 방법

```bash
# 가상환경 실행 (Windows 기준)
venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt