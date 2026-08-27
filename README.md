# Buddy AI Assistant

Buddy AI Assistant is a local AI-powered desktop assistant built using Python, Llama 3.2, Ollama, Streamlit, voice recognition, and Windows automation tools.

The assistant can understand natural-language commands, convert them into structured actions, and safely execute approved operations on a Windows laptop.

## Features

- Local Llama 3.2 inference using Ollama
- Voice-based interaction
- Typed chat interaction
- Wake phrase: "Hey Buddy"
- Text-to-speech responses
- Natural-language command understanding
- Structured JSON-based intent generation
- Multi-step command execution
- Desktop application control
- Google search and website opening
- Chrome launch using a configured Chrome profile
- Keyboard automation
- Generated-content typing into Notepad
- Screenshot capture
- Screenshots stored locally inside the `botscreenshot/` folder
- Camera launch and photo capture
- Volume control
- Battery status
- CPU and RAM monitoring
- System information
- Short-term conversation context
- Streamlit-based user interface
- Start and Stop voice controls
- Live assistant status
- Conversation history
- Animated voice-assistant waveform

## Supported Commands

Examples:

- "Hey Buddy"
- "Open Notepad"
- "Open Calculator"
- "Open Camera"
- "Open Task Manager"
- "Open Chrome"
- "Open Downloads"
- "Open Documents"
- "Search Google for AWS Bedrock"
- "Open Chrome and search for AWS Bedrock documentation"
- "Open youtube.com"
- "Open Notepad and type Hello Buddy"
- "Open Notepad and write 3 lines about artificial intelligence"
- "Calculate 6 plus 5"
- "Increase the volume"
- "Decrease the volume"
- "Mute the laptop"
- "Take a screenshot"
- "Take a picture"
- "Open camera and take a picture"
- "What is my battery percentage?"
- "What is my CPU usage?"
- "How much RAM am I using?"
- "Show my system information"
- "Close Notepad"
- "Close Calculator"
- "Close Chrome"

## Architecture

```text
User Voice / Typed Input
        ↓
Speech Recognition / Streamlit Chat
        ↓
Llama 3.2 through Ollama
        ↓
Structured JSON Intent
        ↓
Python Intent Executor
        ↓
Allowlisted Tools
        ↓
Windows Desktop Actions
        ↓
Response Generation
        ↓
Text-to-Speech / Streamlit Conversation UI
```

## Technology Stack

- Python 3.11
- Llama 3.2
- Ollama
- Streamlit
- SpeechRecognition
- PyAudio
- pyttsx3
- PyAutoGUI
- psutil
- Requests
- HTML / CSS
- Python Threading

## Project Structure

```text
buddy-ai-desktop-assistant/
│
├── tools/
│   ├── __init__.py
│   └── app_tools.py
│
├── botscreenshot/
│
├── assistant_service.py
├── intent_parser.py
├── main.py
├── speech_output.py
├── ui.py
├── voice_input.py
├── requirements.txt
├── .gitignore
└── README.md
```

> The `botscreenshot/` folder is created automatically when Buddy captures a desktop screenshot and is ignored by Git.

## How It Works

Buddy uses Llama 3.2 as the natural-language understanding and intent-generation layer.

For example:

User:

```text
Open Notepad and type Hello Buddy
```

Llama converts the request into structured JSON:

```json
{
  "type": "command",
  "steps": [
    {
      "action": "open_app",
      "application": "notepad"
    },
    {
      "action": "type_text",
      "text": "Hello Buddy"
    }
  ]
}
```

The Python execution layer validates the returned action and calls only approved functions.

The LLM does not directly execute arbitrary operating-system commands.

## Generated Content Example

Buddy can also generate fresh content and type it into an application.

Example:

```text
Open Notepad and write 2 lines about apples
```

The generated intent can look like:

```json
{
  "type": "command",
  "steps": [
    {
      "action": "open_app",
      "application": "notepad"
    },
    {
      "action": "type_text",
      "text": "Apples are nutritious fruits rich in vitamins, fiber, and antioxidants.\nThey are enjoyed worldwide as a healthy and refreshing snack."
    }
  ]
}
```

## Camera Behavior

Opening the camera and taking a picture are handled as separate actions.

Example:

```text
Open camera
```

returns:

```json
{
  "type": "command",
  "steps": [
    {
      "action": "open_app",
      "application": "camera"
    }
  ]
}
```

Example:

```text
Open camera and take a picture
```

returns:

```json
{
  "type": "command",
  "steps": [
    {
      "action": "open_app",
      "application": "camera"
    },
    {
      "action": "take_picture"
    }
  ]
}
```

This prevents Buddy from taking a picture unless the user explicitly asks for it.

## Chrome Profile Support

Buddy can launch Chrome using a configured Chrome profile instead of opening the Chrome profile-selection screen.

The Chrome profile directory is configured inside:

```text
tools/app_tools.py
```

To find the correct profile directory:

1. Open the required Chrome profile manually.
2. Open:

```text
chrome://version
```

3. Find **Profile Path**.
4. Use the final folder name such as:

```text
Default
```

or:

```text
Profile 2
```

inside the Chrome configuration in `app_tools.py`.

## Screenshot Storage

Desktop screenshots are stored locally inside:

```text
botscreenshot/
```

Example:

```text
botscreenshot/
└── screenshot_1787742731.png
```

The folder is ignored by Git so personal screenshots are not uploaded to the repository.

## Safety Design

The project uses an allowlisted tool-execution architecture.

Instead of directly executing commands generated by the LLM:

```text
User Request
↓
Llama Intent
↓
Structured JSON
↓
Action Validation
↓
Approved Python Tool
↓
Windows Action
```

This reduces the risk of unintended operating-system commands.

The intent parser is also instructed to use only supported actions and avoid inventing new tool names.

## Voice Mode

Start voice mode from the Streamlit UI.

Then say:

```text
Hey Buddy
```

Buddy enters active listening mode.

To return to standby, say:

```text
Go to sleep
```

## Typed Chat Mode

Voice mode is optional.

You can type a message directly in the Streamlit UI without saying the wake phrase.

Example:

```text
Open calculator
```

or:

```text
What is my CPU usage?
```

Typed requests use the same Llama intent and tool-execution pipeline as voice commands.

## Installation

Clone the repository:

```bash
git clone https://github.com/v1i1n1/buddy-ai-desktop-assistant.git
cd buddy-ai-desktop-assistant
```

Create a virtual environment:

```bash
python -m venv venv
```

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Install Ollama

Install Ollama separately on your system.

Pull Llama 3.2:

```bash
ollama pull llama3.2
```

Verify the model:

```bash
ollama list
```

You can also verify that Ollama is running with:

```bash
ollama ps
```

## Run the Application

Start the Streamlit interface:

```bash
streamlit run ui.py
```

Then use either:

```text
START VOICE
```

for voice interaction,

or type a command directly in the chat input.

## Local vs Internet-Dependent Components

Currently:

```text
Llama 3.2 inference     → Local
Ollama                  → Local
Python desktop tools    → Local
Text-to-speech          → Local
Streamlit UI            → Local
Speech-to-text          → Uses Google Speech Recognition
Google search/websites  → Requires internet
```

Because the current speech recognition uses Google's recognition service, the project should be described as a **local Llama-powered desktop assistant**, rather than a fully offline assistant.

## Current Limitations

- Llama inference performance depends on local hardware.
- CPU-only Llama inference may take longer for complex prompts.
- Current speech recognition uses Google's speech recognition service and requires internet connectivity.
- Desktop automation is currently designed for Windows.
- Chrome behavior depends on the locally configured Chrome profile.
- Camera photo capture depends on the Windows Camera application's keyboard behavior.
- PyAutoGUI actions depend on the correct application having focus.
- Closing Chrome currently closes Chrome processes rather than an individual tab.
- The animated waveform represents assistant state and is not driven by actual microphone amplitude.

## Future Enhancements

- Local speech-to-text using Faster Whisper
- Real-time microphone waveform
- Persistent conversational memory
- LangGraph-based agent orchestration
- Additional desktop tools
- File search and document operations
- Application-specific automation
- Configurable wake word
- Improved window focus handling
- Confirmation prompts for sensitive actions
- Better Chrome tab-level control

## Disclaimer

This project is intended for learning, experimentation, and local desktop automation.

Use system-control functionality carefully and only on devices you own or are authorized to control.