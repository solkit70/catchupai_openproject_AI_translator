import streamlit as st
import speech_recognition as sr
import json
import threading
import os
from gtts import gTTS
import pygame
import time
from openai import OpenAI
import langdetect
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# OpenAI API 키 설정
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("OpenAI API 키가 설정되지 않았습니다. .env 파일을 확인해주세요.")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

# 상태 관리 초기화
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "output_text" not in st.session_state:
    st.session_state.output_text = ""
if "audio_file" not in st.session_state:
    st.session_state.audio_file = None
if "detected_language" not in st.session_state:
    st.session_state.detected_language = None

def detect_language(text):
    """
    텍스트의 언어를 감지하는 함수
    Returns language code and language name
    """
    try:
        detected = langdetect.detect(text)
        # 언어 코드와 해당하는 언어 이름을 반환
        language_names = {
            'ko': '한국어',
            'en': '영어',
            'ja': '일본어',
            'zh-cn': '중국어',
            'es': '스페인어',
            'fr': '프랑스어',
            'de': '독일어',
            'ru': '러시아어',
            'vi': '베트남어',
            'th': '태국어',
            'ar': '아랍어',
            'hi': '힌디어',
            'pt': '포르투갈어',
            'it': '이탈리아어'
        }
        return detected, language_names.get(detected, detected)
    except:
        return "en", "영어"  # 기본값으로 영어 반환

def get_tts_language(lang_code):
    """
    TTS에 사용할 언어 코드 반환
    """
    if lang_code == "ko":
        return "ko"
    return "en"

def recognize_speech():
    """
    음성을 텍스트로 변환하는 함수
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 말씀해 주세요... (마이크 조정 중)")
        recognizer.adjust_for_ambient_noise(source)
        st.info("🎤 이제 말씀하세요!")
        audio = recognizer.listen(source, timeout=5)
        st.info("✨ 음성 처리 중...")

    try:
        # 먼저 한국어로 인식 시도
        try:
            text = recognizer.recognize_google(audio, language="ko-KR")
        except:
            # 한국어 인식 실패 시 영어로 시도
            text = recognizer.recognize_google(audio, language="en-US")
        return text
    except sr.UnknownValueError:
        st.error("❌ 음성을 인식하지 못했습니다.")
        return None
    except sr.RequestError:
        st.error("❌ 음성 인식 서비스에 문제가 있습니다.")
        return None

def translate_text(text, source_lang):
    """
    OpenAI API를 사용하여 텍스트를 번역하는 함수
    """
    if source_lang == "en":
        prompt = f"Translate the following English text to Korean, preserving any proper nouns: '{text}'"
    else:
        prompt = f"Translate the following {source_lang} text to English. The input text is: '{text}'"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional translator. Translate the text naturally while preserving the original meaning."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"번역 중 오류가 발생했습니다: {str(e)}")
        return None

def handle_translation(input_text):
    """
    번역 처리와 음성 변환을 관리하는 함수
    """
    source_lang, source_lang_name = detect_language(input_text)
    st.session_state.detected_language = source_lang
    
    # 텍스트 번역
    translated_text = translate_text(input_text, source_lang)
    if translated_text:
        st.session_state.output_text = translated_text
        
        # 번역된 텍스트를 음성으로 변환
        target_lang = "ko" if source_lang == "en" else "en"
        try:
            tts = gTTS(text=translated_text, lang=get_tts_language(target_lang))
            audio_file = "output.mp3"
            tts.save(audio_file)
            st.session_state.audio_file = audio_file
        except Exception as e:
            st.error(f"음성 변환 중 오류가 발생했습니다: {str(e)}")

def play_audio(file_path):
    """
    음성 파일 재생 함수
    """
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

# Streamlit UI
st.set_page_config(
    page_title="AI 실시간 음성 번역기",
    page_icon="🎯",
    layout="centered"
)

st.title("🌎 AI 실시간 음성 번역기")
st.markdown("""
    ### 사용 방법
    1. '음성 녹음 시작' 버튼을 클릭하세요
    2. 마이크에 말씀해 주세요
    3. 자동으로 언어를 감지하여 번역합니다
    - 영어 → 한국어
    - 그 외 언어 → 영어
""")

col1, col2 = st.columns(2)
with col1:
    if st.button("🎤 음성 녹음 시작", key="record"):
        input_text = recognize_speech()
        if input_text:
            st.session_state.input_text = input_text
            handle_translation(input_text)

with col2:
    if st.session_state.audio_file and os.path.exists(st.session_state.audio_file):
        if st.button("🔊 번역 음성 재생", key="play"):
            play_audio(st.session_state.audio_file)

if st.session_state.input_text:
    st.markdown("### 📝 입력된 텍스트")
    st.info(st.session_state.input_text)
    if st.session_state.detected_language:
        source_lang, source_lang_name = detect_language(st.session_state.input_text)
        st.caption(f"감지된 언어: {source_lang_name}")

if st.session_state.output_text:
    st.markdown("### 🔄 번역된 텍스트")
    st.success(st.session_state.output_text)
    target_lang = "한국어" if st.session_state.detected_language == "en" else "영어"
    st.caption(f"번역된 언어: {target_lang}")

# 오디오 파일 표시
if st.session_state.audio_file and os.path.exists(st.session_state.audio_file):
    st.markdown("### 🎵 번역된 음성")
    with open(st.session_state.audio_file, "rb") as file:
        st.audio(file.read(), format="audio/mp3")

# 앱 종료 시 오디오 파일 정리
if st.session_state.audio_file and os.path.exists(st.session_state.audio_file):
    os.remove(st.session_state.audio_file)
    st.session_state.audio_file = None