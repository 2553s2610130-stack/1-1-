import streamlit as st
st. title ('나는 짱이다')
st.write ('바이브코딩 재미있다!!')
import streamlit as st
from google import genai

# 페이지 설정
st.set_page_config(
    page_title="저녁 메뉴 추천 챗봇",
    page_icon="🍽️",
)

st.title("🍽️ 저녁 메뉴 추천 챗봇")
st.caption("오늘 저녁 뭐 먹을지 고민될 때 추천해드립니다!")

# API 키 확인
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error(
        "GEMINI_API_KEY가 설정되지 않았습니다. "
        "Streamlit Secrets를 확인해주세요."
    )
    st.stop()

# Gemini 클라이언트 생성
client = genai.Client(api_key=api_key)

# 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요! 🍽️\n\n"
                "현재 기분, 예산, 매운 음식 선호 여부, "
                "혼밥인지 같이 먹는지 알려주시면 "
                "저녁 메뉴를 추천해드릴게요."
            ),
        }
    ]

# 기존 대화 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
if prompt := st.chat_input("오늘 저녁 뭐 먹을까요?"):
    # 사용자 메시지 저장
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # 대화 기록 구성
            conversation = []

            for msg in st.session_state.messages:
                role = "user" if msg["role"] == "user" else "model"
                conversation.append(
                    {
                        "role": role,
                        "parts": [{"text": msg["content"]}],
                    }
                )

            system_prompt = """
당신은 저녁 메뉴 추천 전문 챗봇입니다.

규칙:
- 사용자의 상황에 맞게 메뉴를 추천한다.
- 추천 이유를 함께 설명한다.
- 한국인이 쉽게 찾을 수 있는 메뉴를 우선 추천한다.
- 3~5개 메뉴를 제안한다.
- 필요한 경우 예산, 인원, 매운맛 선호도를 추가로 질문한다.
- 답변은 친근한 한국어로 작성한다.
"""

            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=conversation + [
                    {
                        "role": "user",
                        "parts": [
                            {
                                "text": system_prompt
                            }
                        ],
                    }
                ],
            )

            answer = response.text

            st.markdown(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

        except Exception as e:
            error_message = (
                f"오류가 발생했습니다.\n\n"
                f"에러 내용: {str(e)}"
            )

            st.error(error_message)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message,
                }
            )

# 사이드바
with st.sidebar:
    st.header("설정")

    if st.button("대화 초기화"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "안녕하세요! 🍽️\n\n"
                    "오늘 저녁 메뉴를 추천해드릴게요."
                ),
            }
        ]
        st.rerun()
