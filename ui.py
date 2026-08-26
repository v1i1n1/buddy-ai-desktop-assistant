import time
import html
import streamlit as st

from assistant_service import BuddyAssistant


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Buddy AI Assistant",
    page_icon="🤖",
    layout="centered"
)


# =========================================================
# SESSION STATE
# =========================================================

if "assistant" not in st.session_state:
    st.session_state.assistant = BuddyAssistant()


assistant = st.session_state.assistant


if not hasattr(assistant, "status"):
    assistant.status = "Stopped"

if not hasattr(assistant, "messages"):
    assistant.messages = []

if not hasattr(assistant, "running"):
    assistant.running = False


# =========================================================
# CSS
# =========================================================

st.html(
    """
    <style>

    /* =====================================================
       MAIN APP
    ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at top,
                #172554 0%,
                #0f172a 38%,
                #020617 100%
            );

        color: #f8fafc;
    }


    /* =====================================================
       STREAMLIT TOP HEADER
    ===================================================== */

    header[data-testid="stHeader"] {
        background: #0f172a !important;
        color: #ffffff !important;
    }

    div[data-testid="stToolbar"] {
        background: #0f172a !important;
    }

    div[data-testid="stDecoration"] {
        display: none !important;
    }

    [data-testid="stStatusWidget"] {
        visibility: hidden;
    }


    /* =====================================================
       MAIN CONTENT
    ===================================================== */

    .block-container {
        max-width: 820px;

        padding-top: 4.5rem !important;

        padding-bottom: 2rem;
    }


    /* =====================================================
       HEADER
    ===================================================== */

    .buddy-header {
        text-align: center;

        margin-top: 10px;
        margin-bottom: 18px;
    }


    .buddy-title {
        font-size: 40px;

        font-weight: 800;

        color: #ffffff;

        margin: 0;
        padding: 0;

        line-height: 1.3;

        letter-spacing: 0.2px;
    }


    /* =====================================================
       MICROPHONE
    ===================================================== */

    .assistant-circle {
        width: 105px;
        height: 105px;

        margin: 18px auto 12px auto;

        border-radius: 50%;

        display: flex;
        justify-content: center;
        align-items: center;

        font-size: 48px;

        background: #0f172a;

        border: 2px solid #38bdf8;

        box-shadow:
            0 0 20px rgba(56, 189, 248, 0.30);
    }


    .assistant-active {
        animation: pulse-circle 1.5s infinite;
    }


    @keyframes pulse-circle {

        0% {
            box-shadow:
                0 0 12px rgba(56, 189, 248, 0.25);
        }

        50% {
            box-shadow:
                0 0 30px rgba(56, 189, 248, 0.70),
                0 0 55px rgba(56, 189, 248, 0.25);
        }

        100% {
            box-shadow:
                0 0 12px rgba(56, 189, 248, 0.25);
        }
    }


    /* =====================================================
       STATUS
    ===================================================== */

    .status-text {
        text-align: center;

        font-size: 17px;
        font-weight: 700;

        color: #ffffff;

        margin-top: 5px;
    }


    .status-subtext {
        text-align: center;

        color: #94a3b8;

        font-size: 13px;

        margin-top: 3px;
    }


    /* =====================================================
       WAVEFORM
    ===================================================== */

    .wave-wrapper {
        display: flex;

        justify-content: center;
        align-items: center;

        height: 85px;

        gap: 6px;

        margin-bottom: 15px;
    }


    .wave-bar {
        width: 7px;

        border-radius: 10px;

        background: #38bdf8;

        box-shadow:
            0 0 7px rgba(56, 189, 248, 0.7);

        animation:
            audio-wave 0.75s ease-in-out infinite;
    }


    .wave-bar:nth-child(1) {
        height: 18px;
        animation-delay: 0.00s;
    }

    .wave-bar:nth-child(2) {
        height: 30px;
        animation-delay: 0.08s;
    }

    .wave-bar:nth-child(3) {
        height: 45px;
        animation-delay: 0.16s;
    }

    .wave-bar:nth-child(4) {
        height: 60px;
        animation-delay: 0.24s;
    }

    .wave-bar:nth-child(5) {
        height: 48px;
        animation-delay: 0.32s;
    }

    .wave-bar:nth-child(6) {
        height: 35px;
        animation-delay: 0.40s;
    }

    .wave-bar:nth-child(7) {
        height: 27px;
        animation-delay: 0.48s;
    }

    .wave-bar:nth-child(8) {
        height: 19px;
        animation-delay: 0.56s;
    }

    .wave-bar:nth-child(9) {
        height: 13px;
        animation-delay: 0.64s;
    }


    @keyframes audio-wave {

        0% {
            transform: scaleY(0.35);
            opacity: 0.45;
        }

        50% {
            transform: scaleY(1.2);
            opacity: 1;
        }

        100% {
            transform: scaleY(0.35);
            opacity: 0.45;
        }
    }


    .wave-stopped .wave-bar {
        animation: none;

        opacity: 0.2;

        transform: scaleY(0.3);
    }


    .wave-waiting .wave-bar {
        animation-duration: 1.4s;
    }


    .wave-listening .wave-bar {
        animation-duration: 0.5s;
    }


    .wave-thinking .wave-bar {
        animation-duration: 0.9s;
    }


    /* =====================================================
       BUTTONS
    ===================================================== */

    div.stButton > button {
        min-height: 48px;

        border-radius: 12px;

        font-size: 14px;
        font-weight: 700;

        background: #111827;

        border: 1px solid #334155;

        color: #ffffff;
    }


    div.stButton > button:hover {
        border-color: #38bdf8;

        color: #38bdf8;
    }


    div.stButton > button:disabled {
        background: #0b1220;

        border-color: #172033;

        color: #334155;
    }


    /* =====================================================
       DIVIDER
    ===================================================== */

    hr {
        border-color: #1e293b !important;
    }


    /* =====================================================
       CONVERSATION
    ===================================================== */

    .conversation-heading {
        font-size: 22px;

        font-weight: 750;

        color: #ffffff;

        margin-bottom: 14px;
    }


    .chat-area {
        border: 1px solid #1e293b;

        background: rgba(
            2,
            6,
            23,
            0.40
        );

        border-radius: 16px;

        padding: 16px;

        min-height: 250px;

        max-height: 420px;

        overflow-y: auto;
    }


    /* USER MESSAGE */

    .chat-user {
        display: flex;

        align-items: center;

        gap: 10px;

        margin-bottom: 14px;
    }


    .chat-user-icon {
        width: 36px;
        height: 36px;

        flex-shrink: 0;

        border-radius: 10px;

        background: #ef4444;

        display: flex;
        align-items: center;
        justify-content: center;

        color: #ffffff;
    }


    .chat-user-bubble {
        flex: 1;

        background: #172033;

        border: 1px solid #334155;

        border-radius: 13px;

        padding: 11px 14px;

        color: #ffffff;

        font-size: 15px;

        line-height: 1.5;
    }


    /* BUDDY MESSAGE */

    .chat-assistant {
        display: flex;

        align-items: center;

        gap: 10px;

        margin-bottom: 14px;
    }


    .chat-assistant-icon {
        width: 36px;
        height: 36px;

        flex-shrink: 0;

        border-radius: 10px;

        background: #f59e0b;

        display: flex;
        align-items: center;
        justify-content: center;

        color: #ffffff;
    }


    .chat-assistant-bubble {
        flex: 1;

        background: #0f2942;

        border: 1px solid #1e4b6d;

        border-radius: 13px;

        padding: 11px 14px;

        color: #ffffff;

        font-size: 15px;

        line-height: 1.5;
    }


    .empty-chat {
        text-align: center;

        padding: 50px 15px;

        color: #94a3b8;

        font-size: 15px;
    }


    /* =====================================================
       FOOTER
    ===================================================== */

    .footer-text {
        text-align: center;

        margin-top: 15px;

        color: #64748b;

        font-size: 12px;
    }

    </style>
    """
)


# =========================================================
# HEADER
# =========================================================

st.html(
    """
    <div class="buddy-header">
        <div class="buddy-title">
            🤖 Buddy AI Assistant
        </div>
    </div>
    """
)


# =========================================================
# STATUS LOGIC
# =========================================================

status = str(assistant.status)


if status == "Stopped":

    status_message = "Buddy is stopped"

    status_subtext = (
        "Click Start Buddy to activate the assistant."
    )

    wave_class = "wave-stopped"

    mic_class = ""


elif status == "Waiting for wake word":

    status_message = 'Waiting for "Hey Buddy"'

    status_subtext = (
        "Buddy is ready and waiting for you."
    )

    wave_class = "wave-waiting"

    mic_class = "assistant-active"


elif status == "Listening":

    status_message = "Listening..."

    status_subtext = (
        "Speak your command."
    )

    wave_class = "wave-listening"

    mic_class = "assistant-active"


elif status == "Thinking":

    status_message = "Thinking..."

    status_subtext = (
        "Understanding your request."
    )

    wave_class = "wave-thinking"

    mic_class = "assistant-active"


elif status == "Executing":

    status_message = "Executing..."

    status_subtext = (
        "Performing the requested action."
    )

    wave_class = "wave-listening"

    mic_class = "assistant-active"


else:

    status_message = status

    status_subtext = ""

    wave_class = "wave-waiting"

    mic_class = "assistant-active"


# =========================================================
# MICROPHONE
# =========================================================

st.html(
    f"""
    <div class="assistant-circle {mic_class}">
        🎙️
    </div>
    """
)


# =========================================================
# STATUS DISPLAY
# =========================================================

st.html(
    f"""
    <div class="status-text">
        ● {html.escape(status_message)}
    </div>

    <div class="status-subtext">
        {html.escape(status_subtext)}
    </div>
    """
)


# =========================================================
# WAVEFORM
# =========================================================

st.html(
    f"""
    <div class="wave-wrapper {wave_class}">
        <div class="wave-bar"></div>
        <div class="wave-bar"></div>
        <div class="wave-bar"></div>
        <div class="wave-bar"></div>
        <div class="wave-bar"></div>
        <div class="wave-bar"></div>
        <div class="wave-bar"></div>
        <div class="wave-bar"></div>
        <div class="wave-bar"></div>
    </div>
    """
)


# =========================================================
# START / STOP BUTTONS
# =========================================================

col1, col2 = st.columns(2)


with col1:

    if st.button(
        "▶ START BUDDY",
        use_container_width=True,
        disabled=assistant.running
    ):

        assistant.start()

        st.rerun()


with col2:

    if st.button(
        "■ STOP BUDDY",
        use_container_width=True,
        disabled=not assistant.running
    ):

        assistant.stop()

        st.rerun()


# =========================================================
# CONVERSATION
# =========================================================

st.divider()


st.html(
    """
    <div class="conversation-heading">
        💬 Conversation
    </div>
    """
)


chat_content = ""


if not assistant.messages:

    chat_content = """
        <div class="empty-chat">
            Start Buddy and say
            <strong>"Hey Buddy"</strong>
            to begin.
        </div>
    """


else:

    for message in assistant.messages:

        role = message.get(
            "role",
            "assistant"
        )

        content = html.escape(
            str(
                message.get(
                    "content",
                    ""
                )
            )
        )


        if role == "user":

            chat_content += f"""
                <div class="chat-user">

                    <div class="chat-user-icon">
                        👤
                    </div>

                    <div class="chat-user-bubble">
                        {content}
                    </div>

                </div>
            """


        else:

            chat_content += f"""
                <div class="chat-assistant">

                    <div class="chat-assistant-icon">
                        🤖
                    </div>

                    <div class="chat-assistant-bubble">
                        {content}
                    </div>

                </div>
            """


st.html(
    f"""
    <div class="chat-area">
        {chat_content}
    </div>
    """
)


# =========================================================
# CLEAR CHAT
# =========================================================

st.write("")


if st.button(
    "🗑 CLEAR CONVERSATION",
    use_container_width=True
):

    assistant.clear_chat()

    st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.html(
    """
    <div class="footer-text">
        🎙 Say "Hey Buddy" to activate
        &nbsp; • &nbsp;
        Say "Go to sleep" to return to standby
    </div>
    """
)


# =========================================================
# AUTO REFRESH
# =========================================================

if assistant.running:

    time.sleep(
        0.7
    )

    st.rerun()