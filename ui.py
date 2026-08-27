import html
import time
import streamlit as st

from assistant_service import BuddyAssistant


st.set_page_config(
    page_title="Buddy AI Assistant",
    page_icon="🤖",
    layout="centered"
)


# =========================================================
# CSS
# =========================================================

st.html(
    """
    <style>

    html,
    body,
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(
                circle at top,
                #172554 0%,
                #0f172a 45%,
                #020617 100%
            );

        color: white;
    }


    [data-testid="stAppViewContainer"] {
        min-height: 100vh;
    }


    header[data-testid="stHeader"] {
        background: #0f172a !important;
        color: white !important;
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


    .block-container {
        padding-top: 4.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 900px;
    }


    .buddy-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        color: white;
        margin-bottom: 15px;
    }


    .mic-wrapper {
        display: flex;
        justify-content: center;
        margin-top: 20px;
        margin-bottom: 12px;
    }


    .mic-circle {
        width: 105px;
        height: 105px;
        border-radius: 50%;
        border: 3px solid #22d3ee;

        background:
            rgba(
                34,
                211,
                238,
                0.08
            );

        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 45px;

        box-shadow:
            0 0 25px
            rgba(
                34,
                211,
                238,
                0.30
            );
    }


    .mic-active {
        animation: pulse 1.5s infinite;
    }


    @keyframes pulse {

        0% {
            box-shadow:
                0 0 0 0
                rgba(
                    34,
                    211,
                    238,
                    0.50
                );
        }

        70% {
            box-shadow:
                0 0 0 25px
                rgba(
                    34,
                    211,
                    238,
                    0
                );
        }

        100% {
            box-shadow:
                0 0 0 0
                rgba(
                    34,
                    211,
                    238,
                    0
                );
        }
    }


    .status-text {
        text-align: center;
        color: #bae6fd;
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 15px;
    }


    .wave {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 50px;
        gap: 5px;
        margin-bottom: 15px;
    }


    .wave span {
        width: 5px;
        height: 10px;
        background: #22d3ee;
        border-radius: 10px;

        animation:
            wave-animation
            1s
            infinite
            ease-in-out;
    }


    .wave span:nth-child(2) {
        animation-delay: 0.1s;
    }

    .wave span:nth-child(3) {
        animation-delay: 0.2s;
    }

    .wave span:nth-child(4) {
        animation-delay: 0.3s;
    }

    .wave span:nth-child(5) {
        animation-delay: 0.4s;
    }

    .wave span:nth-child(6) {
        animation-delay: 0.5s;
    }

    .wave span:nth-child(7) {
        animation-delay: 0.6s;
    }

    .wave span:nth-child(8) {
        animation-delay: 0.7s;
    }


    @keyframes wave-animation {

        0%,
        100% {
            height: 10px;
        }

        50% {
            height: 42px;
        }
    }


    .section-title {
        color: white;
        font-size: 22px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
    }


    .mode-note {
        text-align: center;
        color: #94a3b8;
        font-size: 13px;
        margin-top: 8px;
        margin-bottom: 22px;
    }


    .chat-card {
        padding: 14px 16px;
        border-radius: 14px;
        margin-bottom: 12px;
        color: white;
        line-height: 1.5;
    }


    .user-card {
        background: #172033;

        border:
            1px solid
            rgba(
                148,
                163,
                184,
                0.18
            );
    }


    .assistant-card {
        background: #0f2942;

        border:
            1px solid
            rgba(
                34,
                211,
                238,
                0.20
            );
    }


    .chat-role {
        font-weight: 700;
        margin-bottom: 6px;
        color: white;
    }


    .chat-text {
        color: #f8fafc;
        font-size: 15px;
        white-space: pre-wrap;
    }


    .footer {
        margin-top: 30px;
        text-align: center;
        color: #94a3b8;
        font-size: 13px;
    }


    /* =====================================================
       TEXT INPUT
       ===================================================== */

    div[data-testid="stTextInput"] input {
        background: #0f172a !important;
        color: white !important;

        border:
            1px solid
            #334155 !important;

        border-radius:
            12px !important;

        height:
            48px !important;
    }


    div[data-testid="stTextInput"] input:focus {
        border:
            1px solid
            #22d3ee !important;

        box-shadow:
            0 0 0 1px
            #22d3ee !important;
    }


    div[data-testid="stTextInput"] input::placeholder {
        color: #64748b !important;
    }


    /* =====================================================
       ALL NORMAL BUTTONS
       START / STOP / CLEAR
       ===================================================== */

    div.stButton > button {
        border-radius: 12px !important;

        font-weight: 700 !important;

        min-height: 46px !important;

        background: #0f172a !important;

        color: #f8fafc !important;

        border:
            1px solid
            #334155 !important;

        transition:
            all
            0.25s
            ease !important;
    }


    div.stButton > button:hover {
        background: #164e63 !important;

        color: #ffffff !important;

        border:
            1px solid
            #22d3ee !important;

        box-shadow:
            0 0 14px
            rgba(
                34,
                211,
                238,
                0.30
            ) !important;

        transform:
            translateY(-1px);
    }


    div.stButton > button:active {
        background: #0e7490 !important;

        color: #ffffff !important;

        border:
            1px solid
            #67e8f9 !important;

        transform:
            translateY(0px);
    }


    div.stButton > button:focus {
        background: #0f172a !important;

        color: #ffffff !important;

        border:
            1px solid
            #22d3ee !important;

        box-shadow:
            0 0 0 2px
            rgba(
                34,
                211,
                238,
                0.20
            ) !important;
    }


    /* =====================================================
       SEND BUTTON INSIDE FORM
       ===================================================== */

    div[data-testid="stForm"] button {
        background: #0891b2 !important;

        color: #ffffff !important;

        border:
            1px solid
            #22d3ee !important;

        border-radius:
            12px !important;

        font-weight:
            700 !important;

        min-height:
            48px !important;

        transition:
            all
            0.25s
            ease !important;
    }


    div[data-testid="stForm"] button:hover {
        background: #0e7490 !important;

        color: #ffffff !important;

        border:
            1px solid
            #67e8f9 !important;

        box-shadow:
            0 0 14px
            rgba(
                34,
                211,
                238,
                0.30
            ) !important;

        transform:
            translateY(-1px);
    }


    div[data-testid="stForm"] button:active {
        background: #155e75 !important;

        color: #ffffff !important;

        border:
            1px solid
            #67e8f9 !important;

        transform:
            translateY(0px);
    }


    div[data-testid="stForm"] button:focus {
        background: #0891b2 !important;

        color: #ffffff !important;

        border:
            1px solid
            #67e8f9 !important;

        box-shadow:
            0 0 0 2px
            rgba(
                34,
                211,
                238,
                0.20
            ) !important;
    }


    </style>
    """
)


# =========================================================
# SESSION STATE
# =========================================================

if "assistant" not in st.session_state:
    st.session_state.assistant = BuddyAssistant()


assistant = st.session_state.assistant


if not hasattr(
    assistant,
    "status"
):
    assistant.status = "Stopped"


if not hasattr(
    assistant,
    "messages"
):
    assistant.messages = []


if not hasattr(
    assistant,
    "running"
):
    assistant.running = False


# =========================================================
# TITLE
# =========================================================

st.html(
    """
    <div class="buddy-title">
        🤖 Buddy AI Assistant
    </div>
    """
)


# =========================================================
# MICROPHONE + STATUS
# =========================================================

status = assistant.status


active_statuses = [
    "Waiting for wake word",
    "Listening",
    "Thinking",
    "Executing"
]


if status in active_statuses:
    mic_class = "mic-circle mic-active"
else:
    mic_class = "mic-circle"


st.html(
    f"""
    <div class="mic-wrapper">

        <div class="{mic_class}">
            🎙️
        </div>

    </div>

    <div class="status-text">
        {html.escape(status)}
    </div>
    """
)


# =========================================================
# WAVEFORM
# =========================================================

if assistant.running:

    st.html(
        """
        <div class="wave">

            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>

        </div>
        """
    )

else:

    st.html(
        """
        <div
            style="
                text-align:center;
                color:#64748b;
                margin-bottom:20px;
            "
        >
            Voice assistant is stopped
        </div>
        """
    )


# =========================================================
# VOICE BUTTONS
# =========================================================

start_col, stop_col = st.columns(2)


with start_col:

    if st.button(
        "🎙️ START VOICE",
        use_container_width=True
    ):

        assistant.start()

        time.sleep(0.2)

        st.rerun()


with stop_col:

    if st.button(
        "⏹ STOP VOICE",
        use_container_width=True
    ):

        assistant.stop()

        st.rerun()


st.html(
    """
    <div class="mode-note">

        Voice mode is optional.
        You can type commands below even when voice is stopped.

    </div>
    """
)


# =========================================================
# TEXT CHAT SECTION
# =========================================================

st.html(
    """
    <div class="section-title">
        💬 Chat with Buddy
    </div>
    """
)


with st.form(
    "buddy_chat_form",
    clear_on_submit=True
):

    text_col, send_col = st.columns(
        [5, 1]
    )


    with text_col:

        typed_message = st.text_input(
            "Message",
            placeholder="Type a message or command...",
            label_visibility="collapsed"
        )


    with send_col:

        send_clicked = st.form_submit_button(
            "Send",
            use_container_width=True
        )


if send_clicked:

    clean_message = (
        typed_message.strip()
        if typed_message
        else ""
    )


    if clean_message:

        with st.spinner(
            "Buddy is thinking..."
        ):

            assistant.process_text_request(
                clean_message
            )


        st.rerun()


# =========================================================
# SUGGESTED COMMANDS
# =========================================================

st.caption(
    "Try: Open calculator • "
    "What is my CPU usage? • "
    "Search Google for AWS Bedrock"
)


# =========================================================
# CONVERSATION
# =========================================================

st.html(
    """
    <div class="section-title">
        Conversation
    </div>
    """
)


messages = assistant.get_messages()


if not messages:

    st.html(
        """
        <div
            style="
                text-align:center;
                color:#64748b;
                padding:25px;
                border:1px dashed #334155;
                border-radius:14px;
            "
        >

            No conversation yet.

            <br><br>

            Type a message below or start
            voice mode and say
            <b>Hey Buddy</b>.

        </div>
        """
    )


else:

    for message in messages:

        role = message.get(
            "role",
            ""
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

            st.html(
                f"""
                <div
                    class="
                        chat-card
                        user-card
                    "
                >

                    <div class="chat-role">
                        👤 You
                    </div>

                    <div class="chat-text">
                        {content}
                    </div>

                </div>
                """
            )


        else:

            st.html(
                f"""
                <div
                    class="
                        chat-card
                        assistant-card
                    "
                >

                    <div class="chat-role">
                        🤖 Buddy
                    </div>

                    <div class="chat-text">
                        {content}
                    </div>

                </div>
                """
            )


# =========================================================
# CLEAR CHAT
# =========================================================

st.write("")


if st.button(
    "🗑 Clear Conversation",
    use_container_width=True
):

    assistant.clear_chat()

    st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.html(
    """
    <div class="footer">

        🎙 Voice:
        Say "Hey Buddy" to activate
        •
        Say "Go to sleep" to return to standby

        <br>

        ⌨ Type:
        Enter a message and click Send

    </div>
    """
)


# =========================================================
# AUTO REFRESH WHILE VOICE IS RUNNING
# =========================================================

if assistant.running:

    time.sleep(0.7)

    st.rerun()