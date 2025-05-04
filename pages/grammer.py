import streamlit as st
import speech_recognition as sr
from openai import OpenAI
import os
from dotenv import load_dotenv

# Streamlit 페이지 설정을 가장 먼저 실행
st.set_page_config(
    page_title="English Grammar Checker",
    page_icon="📝",
    layout="centered"
)

# .env 파일 로드
load_dotenv()

# 세션 상태 초기화
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = os.getenv("OPENAI_API_KEY", "")
if "is_api_key_valid" not in st.session_state:
    st.session_state.is_api_key_valid = False

def validate_api_key(api_key):
    """
    OpenAI API 키의 유효성을 검사하는 함수
    """
    try:
        client = OpenAI(api_key=api_key)
        # 간단한 API 호출로 키 검증
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        return True
    except Exception as e:
        return False

st.title("📝 English Grammar Checker")

# OpenAI API 키 설정 섹션
st.markdown("""
## OpenAI API 키 설정 ⚙️

1. 아래 입력창에 OpenAI API 키를 입력해주세요.
2. API 키를 붙여넣고 Enter 키를 누르세요.
3. API 키가 유효하면 녹색 체크 표시가 나타납니다.

API 키가 없으신가요? [OpenAI API 키 생성하기](https://platform.openai.com/account/api-keys)
""")

# API 키 입력 필드
api_key_input = st.text_input(
    "OpenAI API 키를 입력하세요",
    type="password",
    value=st.session_state.openai_api_key,
    placeholder="OpenAI API Key",
    help="API 키가 없다면 https://platform.openai.com/account/api-keys 에서 생성하실 수 있습니다."
)

if not api_key_input:
    st.error("""
    ⚠️ OpenAI API 키가 필요합니다!
    
    1. 위의 입력창에 OpenAI API 키를 입력해주세요.
    2. API 키를 붙여넣고 Enter 키를 누르면 자동으로 검증됩니다.
    3. 유효한 API 키를 입력하면 문법 검사 기능을 사용하실 수 있습니다.
    """)
    st.stop()

if api_key_input:
    if api_key_input != st.session_state.openai_api_key:
        st.session_state.openai_api_key = api_key_input
        st.session_state.is_api_key_valid = validate_api_key(api_key_input)
        if st.session_state.is_api_key_valid:
            st.success("✅ API 키가 유효합니다!")
        else:
            st.error("❌ 유효하지 않은 API 키입니다.")
elif not st.session_state.openai_api_key:
    st.stop()

# API 키가 유효하지 않으면 여기서 중단
if not st.session_state.is_api_key_valid:
    st.error("유효한 OpenAI API 키를 입력해주세요.")
    st.stop()

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=st.session_state.openai_api_key)

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
5. 학습할 어휘
6. 예문
7. 관련 학습 자료
8. 작문 스타일 제안

분석할 문장: "{text}"

응답은 다음과 같은 형식으로 작성해주세요:

문법 평가: [점수]/100

발견된 오류:
- [오류 설명]

수정된 문장:
"[수정된 영문]"

상세 설명:
[문법 오류와 수정 사항에 대한 자세한 설명]

학습할 어휘:
- [단어/표현]: [의미]
- 난이도: [초급/중급/고급]
- 유의어/반의어: [관련 단어들]

예문:
1. [예문 1]
2. [예문 2]
3. [예문 3]

관련 학습 자료:
- YouTube 영상: [추천 영상 링크]
- 온라인 학습 자료: [관련 웹사이트 링크]
- 추천 책/교재: [도서명]

작문 스타일 제안:
- [개선을 위한 제안사항]
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 전문 영어 교사이자 문법 검사기입니다. 문법 교정뿐만 아니라 어휘 학습과 관련 자료도 제공하여 종합적인 영어 학습이 가능하도록 한국어로 상세하고 건설적인 피드백을 제공해주세요."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"분석 중 오류가 발생했습니다: {str(e)}")
        return None

# 예제 문장 리스트
EXAMPLE_SENTENCES = [
    "I goed to school yesterday.",  # 기본 시제 오류
    "She have three cats in her house.",  # 동사 일치 오류
    "I am study English very hard.",  # 진행형 오류
    "If I will have money, I will buy a car.",  # 조건문 오류
    "I very like pizza and hamburger.",  # 어순 오류
    "He told to me about his dream.",  # 전치사 사용 오류
    "I have been living in Korea since 5 years.",  # 현재완료 시제 오류
    "The weather is more cold than yesterday.",  # 비교급 오류
    "Every students in this class is smart.",  # 수의 일치 오류
    "I am interesting in learning English.",  # 형용사/분사 오류
]

st.markdown("""
    ### 영어 문법 검사기
    말하거나 입력한 영어 문장의 문법을 검사하고 개선 방안을 제시합니다.
    
    #### 기능
    - 문법 점수 평가 (100점 만점)
    - 문법 오류 지적
    - 수정된 문장 제안
    - 핵심 어휘 학습
    - 예문 제시
    - 관련 학습 자료 추천
    - 자세한 설명과 작문 스타일 제안
""")

# 입력 방식 선택
input_method = st.radio(
    "입력 방식을 선택하세요:",
    ["음성 입력", "텍스트 입력", "예제 문장 선택"]
)

if input_method == "음성 입력":
    if st.button("🎤 음성 녹음 시작", key="record"):
        input_text = recognize_speech()
        if input_text:
            st.session_state.input_text = input_text
elif input_method == "예제 문장 선택":
    selected_example = st.selectbox(
        "분석할 예제 문장을 선택하세요:",
        EXAMPLE_SENTENCES,
        format_func=lambda x: f"📝 {x}"
    )
    if selected_example:
        st.session_state.input_text = selected_example
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