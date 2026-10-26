"""Prototype for recording mouse movement and event timing."""

import csv
import time
from datetime import datetime
from pathlib import Path

from pynput import mouse


def main():
    samples = []
    previous = None
    start_ns = time.perf_counter_ns()

    def on_move(x, y, *extra):
        nonlocal previous
        timestamp_ns = time.perf_counter_ns()

        # The first event has no previous sample to compare against.
        if previous is None:
            dt_ns = dx = dy = ""
        else:
            previous_time, previous_x, previous_y = previous
            dt_ns = timestamp_ns - previous_time
            dx = x - previous_x
            dy = y - previous_y

        samples.append([
            timestamp_ns - start_ns,
            dt_ns,
            x,
            y,
            dx,
            dy,
        ])

        previous = (timestamp_ns, x, y)

    print("Recording mouse movement for 15 seconds.")
    print("Move your mouse. Press Ctrl+C to stop early.")

    # Capture cursor movement in a background thread.
    listener = mouse.Listener(on_move=on_move)
    listener.start()

    try:
        time.sleep(15)
    except KeyboardInterrupt:
        print("\nStopping early...")
    finally:
        listener.stop()
        listener.join()

    folder = Path("recordings")
    folder.mkdir(exist_ok=True)

    filename = datetime.now().strftime("mouse_%Y%m%d_%H%M%S_%f.csv")
    output_path = folder / filename

    # Save samples without overwriting an existing recording.
    with output_path.open("x", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "elapsed_ns", "dt_ns", "x", "y", "dx", "dy"
        ])
        writer.writerows(samples)

    print(f"Saved {len(samples)} samples.")
    print(f"File: {output_path.resolve()}")


if __name__ == "__main__":
    main()