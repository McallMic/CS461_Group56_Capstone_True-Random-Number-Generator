# Project Requirements

**Status:** Draft for team and project-partner review

## Problem Statement

Project 56: True Random Number Generator:
We aims to deliver a usable random-number generator that users can download, install, and test. The team’s initial use is to evaluate whether the generator’s output demonstrates the value of the TRNG approach. The intended audience beyond our team is not yet finalized yet.

The mouse-movement noise capture is our preliminary prototype, which we plan to replace with a different noise source. The source, digitization method, output format, and measurable success criteria will remain open.

## Functional Requirements

- **FR-1 — Generate random-number output (P1, proposed).** The system shall generate and provide random-number output using the noise source selected by the team.
  - **Acceptance:** A user can start a run and receive output in the documented format on a supported installation. The supported platform and output format remain open questions.

- **FR-2 — Preserve source samples (P1, proposed).** The system shall retain the captured raw samples at their available resolution and record enough metadata to interpret each capture.
  - **Acceptance:** A saved capture can be read back without sample values changing, and includes the agreed metadata. The required metadata fields and file format remain open.

- **FR-3 — Estimate min-entropy (P1, proposed).** The analysis component shall estimate min-entropy using the team’s selected Most Common Value (MCV) model and report the sample count and values used to calculate the estimate.
  - **Acceptance:** For a known input dataset, the reported MCV and estimate match a reference calculation. The confidence level and minimum sample count require team confirmation.

- **FR-4 — Install and run the generator (P1, proposed).** The project shall provide installation and usage instructions that allow someone outside the team to run the generator.
  - **Acceptance:** A person outside the team follows the documented steps on the selected operating system and obtains random-number output. The operating system and distribution channel remain open questions.

- **FR-5 — Compare against a baseline (P2, assumption to confirm).** The analysis should be able to evaluate TRNG output alongside a documented pseudorandom baseline using the same analysis method.
  - **Acceptance:** The report identifies the baseline, sample sizes, analysis method, and results for both datasets.

## Non-Functional Requirements

- **NFR-1 — Sample integrity (P1, proposed).** Processing and export shall not silently alter the captured raw samples.
  - **Acceptance:** A test confirms that sample values and count match before and after saving and loading a capture.

- **NFR-2 — Results traceability (P1, proposed).** Each entropy result shall identify the estimator and the sample count used.
  - **Acceptance:** The generated report includes those fields and the agreed estimator inputs.

- **NFR-3 — Installability (P1, proposed).** A user outside the development team shall be able to install and run the project using documented steps.
  - **Acceptance:** A clean installation succeeds on the selected platform without editing the source code.

## Constraints

- The mouse-movement recorder is an exploratory prototype. The team plans to replace it with a different noise source.
- The team has not yet selected the noise source, digitization method, or final circuit and hardware design.
- People outside the team must be able to download, install, and use the product. It will be distributed through GitHub.
- The team has not yet agreed on numeric success thresholds and plans to finalize them by the end of the week.

## Success Metrics

**Open:** The team has not selected numeric success criteria. Candidate measures include estimated min-entropy, sample size, output rate, and results against a pseudorandom baseline. The team and project partner should help choose measures and thresholds before treating them as acceptance targets.

## Non-Goals

- Using mouse movement as the final noise source.
- Claiming cryptographic suitability or security certification unless the team and project partner explicitly add and validate that goal.

## Open Questions

| Question | Proposed owner | Status |
|---|---|---|
| Which noise source and digitization method will the project use? | Research Manager and project partner | Open |
| Who is the intended user beyond the project team? | Project Manager and project partner | Open |
| What output type, range, and file or interface format should users receive? | Team | Open |
| Which operating systems and distribution channel must installation support? | Project Manager and project partner | Open |
| Which metrics, datasets, and thresholds define a successful result? | Team and project partner | Open |
| Should baseline comparison be a required feature? | Team and project partner | Open |
| What confidence level and minimum sample count should the MCV estimator require? | Quality Owner and project partner | Open |
