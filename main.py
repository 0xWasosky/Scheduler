import json
import time
import subprocess
from multiprocessing import Process


def run_file(command: str):
    subprocess.run(command, shell=True)


def timer(s: int, file: str, mode: str, modes: dict):

    counter = 1

    while counter <= s:
        time.sleep(1)
        counter += 1

    if mode == "exec":

        p = Process(target=run_file, args=(f"./{file}",))
        p.start()
        p.join()
    else:
        if modes.get(mode) is None:
            exit(1)
        else:
            p = Process(target=run_file, args=(modes.get(mode) + " " + file,))
            p.start()
            p.join()


def manage_timers(files: dict, interpreters: dict) -> None:
    processes = []

    for file, opt in files.items():
        process = Process(target=timer, args=(opt[0], file, opt[1], interpreters))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()


if __name__ == "__main__":
    with open("interpreters.json", "r") as f:
        interpreters = json.load(f)

    with open("files.json", "r") as f:
        files = json.load(f)

    while 1:
        manage_timers(files, interpreters)
