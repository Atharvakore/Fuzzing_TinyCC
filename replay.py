from pathlib import Path
import subprocess


def replay_crashes():
    if not (Path(__file__).parent / "crashes").exists():
        print("No crashes directory found. Please map the crashes directory into the container according to the instructions in the README.")
        return
        
    crashes_dir = Path(__file__).parent / "crashes"
    for crash_file in crashes_dir.iterdir():
        if crash_file.is_file() and '.' not in crash_file.name:
            with open(crash_file, "rb") as f:
                input = f.read()
                result = subprocess.run(
                    ["tcc", "-o", "/dev/null", "-"],
                    input=input,
                    stderr=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                )
                if result.returncode < 0: # target crashed!
                    print(f"✅ Crash {crash_file.name} reproduced")
                else:
                    print(f"❌ Crash {crash_file.name} not reproduced")
                    
if __name__ == "__main__":
    replay_crashes()