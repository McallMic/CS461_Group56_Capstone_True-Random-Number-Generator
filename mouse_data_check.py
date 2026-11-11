"""Check a mouse_capture.py CSV recording for data quality issues."""

import argparse
import csv
import sys
from pathlib import Path
from statistics import mean


REQUIRED_COLUMNS = ("elapsed_ns", "dt_ns", "x", "y", "dx", "dy")
INTEGER_COLUMNS = ("elapsed_ns", "x", "y")
OPTIONAL_INTEGER_COLUMNS = ("dt_ns", "dx", "dy")


def inspect_recording(path: Path) -> tuple[list[str], list[str]]:
    """Return summary lines and data-quality findings for one recording."""
    findings: list[str] = []
    rows: list[dict[str, str]] = []

    try:
        with path.open("r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames
            if headers is None:
                return ["Rows: 0"], ["ERROR: The file is empty or has no CSV header."]

            missing_headers = [name for name in REQUIRED_COLUMNS if name not in headers]
            if missing_headers:
                return ["Rows: 0"], [
                    "ERROR: Missing required column(s): " + ", ".join(missing_headers)
                ]

            for line_number, row in enumerate(reader, start=2):
                if None in row:
                    findings.append(f"ERROR: Line {line_number} has extra CSV fields.")
                    continue
                if any(value is None for value in row.values()):
                    findings.append(f"ERROR: Line {line_number} has fewer fields than the header.")
                    continue
                rows.append(row)
    except (OSError, UnicodeError, csv.Error) as error:
        return [], [f"ERROR: Could not read CSV: {error}"]

    if not rows:
        findings.append("WARNING: The recording contains no samples.")
        return ["Rows: 0"], findings

    parsed: list[dict[str, int | None]] = []
    for row_number, row in enumerate(rows, start=2):
        values: dict[str, int | None] = {}
        for column in INTEGER_COLUMNS:
            raw = row[column].strip()
            try:
                values[column] = int(raw)
            except ValueError:
                findings.append(f"ERROR: Line {row_number} has a non-integer {column!r} value.")
                values[column] = None
        for column in OPTIONAL_INTEGER_COLUMNS:
            raw = row[column].strip()
            if raw == "":
                values[column] = None
            else:
                try:
                    values[column] = int(raw)
                except ValueError:
                    findings.append(f"ERROR: Line {row_number} has a non-integer {column!r} value.")
                    values[column] = None
        parsed.append(values)

    for index, row in enumerate(parsed):
        line_number = index + 2
        if any(row[column] is None for column in INTEGER_COLUMNS):
            continue
        elapsed = int(row["elapsed_ns"])
        if elapsed < 0:
            findings.append(f"ERROR: Line {line_number} has a negative elapsed_ns value.")
        if index == 0:
            if any(row[column] is not None for column in OPTIONAL_INTEGER_COLUMNS):
                findings.append(f"WARNING: Line {line_number}, the first sample, has interval/delta values.")
            continue

        previous = parsed[index - 1]
        if any(previous[column] is None for column in INTEGER_COLUMNS):
            continue
        elapsed_gap = elapsed - int(previous["elapsed_ns"])
        if elapsed_gap <= 0:
            findings.append(f"ERROR: Line {line_number} does not have a later elapsed_ns than the prior sample.")
        if row["dt_ns"] is None:
            findings.append(f"WARNING: Line {line_number} is missing dt_ns.")
        elif int(row["dt_ns"]) <= 0:
            findings.append(f"ERROR: Line {line_number} has a non-positive dt_ns value.")
        elif int(row["dt_ns"]) != elapsed_gap:
            findings.append(f"WARNING: Line {line_number} dt_ns does not match the elapsed_ns difference.")

        expected_dx = int(row["x"]) - int(previous["x"])
        expected_dy = int(row["y"]) - int(previous["y"])
        for column, expected in (("dx", expected_dx), ("dy", expected_dy)):
            if row[column] is None:
                findings.append(f"WARNING: Line {line_number} is missing {column}.")
            elif int(row[column]) != expected:
                findings.append(f"WARNING: Line {line_number} {column} does not match the position difference.")

    valid_elapsed = [int(row["elapsed_ns"]) for row in parsed if row["elapsed_ns"] is not None]
    valid_dt = [int(row["dt_ns"]) for row in parsed[1:] if row["dt_ns"] is not None]
    positions = {
        (int(row["x"]), int(row["y"]))
        for row in parsed
        if row["x"] is not None and row["y"] is not None
    }
    stationary = sum(
        row["dx"] == 0 and row["dy"] == 0
        for row in parsed
        if row["dx"] is not None and row["dy"] is not None
    )
    summary = [f"Rows: {len(rows)}"]
    if valid_elapsed:
        summary.append(f"Elapsed span: {max(valid_elapsed) / 1e9:.3f} seconds")
    summary.append(f"Unique cursor positions: {len(positions)}")
    if valid_dt:
        summary.extend([
            f"Intervals (dt_ns): {len(valid_dt)} recorded",
            f"  minimum: {min(valid_dt)} ns",
            f"  mean: {mean(valid_dt):.0f} ns",
            f"  maximum: {max(valid_dt)} ns",
        ])
    summary.append(f"Recorded stationary moves (dx=0 and dy=0): {stationary}")

    if not any(item.startswith("ERROR:") for item in findings):
        findings.insert(0, "No structural or consistency errors found.")
    return summary, findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check a mouse_capture.py CSV recording for data quality issues."
    )
    parser.add_argument("csv_file", type=Path, help="Path to a recording CSV file")
    args = parser.parse_args()

    summary, findings = inspect_recording(args.csv_file)
    print(f"Mouse recording check: {args.csv_file}")
    for line in summary:
        print(line)
    print("Findings:")
    for finding in findings:
        print(f"- {finding}")
    # This tool checks capture integrity only; it does not certify randomness.
    return 1 if any(item.startswith("ERROR:") for item in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
