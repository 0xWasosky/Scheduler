import json
import asyncio
import subprocess
from multiprocessing import Process


def run_file(command: str):
    subprocess.run(command, shell=True)


async def timer(s: int, file: str, mode: str, modes: dict):

    while True:
        if mode == "exec":
            p = Process(target=run_file, args=(f"./{file}",))
            p.start()

        else:
            if modes.get(mode) is None:
                exit(1)
            else:
                p = Process(target=run_file, args=(modes.get(mode) + " " + file,))
                p.start()
                p.join()

        await asyncio.sleep(s)


async def manage_timers(files: dict, interpreters: dict) -> None:
    processes = []

    for file, opt in files.items():
        processes.append(timer(opt[0], file, opt[1], interpreters))

    await asyncio.gather(*processes)


if __name__ == "__main__":
    with open("interpreters.json", "r") as f:
        interpreters = json.load(f)

    with open("files.json", "r") as f:
        files = json.load(f)

    asyncio.run(manage_timers(files, interpreters))
