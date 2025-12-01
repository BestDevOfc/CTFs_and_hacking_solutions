#!/usr/bin/env python3

# python3 autotype.py --file ntp.conf -m type -d 0.002 --stop-key esc
import argparse
import sys
import time
import pyautogui
import pyperclip
import keyboard
from pathlib import Path

def read_text_source(file_path: str | None, text: str | None) -> str:
    """Read text from file or direct input."""
    if file_path:
        path = Path(file_path).expanduser()
        if not path.exists():
            sys.exit(f"Error: file not found: {path}")
        return path.read_text(encoding="utf-8")
    elif text:
        return text
    elif not sys.stdin.isatty():
        return sys.stdin.read()
    else:
        sys.exit("Error: must specify --file, --text, or provide input via stdin.")

def paste_text(text: str):
    """Copy to clipboard and paste (fastest)."""
    prev_clip = pyperclip.paste()
    try:
        pyperclip.copy(text)
        pyautogui.hotkey('command', 'v')
    finally:
        pyperclip.copy(prev_clip)

def type_text(text: str, delay: float, chunk: int, stop_key: str):
    """Simulate typing text with delay, stops if stop_key pressed."""
    count = 0
    for ch in text:
        if keyboard.is_pressed(stop_key):
            print(f"\n[{stop_key.upper()} pressed] Typing aborted.")
            return
        pyautogui.typewrite(ch, interval=delay)
        count += 1
        if chunk > 0 and count % chunk == 0:
            time.sleep(min(0.03, delay * 2))

def main():
    parser = argparse.ArgumentParser(description="Auto-type or paste text (macOS safe, with stop key).")
    parser.add_argument("-f", "--file", help="Path to a text file containing the text to type.")
    parser.add_argument("-t", "--text", help="Text to type directly (if no file).")
    parser.add_argument("-m", "--mode", choices=["paste", "type"], default="paste",
                        help="Use 'paste' for fastest (⌘V) or 'type' to simulate keystrokes.")
    parser.add_argument("-d", "--delay", type=float, default=0.0,
                        help="Delay between characters for 'type' mode (seconds).")
    parser.add_argument("-c", "--countdown", type=float, default=3.0,
                        help="Seconds to wait before starting (time to focus window).")
    parser.add_argument("-r", "--repeat", type=int, default=1,
                        help="Number of times to repeat typing/pasting.")
    parser.add_argument("--chunk", type=int, default=32,
                        help="Pause very briefly every N characters in 'type' mode (0 to disable).")
    parser.add_argument("--stop-key", default="esc",
                        help="Key to press to abort typing (default: esc).")

    args = parser.parse_args()
    text = read_text_source(args.file, args.text)

    print(f"✅ Press [{args.stop_key.upper()}] anytime to abort.\n")

    # Countdown
    if args.countdown > 0:
        for i in range(int(args.countdown), 0, -1):
            print(f"Starting in {i}…")
            time.sleep(1)
        rem = args.countdown - int(args.countdown)
        if rem > 0:
            time.sleep(rem)

    for i in range(args.repeat):
        if keyboard.is_pressed(args.stop_key):
            print(f"[{args.stop_key.upper()} pressed] Stopped before typing.")
            break

        if args.mode == "paste":
            paste_text(text)
        else:
            type_text(text, args.delay, args.chunk, args.stop_key)

        if i < args.repeat - 1:
            time.sleep(0.2)

if __name__ == "__main__":
    pyautogui.FAILSAFE = True  # move mouse to top-left corner to abort (extra failsafe)
    pyautogui.PAUSE = 0.0
    main()
