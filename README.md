# Catch Up AI Translator

## 프로젝트 소개
이 프로젝트는 Vibe Coding의 AI 번역 앱 개발 프로젝트로, 누구나 참여할 수 있는 Open Project입니다.
[Catch Up AI](https://www.youtube.com/@catchupai) 유튜브 채널의 Live 방송 참여자들과 함께 만들어가는 협업 프로젝트입니다.

## 프로젝트 목표
- 비영어권과 영어권 사용자 간의 원활한 의사소통 지원
- AI 기술을 활용한 실시간 음성 번역 서비스 구현
- 참여자들의 Vibe Coding 경험 축적 및 노하우 공유

## 주요 기능
1. 실시간 음성 번역
   - 다국어 자동 감지
   - 실시간 음성 인식 및 번역
   - 번역된 텍스트의 음성 출력

2. 확장 가능한 기능 (개발 예정)
   - 회의 녹음 및 자동 회의록 작성
   - 강의/수업 내용 자동 정리
   - 참여자들의 제안에 따른 추가 기능

## 사용 기술
- OpenAI GPT-4 API: 고품질 텍스트 번역
- Speech Recognition: 실시간 음성 인식
- gTTS (Google Text-to-Speech): 번역된 텍스트의 음성 변환
- Streamlit: 웹 인터페이스 구현
- Python: 주요 개발 언어
- PyAudio: 오디오 입출력 처리
- Pygame: 오디오 재생

## 설치 및 실행 방법
1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

2. OpenAI API 키 설정:
- .env 파일에 API 키 추가:
```
OPENAI_API_KEY=your-api-key-here
```

3. 애플리케이션 실행:
```bash
streamlit run main.py
```

## 프로젝트 특징
이 프로젝트는 Vibe Coding의 즉흥적인 특성을 최대한 활용하는 실험적인 프로젝트입니다.
성공과 실패에 얽매이지 않고, 참가자들이 Vibe Coding을 깊이 이해하고 실무 경험을 쌓는 것에 중점을 둡니다.

## 함께 작업한 분들
이 프로젝트에 기여해 주신 분들의 명단입니다:

- Patrick Seo
- 이홍범 (문법 검사기 기능 개선)

<!-- 
참여자 정보는 다음과 같은 형식으로 추가됩니다:
- 이름/아이디 [LinkedIn](링크주소) [GitHub](링크주소)
-->

## 라이센스
이 프로젝트는 MIT 라이센스 하에 제공되며, 개인 또는 상업적 목적으로 자유롭게 사용할 수 있습니다.
단, 다음 출처를 반드시 포함해야 합니다:

- YouTube 채널: [Catch Up AI](https://www.youtube.com/@catchupai)

## 참여 방법
1. [Catch Up AI](https://www.youtube.com/@catchupai) 유튜브 채널의 라이브 방송 참여
2. GitHub를 통한 코드 기여
3. 새로운 기능 제안 및 토론 참여