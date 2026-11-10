from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent import ResearchAgent  # noqa: E402
from env_loader import load_lab_env  # noqa: E402
from providers import make_provider  # noqa: E402
from tools import load_tool_declarations, to_openai_tools  # noqa: E402

load_lab_env(ROOT)

st.set_page_config(page_title="Research Agent", page_icon="🔎")
st.title("🔎 Research Agent")
st.caption("Tìm kiếm web/mạng xã hội, đọc URL, tra policy và định dạng digest.")

provider_name = st.sidebar.selectbox("Provider", ["openrouter", "openai", "anthropic", "gemini", "ollama"])
version = st.sidebar.text_input("Version", "v3")

if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Bạn muốn nghiên cứu điều gì?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    try:
        provider = make_provider(provider_name)
        agent = ResearchAgent(
            provider,
            system_prompt=(ROOT / "artifacts" / "system_prompt.md").read_text(encoding="utf-8"),
            tools=to_openai_tools(load_tool_declarations(ROOT / "artifacts" / "tools.yaml")),
            model=getattr(provider, "default_model", None),
        )
        result = agent.run(st.session_state.messages)
        answer = result.text or "\n".join(
            f"**{event['tool']}**\n```json\n{event['result']}\n```" for event in result.tool_results
        ) or "Mình chưa nhận được kết quả từ provider."
    except Exception as exc:
        answer = f"Không thể chạy agent ({type(exc).__name__}): {exc}"
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
