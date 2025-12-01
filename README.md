
---

````markdown
# TinyCC Fuzzer

This project contains my implementation of a fuzzer designed to explore and maximize branch coverage in the Tiny C Compiler (TCC).  
The fuzzer runs inside a Docker environment and attempts to generate effective C test cases within a one-hour time budget.

## Prerequisites

- Install [Docker](https://docs.docker.com/get-started/get-docker/).  
  The fuzzer is built and executed entirely within a container.

## Overview

The core logic is implemented in `fuzzer/fuzzer.py`.  
The main generator function:

```python
yield_next_input()
````

produces an unbounded sequence of C programs. TCC compiles each input, and coverage information is recorded.

Key aspects:

* Inputs are produced via Python generators.
* Additional helper modules or fuzzing components can be added to the `fuzzer/` directory.
* The design allows combining different fuzzing strategies (mutation, generation, hybrid approaches, seed-based logic, etc.).
* No external C-specific generators such as Csmith are used.

## Fuzzing Modes

The fuzzer is evaluated in two configurations:

1. **Without seeds**
   No initial inputs are provided. The fuzzer starts exploring from scratch.

2. **With seeds**
   A set of seed programs is supplied through the function `get_seeds()` in `fuzzer/project-evaluation.py`.
   The same fuzzer implementation may adapt its behavior depending on whether seeds are available.

Constraints:

* For the “no seeds” mode, the fuzzer must not rely on hard-coded inputs.
* For the “with seeds” mode, only the provided seeds are used.

## Evaluation Setup

For each mode (with and without seeds):

* The container is executed three times.
* Each run lasts **1 hour**.
* Branch coverage on an instrumented version of TinyCC is measured.
* The **median** coverage result across the three runs is used.

Coverage instrumentation uses `gcov` (see the `Dockerfile`).

## Repository Structure and Constraints

Certain files define the evaluation environment and are not modified:

* `fuzzer/__init__.py`
* `fuzzer/project-evaluation.py`
* `Dockerfile`
* `run_and_get_coverage.sh`

Additional guidelines:

* No custom seeds are added beyond seeds delivered dynamically via `get_seeds`.
* The instrumented TinyCC build in `tinycc/` is treated as a black box and is accessed only via the provided interface.
* A separate local TinyCC build may be used for development experiments if needed.

## Dependencies

You may add:

* Python packages to `requirements.txt`
* Debian packages to `apt-packages.txt`

No binary files are committed to the repository.

## Building and Running

Build the container:

```bash
docker build -t project-1 .
```

Run the fuzzer:

```bash
docker run project-1
```

Optionally shorten evaluation time:

```bash
docker run -e EVALUATION_TIME=<seconds> project-1
```

Approximate evaluation resource limits:

```bash
docker run --cpus="1" --memory="12g" project-1
```

## Viewing Coverage Results

To inspect coverage locally:

```bash
docker run -v $(pwd)/coverage:/coverage project-1
```

Then open:

```
coverage/report.html
```

This helps identify unexplored code regions.

## Handling Crashes

If the fuzzer triggers crashes in TinyCC, they are stored in the `crashes/` directory.

Retrieve crash files:

```bash
docker run -v $(pwd)/crashes:/crashes project-1
```

Replay crashes:

1. Build the replay image:

   ```bash
   docker build -t project-1-replay -f replay.Dockerfile .
   ```

2. Execute the replay:

   ```bash
   docker run -v $(pwd)/crashes:/crashes project-1-replay
   ```

This verifies reproducibility and allows further input minimization.

## Notes

* The fuzzer must remain stable under the given 1-core, 12-GB RAM limits.
  If it crashes, only coverage accumulated before the crash is counted.
* Local repeated runs help ensure consistent behavior.
* Full coverage is not expected; the goal is to push coverage as far as practical.
* Experimentation with multiple fuzzing approaches is encouraged.

```

```
