import subprocess
import time

TARGET_VOLUME = 50          # 0–100
CHECK_INTERVAL = 1          # seconds


def get_volume() -> int:
    """Return current output volume (0–100) using AppleScript."""
    result = subprocess.run(
        ["osascript", "-e", "output volume of (get volume settings)"],
        capture_output=True,
        text=True
    )
    return int(result.stdout.strip())


def set_volume(level: int):
    """Set output volume to given level (0–100) using AppleScript."""
    subprocess.run(
        ["osascript", "-e", f"set volume output volume {level}"],
        check=False
    )


def main():
    print(f"Locking volume at {TARGET_VOLUME}%. Press Ctrl+C to stop.")
    # Make sure it's correct from the start
    set_volume(TARGET_VOLUME)

    while True:
        try:
            current = get_volume()
            if current != TARGET_VOLUME:
                set_volume(TARGET_VOLUME)
        except Exception as e:
            # Optional: print errors but keep the script running
            print("Error checking/setting volume:", e)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
