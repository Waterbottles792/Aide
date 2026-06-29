import argparse
import asyncio
import json
import re
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.markup import escape as markup_escape
from rich.panel import Panel
from rich.prompt import Prompt

from textual import on
from textual.app import App, ComposeResult, Screen
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Button, Input, Static

from .provider_client import ProviderClient
from .search import fetch_room_context

console = Console()

DEFAULT_CONFIG_PATH = Path.home() / ".aide" / "config.json"

PROVIDERS = [
    ("openai", "OpenAI"),
    ("groq", "Groq"),
    ("claude", "Claude"),
    ("gemini", "Gemini"),
]

PLATFORMS = [
    ("tryhackme", "TryHackMe"),
    ("hackthebox", "Hack The Box"),
    ("portswigger", "PortSwigger"),
]

MODES = [
    ("general", "General"),
    ("ctf", "CTF Walkthrough"),
    ("web", "Web Security"),
    ("network", "Network Security"),
    ("scripting", "Scripting Help"),
]

MODE_INSTRUCTIONS = {
    "general":   "Focus on foundational concepts and general cybersecurity principles.",
    "ctf":       "Focus on methodology, enumeration, and common pitfalls in CTF challenges. Do not reveal the flag.",
    "web":       "Emphasize web application architecture, HTTP mechanics, and OWASP top 10 vulnerabilities.",
    "network":   "Focus on network protocols, traffic analysis, routing, and network defense strategies.",
    "scripting": "Help the user build secure and effective scripts. Focus on Python, Bash, or PowerShell best practices for security.",
}

AIDE_ASCII = """\
 ░█████╗░██╗██████╗░███████╗
 ██╔══██╗██║██╔══██╗██╔════╝
 ███████║██║██║  ██║█████╗  
 ██╔══██║██║██║  ██║██╔══╝  
 ██║  ██║██║██████╔╝███████╗
 ╚═╝  ╚═╝╚═╝╚═════╝ ╚══════╝"""

MIN_LOADING_SECONDS = 2.0
MAX_RESPONSE_CHARS = 480
MAX_WALKTHROUGH_CHARS = 4000

FLAG_PATTERNS = (
    r"THM\{[^}]+\}",
    r"HTB\{[^}]+\}",
    r"flag\{[^}]+\}",
    r"picoCTF\{[^}]+\}",
    r"CTF\{[^}]+\}",
    r"cyber\{[^}]+\}",
)

LOADING_CSS = """
LoadingScreen {
    background: #000000;
    align: center middle;
}

#loading-wrap {
    width: 72;
    height: auto;
    layout: vertical;
    align: center middle;
}

#loading-logo {
    color: #ffffff;
    text-align: center;
    width: 100%;
}

#loading-msg {
    color: #d4d4d4;
    text-align: center;
    width: 100%;
    margin-top: 2;
}

#loading-sub {
    color: #737373;
    text-align: center;
    width: 100%;
    margin-top: 1;
}

#loading-spinner {
    color: #ffffff;
    text-align: center;
    width: 100%;
    margin-top: 2;
}

#loading-bar {
    color: #525252;
    text-align: center;
    width: 100%;
    margin-top: 1;
}

#loading-status {
    color: #525252;
    text-align: center;
    width: 100%;
    margin-top: 1;
}
"""

CSS = """
MainScreen {
    background: #000000;
    layout: vertical;
}

#header {
    background: #000000;
    border-bottom: solid #262626;
    height: 3;
    padding: 0 1;
}

#header-info {
    width: 1fr;
    content-align: left middle;
    color: #a3a3a3;
    padding: 0 1;
}

#btn-walkthrough {
    background: #000000;
    color: #ffffff;
    border: solid #404040;
    min-width: 24;
    height: 3;
    margin: 0 1;
}

#btn-walkthrough:hover {
    background: #171717;
    border: solid #737373;
}

#btn-walkthrough.-disabled {
    opacity: 0.4;
}

#chat-scroll {
    background: #000000;
    border: solid #262626;
    margin: 0 1;
    padding: 1 2;
    height: 1fr;
}

.msg-user {
    color: #ffffff;
    margin-bottom: 1;
}

.msg-bot {
    color: #a3a3a3;
    margin-bottom: 1;
}

.msg-err {
    color: #fca5a5;
    margin-bottom: 1;
}

.msg-dim {
    color: #525252;
    margin-bottom: 1;
}

.msg-sys {
    color: #737373;
    margin-bottom: 1;
}

.msg-walkthrough {
    color: #d4d4d4;
    margin-bottom: 1;
}

#input-bar {
    background: #000000;
    border-top: solid #262626;
    padding: 0 1;
    height: 3;
}

#chat-input {
    background: #000000;
    border: none;
    color: #ffffff;
    width: 1fr;
    padding: 0 1;
}

#chat-input:focus {
    border: none;
}
"""


# ──────────────────────────────────────────────────────────────────────────────
# Config helpers
# ──────────────────────────────────────────────────────────────────────────────

def ensure_config_dir(path: Optional[Path] = None) -> Path:
    p = path or DEFAULT_CONFIG_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def save_config(data: dict, path: Optional[Path] = None) -> None:
    ensure_config_dir(path).write_text(json.dumps(data, indent=2))

def load_config(path: Optional[Path] = None) -> dict:
    p = path or DEFAULT_CONFIG_PATH
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text())
    except Exception:
        return {}

def _default_model(provider: str) -> str:
    return {"openai": "gpt-4o-mini", "groq": "llama-3.1-8b-instant",
            "claude": "claude-3-5-sonnet-latest", "gemini": "gemini-2.0-flash"}.get(provider, "gpt-4o-mini")

def _default_url(provider: str) -> str:
    return {"openai": "https://api.openai.com/v1/chat/completions",
            "groq": "https://api.groq.com/openai/v1/chat/completions",
            "claude": "https://api.anthropic.com/v1/messages",
            "gemini": "https://generativelanguage.googleapis.com/v1beta/models"}.get(provider, "")

def _prompt_choice(label: str, choices: list[tuple[str, str]]) -> str:
    console.print(f"\n[bold cyan]{label}[/bold cyan]")
    for i, (_, name) in enumerate(choices, 1):
        console.print(f"  [bold green]{i}.[/bold green] {name}")
    while True:
        raw = Prompt.ask("Select number", default="1")
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(choices):
                return choices[idx][0]
        console.print("[bold red]Invalid — try again.[/bold red]")


# ──────────────────────────────────────────────────────────────────────────────
# Setup flow (rich)
# ──────────────────────────────────────────────────────────────────────────────

def run_setup(config_path: Optional[Path] = None) -> dict:
    console.print(Panel(AIDE_ASCII, style="bold blue", expand=False))
    console.print(Panel("[bold magenta]  Aide — Session Setup  [/bold magenta]", expand=False))
    provider = _prompt_choice("Choose your LLM provider:", PROVIDERS)
    api_key  = Prompt.ask("[bold cyan]Enter your API key[/bold cyan]", password=True)
    model    = Prompt.ask("[bold cyan]Model name[/bold cyan]", default=_default_model(provider))
    platform = _prompt_choice("Choose your learning platform:", PLATFORMS)
    mode     = _prompt_choice("Choose your learning mode:", MODES)
    while True:
        room = Prompt.ask("[bold cyan]Room / lab name[/bold cyan]").strip()
        if room:
            break
        console.print("[bold red]Room name is required — please enter the room or lab name.[/bold red]")
    config   = {
        "provider": provider, "api_key": api_key, "model": model,
        "platform": platform, "mode": mode, "room": room,
        "base_url": _default_url(provider),
    }
    save_path = config_path or DEFAULT_CONFIG_PATH
    save_config(config, path=save_path)
    console.print(f"\n[bold green]✓ Config saved → {save_path}[/bold green]")
    console.print("[bold cyan]Launching Aide — loading room context…[/bold cyan]\n")
    return config


# ──────────────────────────────────────────────────────────────────────────────
# Textual TUI
# ──────────────────────────────────────────────────────────────────────────────

SPINNER_FRAMES = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
LOADING_STEPS = [
    "Searching DuckDuckGo for writeups…",
    "Fetching walkthrough pages…",
    "Extracting room context…",
    "Preparing your mentor session…",
]


def _build_chat_prompt(
    platform: str,
    room: str,
    mode: str,
    mode_line: str,
    room_context: str,
    history: list[dict[str, str]],
    user_message: str,
) -> str:
    context_block = ""
    if room_context:
        context_block = (
            f"\n[ROOM CONTEXT — {platform} / {room}]\n"
            f"{room_context}\n[END ROOM CONTEXT]\n"
        )

    history_block = ""
    for item in history[-10:]:
        role = "User" if item["role"] == "user" else "Aide"
        history_block += f"{role}: {item['content']}\n"

    return (
        "You are Aide, a concise cybersecurity mentor.\n"
        f"Platform: {platform}. Room: '{room}'. Mode: {mode}. {mode_line}\n"
        "Rules:\n"
        "- Reply in at most 3 short sentences (under 80 words total).\n"
        "- Give ONE small hint or answer ONLY what the user asked.\n"
        "- Do NOT dump starting tips, numbered lists, or multi-step guides unless explicitly requested.\n"
        "- Do NOT reveal the flag or full solution.\n"
        "- At most one short follow-up question, only if needed.\n"
        "- No markdown headers, no bullet lists, plain conversational text only.\n"
        f"{context_block}\n"
        f"{('Conversation so far:\n' + history_block) if history_block else ''}"
        f"User: {user_message}"
    )


def _trim_response(text: str, limit: int = MAX_RESPONSE_CHARS) -> str:
    cleaned = text.strip()
    if len(cleaned) <= limit:
        return cleaned
    cut = cleaned[:limit].rsplit(" ", 1)[0]
    return cut + "…"


def _build_walkthrough_prompt(
    platform: str,
    room: str,
    mode: str,
    room_context: str,
) -> str:
    context_block = ""
    if room_context:
        context_block = (
            f"\n[ROOM CONTEXT — {platform} / {room}]\n"
            f"{room_context}\n[END ROOM CONTEXT]\n"
        )

    return (
        "You are Aide. The user pressed 'Complete Walkthrough' and wants the full solution.\n"
        f"Platform: {platform}. Room: '{room}'. Mode: {mode}.\n"
        "Provide a complete step-by-step walkthrough from start to finish.\n"
        "Include every task, command, and flag. Use numbered steps.\n"
        "Be thorough and practical — this is an explicit full-spoiler request.\n"
        f"{context_block}"
    )


def _find_flags(text: str) -> set[str]:
    found: set[str] = set()
    for pattern in FLAG_PATTERNS:
        found.update(re.findall(pattern, text, flags=re.IGNORECASE))
    return found


def _expected_flag_count(room_context: str) -> int:
    if not room_context:
        return 1
    return max(len(_find_flags(room_context)), 1)


def _flag_progress_message(found: int, expected: int) -> str:
    return f"flags {found}/{expected}"


def _header_text(room: str, platform: str, found: int, expected: int) -> str:
    return (
        f"[bold white]aide[/bold white]  "
        f"[#737373]·[/]  [white]{markup_escape(room)}[/white]  "
        f"[#737373]·[/]  [#737373]{markup_escape(platform)}[/]  "
        f"[#737373]·[/]  [#525252]{_flag_progress_message(found, expected)}[/]  "
        f"[#737373]·[/]  [#404040]ctrl+q[/]"
    )


def _welcome_message(room: str, context_loaded: bool, source_count: int, expected_flags: int) -> str:
    if context_loaded:
        status = f"{source_count} writeup(s) loaded"
    else:
        status = "no writeups found"
    return (
        f"[#525252]session · {markup_escape(room)} · {status} · "
        f"~{expected_flags} flag(s)[/]\n"
        f"[#404040]ask for hints below, or use Complete Walkthrough for the full solution[/]"
    )


class LoadingScreen(Screen):
    """Full-screen loader shown while writeup context is fetched."""

    CSS = LOADING_CSS

    def __init__(self, config: dict, config_path: Optional[Path] = None):
        super().__init__()
        self.cfg = config
        self.config_path = config_path or DEFAULT_CONFIG_PATH
        self.platform = config.get("platform", "tryhackme")
        self.room = config.get("room", "")
        self.mode = config.get("mode", "general")
        self._frame = 0
        self._step = 0
        self._progress = 0

    def compose(self) -> ComposeResult:
        room = markup_escape(self.room)
        platform = markup_escape(self.platform)
        with Container(id="loading-wrap"):
            yield Static(AIDE_ASCII, id="loading-logo")
            yield Static(
                f"[white]loading[/white]  [#525252]·[/]  "
                f"[white]{room}[/white]  [#525252]·[/]  {platform}",
                id="loading-msg",
            )
            yield Static(
                "[#404040]fetching writeups[/]",
                id="loading-sub",
            )
            yield Static(SPINNER_FRAMES[0], id="loading-spinner")
            yield Static("▱" * 24, id="loading-bar")
            yield Static(LOADING_STEPS[0], id="loading-status")

    async def on_mount(self) -> None:
        self.set_interval(0.12, self._animate)
        started = asyncio.get_running_loop().time()
        context, urls = await fetch_room_context(self.platform, self.room, self.mode)
        elapsed = asyncio.get_running_loop().time() - started
        remaining = MIN_LOADING_SECONDS - elapsed
        if remaining > 0:
            await asyncio.sleep(remaining)
        expected_flags = _expected_flag_count(context)
        self.app.switch_screen(
            MainScreen(self.cfg, context, urls, expected_flags, self.config_path)
        )

    def _animate(self) -> None:
        self._frame = (self._frame + 1) % len(SPINNER_FRAMES)
        self._progress = min(self._progress + 1, 23)
        if self._frame % 8 == 0:
            self._step = min(self._step + 1, len(LOADING_STEPS) - 1)

        filled = "▰" * self._progress + "▱" * (24 - self._progress)
        self.query_one("#loading-spinner", Static).update(SPINNER_FRAMES[self._frame])
        self.query_one("#loading-bar", Static).update(filled)
        self.query_one("#loading-status", Static).update(LOADING_STEPS[self._step])


class MainScreen(Screen):
    CSS = CSS
    BINDINGS = [("ctrl+q", "quit", "Quit")]

    def __init__(
        self,
        config: dict,
        room_context: str,
        source_urls: list[str],
        expected_flags: int = 1,
        config_path: Optional[Path] = None,
    ):
        super().__init__()
        self.cfg = config
        self.config_path = config_path or DEFAULT_CONFIG_PATH
        self.platform = config.get("platform", "Unknown")
        self.room = config.get("room", "Unknown")
        self.mode = config.get("mode", "general")
        self.provider_name = config.get("provider", "Unknown")
        self.model_name = config.get("model", "Unknown")
        self.mode_line = MODE_INSTRUCTIONS.get(self.mode, MODE_INSTRUCTIONS["general"])
        self.room_context = room_context
        self.source_urls = source_urls
        self.expected_flags = expected_flags
        self.flags_found: set[str] = set()
        self.history: list[dict[str, str]] = []
        self.awaiting_room_choice = False
        self.awaiting_room_name = False
        self._busy = False
        self.client = ProviderClient(
            provider=self.provider_name,
            api_key=config.get("api_key", ""),
            model=self.model_name,
            base_url=config.get("base_url"),
        )

    def compose(self) -> ComposeResult:
        welcome = _welcome_message(
            self.room, bool(self.room_context), len(self.source_urls), self.expected_flags,
        )
        with Horizontal(id="header"):
            yield Static(
                _header_text(self.room, self.platform, 0, self.expected_flags),
                id="header-info",
            )
            yield Button("Complete Walkthrough", id="btn-walkthrough", variant="default")
        with VerticalScroll(id="chat-scroll"):
            yield Static(welcome, classes="msg-sys")
        with Horizontal(id="input-bar"):
            yield Input(
                placeholder="message aide…",
                id="chat-input",
            )

    async def on_mount(self) -> None:
        self.query_one("#chat-input", Input).focus()
        self.query_one("#chat-scroll", VerticalScroll).scroll_end(animate=False)

    def _append_chat(self, content: str, classes: str) -> None:
        scroll = self.query_one("#chat-scroll", VerticalScroll)
        scroll.mount(Static(content, classes=classes))
        scroll.scroll_end(animate=False)

    def _update_header(self) -> None:
        self.query_one("#header-info", Static).update(
            _header_text(
                self.room, self.platform,
                len(self.flags_found), self.expected_flags,
            )
        )

    def _set_busy(self, busy: bool) -> None:
        self._busy = busy
        btn = self.query_one("#btn-walkthrough", Button)
        btn.disabled = busy
        chat_input = self.query_one("#chat-input", Input)
        chat_input.disabled = busy

    def _register_flags(self, text: str) -> bool:
        new_flags = _find_flags(text) - self.flags_found
        if not new_flags:
            return False
        self.flags_found.update(new_flags)
        self._update_header()
        names = ", ".join(sorted(new_flags))
        self._append_chat(
            f"[#525252]flag recorded ·[/] [white]{markup_escape(names)}[/white]",
            "msg-sys",
        )
        return True

    def _on_all_flags_found(self) -> None:
        self.awaiting_room_choice = True
        self.awaiting_room_name = False
        self._append_chat(
            "[white]room complete — all flags found[/white]\n"
            "[#525252]type[/] [white]new room[/white] [#525252]or[/] [white]exit[/white]",
            "msg-sys",
        )

    async def _start_new_room(self, room_name: str) -> None:
        self.cfg["room"] = room_name
        save_config(self.cfg, path=self.config_path)
        self.room = room_name
        self.awaiting_room_choice = False
        self.awaiting_room_name = False
        self.app.switch_screen(LoadingScreen(self.cfg, self.config_path))

    @on(Button.Pressed, "#btn-walkthrough")
    async def handle_walkthrough(self) -> None:
        if self._busy or self.awaiting_room_choice:
            return

        self._set_busy(True)
        self._append_chat("[#525252]generating complete walkthrough…[/]", "msg-dim")

        loading = Static("[#404040]…[/]", classes="msg-dim")
        scroll = self.query_one("#chat-scroll", VerticalScroll)
        scroll.mount(loading)
        scroll.scroll_end(animate=False)

        prompt = _build_walkthrough_prompt(
            self.platform, self.room, self.mode, self.room_context,
        )

        try:
            response = _trim_response(
                await self.client.ask(prompt, max_tokens=1800),
                limit=MAX_WALKTHROUGH_CHARS,
            )
            self._register_flags(response)
            await loading.remove()
            self._append_chat(
                f"[#737373]walkthrough[/]\n\n{markup_escape(response)}",
                "msg-walkthrough",
            )
            if len(self.flags_found) >= self.expected_flags and not self.awaiting_room_choice:
                self._on_all_flags_found()
        except Exception as exc:
            await loading.remove()
            self._append_chat(
                f"[#fca5a5]error · {markup_escape(str(exc))}[/]",
                "msg-err",
            )
        finally:
            self._set_busy(False)

    @on(Input.Submitted, "#chat-input")
    async def handle_input(self, event: Input.Submitted) -> None:
        if self._busy:
            return

        text = event.value.strip()
        if not text:
            return

        self.query_one("#chat-input", Input).value = ""
        lowered = text.lower()

        if lowered in {"exit", "quit"}:
            self.app.exit()
            return

        if self.awaiting_room_name:
            if not text.strip():
                self._append_chat("[#525252]room name required[/]", "msg-sys")
                return
            self._append_chat(
                f"[#525252]loading ·[/] [white]{markup_escape(text)}[/white]",
                "msg-sys",
            )
            await self._start_new_room(text.strip())
            return

        if self.awaiting_room_choice:
            if lowered in {"new room", "new", "next", "another"}:
                self.awaiting_room_name = True
                self._append_chat("[#525252]new room name?[/]", "msg-sys")
                return
            self._append_chat(
                "[#525252]type[/] [white]new room[/white] [#525252]or[/] [white]exit[/white]",
                "msg-sys",
            )
            return

        manual_done = lowered in {
            "done", "finished", "complete", "all flags", "found all flags", "room complete",
        }
        self._register_flags(text)

        if manual_done or len(self.flags_found) >= self.expected_flags:
            if not self.awaiting_room_choice:
                self._on_all_flags_found()
            return

        self.history.append({"role": "user", "content": text})
        self._append_chat(f"[white]you ›[/]  {markup_escape(text)}", "msg-user")

        self._set_busy(True)
        loading = Static("[#404040]…[/]", classes="msg-dim")
        scroll = self.query_one("#chat-scroll", VerticalScroll)
        scroll.mount(loading)
        scroll.scroll_end(animate=False)

        prompt = _build_chat_prompt(
            self.platform, self.room, self.mode, self.mode_line,
            self.room_context, self.history[:-1], text,
        )

        try:
            response = _trim_response(await self.client.ask(prompt))
            self.history.append({"role": "assistant", "content": response})
            await loading.remove()
            self._append_chat(
                f"[#737373]aide ‹[/]  {markup_escape(response)}",
                "msg-bot",
            )
            if len(self.flags_found) >= self.expected_flags and not self.awaiting_room_choice:
                self._on_all_flags_found()
        except Exception as exc:
            await loading.remove()
            self._append_chat(
                f"[#fca5a5]error · {markup_escape(str(exc))}[/]",
                "msg-err",
            )
        finally:
            self._set_busy(False)


class AideApp(App):
    CSS = LOADING_CSS + CSS
    BINDINGS = [("ctrl+q", "quit", "Quit")]

    def __init__(self, config: dict, config_path: Optional[Path] = None):
        super().__init__()
        self.config = config
        self.config_path = config_path or DEFAULT_CONFIG_PATH

    def on_mount(self) -> None:
        self.push_screen(LoadingScreen(self.config, self.config_path))


# ──────────────────────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(prog="aide")
    parser.add_argument("--config", type=str, default=str(DEFAULT_CONFIG_PATH))
    args = parser.parse_args()

    config_path = Path(args.config).expanduser()
    config = run_setup(config_path=config_path)
    AideApp(config, config_path=config_path).run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
