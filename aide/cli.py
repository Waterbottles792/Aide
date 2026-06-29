import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Optional

from .provider_client import ProviderClient

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


def ensure_config_dir(path: Optional[Path] = None) -> Path:
    config_path = path or DEFAULT_CONFIG_PATH
    config_path.parent.mkdir(parents=True, exist_ok=True)
    return config_path


def save_config(data: dict, path: Optional[Path] = None) -> Path:
    config_path = ensure_config_dir(path)
    config_path.write_text(json.dumps(data, indent=2))
    return config_path


def load_config(path: Optional[Path] = None) -> dict:
    config_path = path or DEFAULT_CONFIG_PATH
    if not config_path.exists():
        return {}
    try:
        return json.loads(config_path.read_text())
    except Exception:
        return {}


def prompt_choice(prompt: str, choices: list[tuple[str, str]]) -> str:
    print(prompt)
    for idx, (_, label) in enumerate(choices, 1):
        print(f"  {idx}. {label}")
    while True:
        raw = input("Select number: ").strip()
        if raw.isdigit():
            choice_index = int(raw) - 1
            if 0 <= choice_index < len(choices):
                return choices[choice_index][0]
        print("Please enter a valid number.")


def prompt_text(prompt: str, default: Optional[str] = None) -> str:
    if default:
        response = input(f"{prompt} [{default}]: ").strip()
        return response or default
    response = input(f"{prompt}: ").strip()
    return response


def build_provider_model(provider: str) -> str:
    defaults = {
        "openai": "gpt-4o-mini",
        "groq": "llama-3.1-8b-instant",
        "claude": "claude-3-5-sonnet-latest",
        "gemini": "gemini-2.0-flash",
    }
    return defaults.get(provider, "gpt-4o-mini")


def build_provider_base_url(provider: str) -> str:
    defaults = {
        "openai": "https://api.openai.com/v1/chat/completions",
        "groq": "https://api.groq.com/openai/v1/chat/completions",
        "claude": "https://api.anthropic.com/v1/messages",
        "gemini": "https://generativelanguage.googleapis.com/v1beta/models",
    }
    return defaults.get(provider, "")


def run_setup() -> dict:
    print("Aide setup")
    print("=" * 24)
    provider = prompt_choice("Choose your LLM provider:", PROVIDERS)
    api_key = prompt_text("Enter your API key")
    model = prompt_text("Enter the model name", build_provider_model(provider))
    platform = prompt_choice("Choose your learning platform:", PLATFORMS)
    room = prompt_text("Enter the room or lab name")

    config = {
        "provider": provider,
        "api_key": api_key,
        "model": model,
        "platform": platform,
        "room": room,
        "base_url": build_provider_base_url(provider),
    }
    save_config(config)
    print(f"Saved config to {DEFAULT_CONFIG_PATH}")
    return config


def run_chat(config: dict) -> None:
    print("\nAide is ready. Type 'exit' to quit.\n")
    print(f"Platform: {config['platform']} | Room: {config['room']} | Provider: {config['provider']}")
    client = ProviderClient(
        provider=config["provider"],
        api_key=config["api_key"],
        model=config["model"],
        base_url=config.get("base_url"),
    )
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break
        if not user_input:
            continue
        prompt = (
            f"You are Aide, a cybersecurity mentor for {config['platform']} labs. "
            f"The current room is {config['room']}. Give a small hint, not the full solution. "
            f"User request: {user_input}"
        )
        try:
            response = asyncio.run(client.ask(prompt))
            print(f"Aide: {response}")
        except Exception as exc:
            print(f"Aide: request failed: {exc}")


def main() -> int:
    parser = argparse.ArgumentParser(prog="aide")
    parser.add_argument("--config", type=str, default=str(DEFAULT_CONFIG_PATH))
    parser.add_argument("--setup", action="store_true")
    args = parser.parse_args()

    config_path = Path(args.config).expanduser()
    if args.setup or not load_config(path=config_path):
        config = run_setup()
    else:
        config = load_config(path=config_path)
    run_chat(config)
    return 0


if __name__ == "__main__":
    sys.exit(main())
