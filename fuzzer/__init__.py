import hashlib
import os
import subprocess
import time

from fuzzer import yield_next_input

EVALUATION_TIME = int(os.environ.get("EVALUATION_TIME", 3600))  # default to 1 hour


def main():
    print(f"Running fuzzer for {EVALUATION_TIME} seconds")
    
    if not os.path.exists("crashes"):
        os.mkdir("crashes")

    runs = 0
    start_time = time.time()
    for input in yield_next_input():
        runs += 1
        result = subprocess.run(
            ["tcc", "-o", "/dev/null", "-"],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            input=input,
        )

        if result.returncode < 0: # target crashed!
            hash = hashlib.sha256(input).hexdigest()
            print(f"Found crash with hash: {hash}")
            with open(f"crashes/{hash}", "wb") as f:
                f.write(input)
            with open(f"crashes/{hash}.stderr", "wb") as f:
                f.write(result.stderr)
            with open(f"crashes/{hash}.stdout", "wb") as f:
                f.write(result.stdout)

        if time.time() - start_time > EVALUATION_TIME:
            break

    print(f"Ran fuzzer for {time.time() - start_time} seconds, {runs} runs")


if __name__ == "__main__":
    main()
