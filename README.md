[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/deixdVUb)
# Project 1

Here's a simple challenge: Build a fuzzer that will reach as much code coverage on a C compiler as possible in one hour.

## Prerequisites
- Install [Docker](https://docs.docker.com/get-started/get-docker/). Your fuzzer will be run in a Docker container for evaluation. For additional information about Docker, refer to the [Getting Started Section of the Docker docs](https://docs.docker.com/get-started/).

## Your task
Implement your fuzzer in the function `yield_next_input` in `fuzzer/fuzzer.py`.
- You should already know how Python's `Generator`s work from the fuzzing book. Check [the wiki](https://wiki.python.org/moin/Generators) otherwise.
- You may add as many other files as necessary to the `fuzzer` directory.
- You may use the fuzzers provided in the fuzzing book, extend them, build your own, or combine them.
  - The only exception: You may not use C-specific test generators and fuzzers, such as [Csmith](https://github.com/csmith-project/csmith).

## Evaluation *(Changed on 2025-11-19)*

The project will be evaluated in two parts: Without seeds (part (a)) and with a set of high-quality seeds, provided by us (part (b)).
- Check out the function `get_seeds` in `fuzzer/project-evaluation.py`. It will provide you with the seeds for part (b). It will return an empty list for part (a).
  - You will only write one implementation. If you wish for your fuzzer to behave differently in the two parts, add a simple check for the return value of `get_seeds`. You're welcome to reuse all (or a part) of the logic of your fuzzer for part (a) for part (b).
  - You may not use the `SEEDS` variable in `fuzzer/project-evaluation.py` (or any other hard-coded seeds for that matter) in part (a).
  - Run your Docker container with `-e PROVIDE_SEEDS=1` to enable the seeds to test your fuzzer for task (b).
- We will run your fuzzer three times for part (a) and three times for part (b) for 1 hour each on a coverage-instrumented binary of the [Tiny C Compiler](https://www.bellard.org/tcc/)
  - We will limit your Docker container to a single core with 12GB of RAM on a workstation with a AMD Ryzen Threadripper 3960X CPU.
  - Additional runtime checks to prevent cheating may further slightly slow down execution.
- Coverage instrumentation is done with `gcov`, check the `Dockerfile` for details
  - We are only checking *branch coverage*
  - Of the three scores from the three runs, the *middle* score will count, to incentivize you to build a fuzzer that reaches coverage reliably.
- The grading will not be done in the CI, like with the exercises. We will, however, build and run your fuzzer with a very short timeout in the CI to test that it works in principle.
  - The points in the CI do not count towards your actual grade and are purely for your convenience.
  - If the CI fails because your fuzzer performs some setup before the actual fuzzing starts, and the timeout in the CI is not long enough to run this, and the check that your fuzzer reaches any coverage therefore fails, this is fine — we will still grade your fuzzer. Just make sure the Docker container can be built and works.

### Grading *(Changed on 2025-11-19)*

- You will have to reach the minimum coverage on both parts individually.
- The coverage you will have to reach for the passing and maximum grade respectively are:
  - For part (a): 25% and 40%
  - For part (b): 35% and 50%
- Assuming you reach the passing coverage on both parts, your project points will be calculated as follows:
  - min(`coverage_part_a`, 40) - 25 + min(`coverage_part_b`, 50) - 35
  - If you reach a total of 0 project points, you will get exactly the passing grade. 30 project points will give you the maximum grade.

## Rules
- Don't touch the following files — you will at the very least get points deducted:
  - `fuzzer/__init__.py`
  - *(Changed on 2025-11-19)* `fuzzer/project-evaluation.py`
  - `Dockerfile`
  - `run_and_get_coverage.sh`
- *(Changed on 2025-11-19)* Changed You must not add your own seeds, for either part of the evaluation.
- You must not interact with the instrumented binaries or any other information inside the `tinycc` directory. This also applies to runtime interaction, so don't call the target besides through the code in `fuzzer/__init__.py`.
  - *(Changed on 2025-11-19)* Do not rely on the coverage measured there either. If you need coverage feedback for your fuzzer, download and build TinyCC for a second time. Do not copy the TinyCC source, binary, or coverage files. We will patch the TinyCC instance used to evaluate coverage to prevent cheating and this may lead to your fuzzer crashing if you interact with it outside of the interface in `fuzzer/__init__.py`.
- You may add any additional dependency to either `requirements.txt` (for Python dependencies) or `apt-packages.txt` (for Debian packages). Don't push binaries to the GitHub repository, don't publish binaries specific to this project to package repositories or other internet sources.
- Please check that the Dockerfile still runs and builds with the following commands. We will not debug your code; if it doesn't work, you will fail this exercise with a 0.
  - Build the Docker container: `docker build -t project-1 .`
  - Run the Docker container: `docker run project-1`. You can set a shorter timeout with `docker run -e EVALUATION_TIME=<time_in_seconds> project-1` for testing.

## Hints
- Make sure your fuzzer performs well with the resource limits specified above. If it crashes (e.g. because it runs out of memory), it will not be restarted and this run will be awarded points according to the coverage reached when the fuzzer crashes (which may be 0 if no inputs have been yielded!).
- Re-run the evaluation locally multiple times to check if your fuzzer can reach your desired coverage reliably. Consider setting the same resource limits on your Docker container (`docker run --cpus="1" --memory="12g" project-1`) to check for crashes.
- Don't expect to reach 100% coverage. In this exercise (and in almost all real-world examples), this is not possible (e.g., because we're not testing all supported command line flags).
- Be creative! Try multiple approaches! Think outside the box! If you struggle to get additional coverage:
  - *(Fixed on 2025-11-19)* Look at the specific coverage your fuzzer reaches with the following: `docker run -v $(pwd)/coverage:/coverage project-1` and then look at `coverage/report.html`. Read the [chapter on coverage in the Fuzzing Book](https://www.fuzzingbook.org/html/Coverage.html) for some additional background.
  - This project is not primarily about a narrow application of fuzzers built for education. It is about finding the limits of various approaches and combining them to build an effective testing tool.
  - Some concepts from the material of future lectures and exercises may be helpful ([e.g.](https://www.fuzzingbook.org/html/MutationFuzzer.html)), but not necessary to get a passing grade.
  - A vast list of approaches to fuzzing has been suggested and evaluated. Some of those have been implemented in various popular open source fuzzers. You could use those, or borrow ideas and concepts from them.
- If your fuzzer finds crashes:
  - To get a copy of the crashes directory in your fuzzer on your host, run your fuzzer with the following argument: `docker run -v $(pwd)/crashes:/crashes project-1`.
  - Check to see if they are reproducible (run the target again with the same input and check if it crashes again). We provide the infrastructure for this in `replay.Dockerfile` and `replay.py`. Use as follows:
    - Build the container: `docker build -t project-1-replay -f replay.Dockerfile .`
    - Run it (this will replay all crashes in the crashes directory, mapped into the container again): `docker run -v $(pwd)/crashes:/crashes project-1-replay`
  - Then, try to [minimize the crashing input](https://www.fuzzingbook.org/html/Reducer.html).
  - Optional: See if you can find and patch the bug in TinyCC.
  - Before reporting the error/patch to the TinyCC project, reach out to one of the TAs via email.
  - Finding and fixing actual bugs may result in extra credit. During the preparation of this project, we have already found bugs, so this is definitely possible.
