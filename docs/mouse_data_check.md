# Mouse recording data check

`mouse_data_check.py` checks the structure and internal consistency of a CSV created by `mouse_capture.py`. It uses only Python's standard library.

Run it from the repository root:

```bash
python mouse_data_check.py sample_data/your_recording.csv
```

The report summarizes the number of samples, elapsed time, unique cursor positions, recorded timing intervals, and stationary moves. It also flags malformed rows, missing values, non-increasing timestamps, timing differences that do not match `elapsed_ns`, and movement deltas that do not match the coordinate differences. The command exits with status 1 if it finds an error.

The checker assesses capture data quality only. It does not establish that mouse movement is random or suitable as a cryptographic entropy source.
