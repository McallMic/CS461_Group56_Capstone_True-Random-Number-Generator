"""Check the data quality of a mouse_capture.py CSV recording."""

import argparse
import csv
from pathlib import Path
from statistics import median


COLUMNS = ("elapsed_ns", "dt_ns", "x", "y", "dx", "dy")


def check_recording(csv_path, gap_ms):
    samples = []
    problems = []
    seen_events = set()
    duplicate_events = 0
    malformed_rows = 0

    try:
        with csv_path.open("r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                return None, ["The file is empty or has no header."], 0, 0

            missing_columns = [name for name in COLUMNS if name not in reader.fieldnames]
            if missing_columns:
                return None, [
                    "Missing column(s): " + ", ".join(missing_columns)
                ], 0, 0

            for line_number, row in enumerate(reader, start=2):
                if None in row or any(value is None for value in row.values()):
                    malformed_rows += 1
                    problems.append(f"Line {line_number}: wrong number of CSV fields.")
                    continue

                event = tuple(row[name].strip() for name in COLUMNS)
                if event in seen_events:
                    duplicate_events += 1
                seen_events.add(event)

                try:
                    sample = {
                        "elapsed_ns": int(row["elapsed_ns"]),
                        "x": int(row["x"]),
                        "y": int(row["y"]),
                    }

                    for name in ("dt_ns", "dx", "dy"):
                        value = row[name].strip()
                        sample[name] = int(value) if value else None

                except ValueError:
                    malformed_rows += 1
                    problems.append(f"Line {line_number}: contains a non-integer value.")
                    continue

                samples.append(sample)

    except OSError as error:
        return None, [f"Could not open the file: {error}"], 0, 0

    if not samples:
        problems.append("No usable samples were found.")
        return samples, problems, malformed_rows, duplicate_events

    long_gaps = []
    intervals_ms = []

    for index, sample in enumerate(samples):
        line_number = index + 2

        if index == 0:
            continue

        previous = samples[index - 1]
        elapsed_gap = sample["elapsed_ns"] - previous["elapsed_ns"]

        if elapsed_gap <= 0:
            problems.append(
                f"Line {line_number}: elapsed_ns did not increase."
            )
            continue

        intervals_ms.append(elapsed_gap / 1_000_000)

        if elapsed_gap > gap_ms * 1_000_000:
            long_gaps.append((line_number, elapsed_gap / 1_000_000))

        if sample["dt_ns"] is None:
            problems.append(f"Line {line_number}: dt_ns is missing.")
        elif sample["dt_ns"] != elapsed_gap:
            problems.append(
                f"Line {line_number}: dt_ns doesn't match elapsed_ns."
            )

        expected_dx = sample["x"] - previous["x"]
        expected_dy = sample["y"] - previous["y"]

        if sample["dx"] != expected_dx:
            problems.append(f"Line {line_number}: dx doesn't match the x positions.")
        if sample["dy"] != expected_dy:
            problems.append(f"Line {line_number}: dy doesn't match the y positions.")

    print(f"Samples read: {len(samples)}")
    print(f"Malformed rows: {malformed_rows}")
    print(f"Duplicate events: {duplicate_events}")
    print(f"Unique cursor positions: {len({(s['x'], s['y']) for s in samples})}")

    first_event_ms = samples[0]["elapsed_ns"] / 1_000_000
    last_event_ms = samples[-1]["elapsed_ns"] / 1_000_000
    print(f"Time through last event: {last_event_ms / 1000:.2f} seconds")
    print(f"Span from first to last event: {(last_event_ms - first_event_ms) / 1000:.2f} seconds")

    if intervals_ms:
        print(f"Median time between events: {median(intervals_ms):.2f} ms")
        print(f"Gaps longer than {gap_ms:g} ms: {len(long_gaps)}")

    if problems:
        print("\nIssues:")
        for problem in problems:
            print(f"- {problem}")
    else:
        print("\nNo data-quality issues found.")

    return samples, problems, malformed_rows, duplicate_events


def plot_samples(samples):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("\nTo create plots, install matplotlib: pip install matplotlib")
        return

    times_ms = [s["elapsed_ns"] / 1_000_000 for s in samples]
    x_positions = [s["x"] for s in samples]
    y_positions = [s["y"] for s in samples]

    intervals_ms = [
        (samples[i]["elapsed_ns"] - samples[i - 1]["elapsed_ns"]) / 1_000_000
        for i in range(1, len(samples))
    ]

    figure, axes = plt.subplots(1, 2, figsize=(11, 4))

    axes[0].plot(x_positions, y_positions, linewidth=0.8)
    axes[0].set_title("Mouse movement")
    axes[0].set_xlabel("X position")
    axes[0].set_ylabel("Y position")
    axes[0].invert_yaxis()

    axes[1].plot(times_ms[1:], intervals_ms, linewidth=0.8)
    axes[1].set_title("Time between events")
    axes[1].set_xlabel("Elapsed time (ms)")
    axes[1].set_ylabel("Interval (ms)")

    figure.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser(
        description="Check a CSV recording produced by mouse_capture.py."
    )
    parser.add_argument("csv_file", type=Path, help="Path to the recording CSV")
    parser.add_argument(
        "--gap-ms",
        type=float,
        default=1000,
        help="Report intervals longer than this many milliseconds (default: 1000)",
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        help="Plot cursor movement and event timing",
    )
    args = parser.parse_args()

    samples, _, _, _ = check_recording(args.csv_file, args.gap_ms)

    if args.plot and samples:
        plot_samples(samples)


if __name__ == "__main__":
    main()