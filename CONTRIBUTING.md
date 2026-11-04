# Notes

Most sections below are subject to change in the near future as the team does more research into what type of TRNG we want to build and what its development will look like.

# Contributing Guide

How to set up, code, test, review, and release so contributions meet our Definition of Done.

This is unclear at this time; will be updated following further discussion with the group and project partner.

## Code of Conduct

See the Team Charter for the general guidelines of the Code of Conduct: [Team Charter](https://docs.google.com/document/d/1lhDVcDhi6ujgrWubperdLsykDccozzaA1HQHPyKgDjU/edit?usp=sharing)

## Getting Started

As the TRNG is still in development, this is subject to change once more components are added. Currently, the user only needs to clone the repository to get started. There will likely be a final python file that they can eventually run to utilize the TRNG.

## Branching & Workflow

To name a branch, include the main focus of the adjustments being made (like the main file up for editing) in the title. The default branch is main, and a pull request should happen before any merges to main.

## Issues & Planning

Explain how to file issues, required templates/labels, estimation, and triage/assignment practices.

To file an issue, assign it a unique ID value (like #82), which makes it simple for future referencing. 

## Commit Messages

Convential Commits: Commit messages should briefly summarize any changes made and where they occurred, with the following as an example:
"new tests for uniqueness added to test_suite.py".

To reference issues, use the unique ID assigned to each individual one to locate it.

## Code Style, Linting & Formatting

Name the formatter/linter, config file locations, and the exact commands to check/fix locally.

This is unclear at this time; will be updated following further discussion with the group and project partner.

## Testing

Use entropy.py (or other file if this changes during development) to check entropy levels of TRNG values. Use the testing suite in the unit test framework file to check for errors in the code, with more tests added to this file to correspond with any new code added to the project.

## Definition of Done

Our Definition of Done should apply to each change we merge. A change is done when it meets its requirements, passes relevant tests, has been reviewed and approved by another teammate(s), includes any needed documentation updates, and passes automated checks for common coding mistakes or potential security problems. We plan to build a test suite, where we’ll identify the sprint and owner for each check that isn’t set up yet. As we continue to research the generator, we can add or change specific testing requirements as needed!

## Contribution Norm

The floor of work per sprint is that all group members contribute at least one piece of work they own to every sprint.

For the time being, all research and writing contributions will live in the group's shared Google Drive folder, while any code contributions will live in the group's repository.

An owned piece of work is something created by the owner, whether that be a piece of code, a section of a document, a new document they started, etc.

For a piece of work in a document to be accepted, at least one other group member reviewed the work done and informed the owner that their work was satisfactory, either through a message in the shared Discord server or as a comment on the section they reviewed.

For a piece of work regarding code to be accepted, a pull request was made by the owner and then accepted by a different group member.

In terms of the timeframe for reviewing other group members' contributions, the team will discuss and add this once we come to an agreement on the acceptable range of time to complete reviews.

## Pull Requests & Reviews

Outline PR requirements (template, checklist, size limits), reviewer expectations, approval rules, and required status checks.

A pull request title should summarize what changes will be made to the main branch of code. Additionally, there aren't any size limits currently, unless it will majorly conflict with what already exists. In that case, requests should occur frequently to decrease the number of changes per merge. Reviewers should always be a different person than the one initializing the request, and they must read through the changes to ensure that they don't appear to create any major complications to the project. Run code through the test suite as needed.

## CI/CD

Link to pipeline definitions, list mandatory jobs, how to view logs/re-run jobs, and what must pass before merge/release.

Currently, the CI is in development, as we are still determining the exact structure we want to use for the TRNG, and depending on our final decision, the CI could differ greatly. After we have built it, this will update to include the parts listed in the previous paragraph.

## Security & Secrets

State how to report vulnerabilities, prohibited patterns (hard-coded secrets), dependency update policy, and scanning tools.

This is unclear at this time; will be updated following further discussion with the group and project partner.

## Documentation Expectations

Specify what must be updated (README, docs/, API refs, CHANGELOG) and docstring/comment standards.

As the TRNG develops further, any documents with placeholders should be changed (ex: CONTRIBUTING.md, README.md, etc.). There should be some level of commenting/docstrings, with enough detail for others to understand what the code does.

## Release Process

Describe versioning scheme, tagging, changelog generation, packaging/publishing steps, and rollback process.

## Support & Contact

Any questions posed by group members should be asked in the group's Discord server in the appropriate channel. If further communication is necessary with either the project partner or the TA, use school email. Responses should occur within the next few business days for group members.
