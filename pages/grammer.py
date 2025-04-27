import streamlit as st
import speech_recognition as sr
from openai import OpenAI
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# OpenAI API 키 설정
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("OpenAI API 키가 설정되지 않았습니다. .env 파일을 확인해주세요.")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

def recognize_speech():
    """
    음성을 텍스트로 변환하는 함수
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 말씀해 주세요... (마이크 조정 중)")
        recognizer.adjust_for_ambient_noise(source)
        st.info("🎤 이제 말씀하세요!")
        audio = recognizer.listen(source, timeout=20)
        st.info("✨ 음성 처리 중...")

    try:
        # 영어로 인식
        text = recognizer.recognize_google(audio, language="en-US")
        return text
    except sr.UnknownValueError:
        st.error("❌ 음성을 인식하지 못했습니다.")
        return None
    except sr.RequestError:
        st.error("❌ 음성 인식 서비스에 문제가 있습니다.")
        return None

def analyze_grammar(text):
    """
    GPT-4를 사용하여 문법을 분석하고 교정하는 함수
    """
    prompt = f"""Please analyze the following English sentence and provide the feedback in Korean:
1. 문법 평가 점수 (100점 만점)
2. 발견된 오류 (있는 경우)
3. 수정된 문장
4. 수정 내용 설명
5. 작문 스타일 제안

분석할 문장: "{text}"

응답은 다음과 같은 형식으로 작성해주세요:

문법 평가: [점수]/100

발견된 오류:
- [오류 설명]

수정된 문장:
"[수정된 영문]"

상세 설명:
[문법 오류와 수정 사항에 대한 자세한 설명]

작문 스타일 제안:
- [개선을 위한 제안사항]
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 전문 영어 교사이자 문법 검사기입니다. 한국어로 상세하고 건설적인 피드백을 제공해주세요."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"분석 중 오류가 발생했습니다: {str(e)}")
        return None

# Streamlit UI
st.set_page_config(
    page_title="English Grammar Checker",
    page_icon="📝",
    layout="centered"
)

st.title("📝 English Grammar Checker")
st.markdown("""
    ### 영어 문법 검사기
    말하거나 입력한 영어 문장의 문법을 검사하고 개선 방안을 제시합니다.
    
    #### 기능
    - 문법 점수 평가 (100점 만점)
    - 문법 오류 지적
    - 수정된 문장 제안
    - 자세한 설명과 작문 스타일 제안
""")

# 입력 방식 선택
input_method = st.radio(
    "입력 방식을 선택하세요:",
    ["음성 입력", "텍스트 입력"]
)

if input_method == "음성 입력":
    if st.button("🎤 음성 녹음 시작", key="record"):
        input_text = recognize_speech()
        if input_text:
            st.session_state.input_text = input_text
else:
    input_text = st.text_area("영어 문장을 입력하세요:", height=100)
    if input_text:
        st.session_state.input_text = input_text

# 분석 버튼
if st.button("문법 분석하기", type="primary"):
    if "input_text" in st.session_state and st.session_state.input_text:
        with st.spinner("문법을 분석하고 있습니다..."):
            analysis = analyze_grammar(st.session_state.input_text)
            if analysis:
                st.markdown("### 분석 결과")
                st.write(analysis)
    else:
        st.warning("분석할 텍스트를 입력해주세요.")