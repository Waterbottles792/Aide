# Aide

> **An AI mentor for cybersecurity learning that teaches instead of spoiling.**

Aide is a GenAI-powered cybersecurity mentor designed for learners using platforms like **TryHackMe**, **Hack The Box**, **PortSwigger Web Security Academy**, and Capture The Flag (CTF) challenges.

Unlike traditional AI assistants that immediately reveal solutions, Aide provides **progressive hints**, contextual explanations, and guided assistance to help users understand concepts and solve challenges independently.

---

## Features

* Progressive, anti-spoiler hint system
* Multiple AI provider support
* Bring your own API keys
* Context-aware conversations
* Chat history and session management
* DuckDuckGo-powered educational search
* Modern terminal interface
* Premium web interface (in development)

---

## Supported AI Providers

* OpenAI
* Anthropic Claude
* Google Gemini
* Groq
* OpenRouter
* Ollama *(planned)*

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Waterbottles792/Aide.git
cd Aide
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

If you're using the web interface:

```bash
cd web/cybersecurity-mentor-interface
npm install
```

---

## Usage

Configure your preferred AI provider and room settings:

```bash
python3 -m aide.cli --setup
```

Launch Aide:

```bash
python3 -m aide.cli
```

---

## Philosophy

Aide follows one simple principle:

> **Teach. Don't Spoil.**

Instead of revealing solutions immediately, Aide adapts to the learner's progress by providing increasingly detailed hints only when necessary, encouraging critical thinking and long-term skill development.

---

## Disclaimer

Aide is intended for educational purposes only.

Use it only on systems and platforms where you have explicit authorization, including:

* TryHackMe
* Hack The Box
* PortSwigger Web Security Academy
* Capture The Flag (CTF) competitions
* Personal laboratories

Always follow responsible disclosure practices and applicable laws.

---

## Contributing

Contributions, feature requests, and bug reports are welcome.

If you'd like to improve Aide, feel free to open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License.
