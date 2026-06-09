import streamlit as st
from google import genai

# 페이지 설정
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💖",
)

st.title("💖 연애상담 챗봇")
st.caption("Gemini 2.5 Flash Lite 기반")

# API 키 확인
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("API 키를 불러올 수 없습니다. Secrets 설정을 확인하세요.")
    st.stop()

# 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요! 😊\n\n"
                "연애 고민, 썸, 이별, 고백, 인간관계 등 편하게 이야기해 주세요."
            )
        }
    ]

# 이전 대화 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력
prompt = st.chat_input("고민을 입력하세요...")

if prompt:
    # 사용자 메시지 저장
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Gemini용 대화 기록 구성
        history_text = ""

        for msg in st.session_state.messages:
            role = "사용자" if msg["role"] == "user" else "상담사"
            history_text += f"{role}: {msg['content']}\n"

        system_prompt = """
당신은 따뜻하고 공감 능력이 뛰어난 연애 상담사입니다.

규칙:
1. 공감하는 태도로 답변한다.
2. 현실적이고 건설적인 조언을 제공한다.
3. 상대방을 비난하지 않는다.
4. 지나친 단정은 피한다.
5. 답변은 한국어로 작성한다.
"""

        full_prompt = f"""
{system_prompt}

대화 기록:
{history_text}

상담사:
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=full_prompt
        )

        answer = response.text

    except Exception as e:
        answer = f"⚠️ 오류가 발생했습니다.\n\n{str(e)}"

    # 응답 표시
    with st.chat_message("assistant"):
        st.markdown(answer)

    # 기록 저장
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
