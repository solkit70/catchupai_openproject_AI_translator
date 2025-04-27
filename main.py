import streamlit as st

st.set_page_config(
    page_title="Catch Up AI Translator",
    page_icon="🎯",
    layout="wide"
)

st.title("🌎 Catch Up AI Translator")

st.markdown("""
## 🚀 프로젝트 소개
Catch Up AI Translator는 언어 장벽을 넘어서기 위한 실시간 AI 번역 도구입니다.
이 프로젝트는 [Catch Up AI](https://www.youtube.com/@catchupai) 유튜브 채널의 Live 방송 참여자들과 함께 만들어가는 오픈 프로젝트입니다.

## ✨ 주요 기능
- 🎤 실시간 음성 인식
- 🔍 다국어 자동 감지
- 🤖 GPT-4 기반 고품질 번역
- 🔊 번역 결과 음성 출력
- ⚡ 20초 이내 긴 문장 번역 가능

## 🛠️ 지원하는 언어
- 한국어 ↔️ 영어 (기본)
- 일본어, 중국어, 스페인어 등 → 영어

## 📱 사용 방법
1. '음성 녹음 시작' 버튼을 클릭합니다
2. 마이크에 말씀해 주세요 (최대 20초)
3. 자동으로 언어를 감지하고 번역합니다
4. 번역된 텍스트와 음성을 확인하세요

## 🎯 개발 방향
- 실시간 자막 표시
- 대화 기록 저장
- 다국어 간 직접 번역
- 발음 교정 기능
- 회의/강의 자동 요약

## 👥 참여하기
이 프로젝트는 누구나 참여할 수 있는 오픈 프로젝트입니다.
- [Catch Up AI 유튜브 채널](https://www.youtube.com/@catchupai)의 라이브 방송 참여
- GitHub를 통한 코드 기여
- 새로운 기능 제안

## 🚀 시작하기
실시간 번역을 시작하려면 사이드바에서 'Translator'를 선택하세요.
""")

# 앱 시작 버튼
if st.button("🎯 번역기 시작하기", use_container_width=True):
    st.switch_page("translator.py")