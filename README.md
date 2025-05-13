# 📰 CLI파일

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


## 🚀 실행 방법 (CLI 기반 뉴스 요약기)

이 프로젝트는 CLI(Command Line Interface) 환경에서 한국어 및 영어 뉴스 기사를 자동으로 요약하고 제목을 생성하는 도구입니다.

### 1. 의존성 설치

먼저 필요한 패키지를 설치하세요:

```bash
pip install -r requirements.txt

### 2. CLI 실행

다음 명령어를 **프로젝트 루트 디렉토리 (`News-Summary-Helper/`)에서** 실행하세요:

```bash
python -m CLI.runcli


##예시용 url
https://www.khan.co.kr/article/202505121732001
