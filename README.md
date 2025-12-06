# Scheduler

A lightweight Python scheduler that launches external scripts at configured intervals. Configuration is provided via two JSON files: `interpreters.json` and `files.json`.

This project contains the following primary files (in the `src` directory):

- `main.py` — scheduler entry point and runtime logic.
- `interpreters.json` — mapping of interpreter names to command paths.
- `files.json` — mapping of file paths to scheduling options.

Table of contents
-----------------

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Configuration](#configuration)
- [Usage](#usage)
- [Configuration Examples](#configuration-examples)
- [Runtime Behavior](#runtime-behavior)

Overview
--------

The scheduler reads `interpreters.json` and `files.json` and continuously spawns timed processes that wait for a configured interval and then run the target file. Each configured file runs in a separate process.

Features
--------

- Interval-based execution of scripts or executables.
- Support for interpreter aliases mapped in `interpreters.json`.
- Uses Python `multiprocessing` to run each scheduled task separately.

Requirements
------------

- Python 3.10 or newer.
- No additional Python packages are required for the current implementation.

Configuration
-------------

Two JSON configuration files are required and should be located in the same directory where `main.py` is executed.

- `interpreters.json` — a JSON object that maps an interpreter name to the interpreter command (string).

  Example structure:

  ```json
  {
    "python": "/usr/bin/python3",
    "bash": "/bin/bash"
  }
  ```

- `files.json` — a JSON object where each key is a file path (relative or absolute) and each value is a two-element array: `[interval_seconds, mode]`.

  - `interval_seconds`: integer number of seconds to wait before running the file.
  - `mode`: either the name of an interpreter defined in `interpreters.json` or the literal string `"exec"` to run the file as an executable (prefixed with `./`).

  Example structure:

  ```json
  {
    "./test.py": [10, "python"],
    "./bin/my_executable": [60, "exec"]
  }
  ```

Usage
-----

Run the scheduler from the project root (or from `src` if running there) so that `main.py`, `interpreters.json`, and `files.json` are accessible:

```bash
python3 src/main.py
# or
cd src
python3 main.py
```

The scheduler runs indefinitely, creating a timer process for each configured file during each cycle.

Configuration Examples
----------------------

Minimal `interpreters.json`:

```json
{
  "python": "/usr/bin/python3",
  "bash": "/bin/bash"
}
```

Minimal `files.json`:

```json
{
  "./test.py": [5, "python"],
  "./main": [3, "exec"]
}
```

Runtime Behavior
----------------

- For each entry in `files.json`, the scheduler spawns a process which runs the `timer` routine.
- The `timer` routine waits `interval_seconds` seconds (implemented as `time.sleep(1)` in a loop) and then executes the target file.
- If the `mode` is `"exec"`, the scheduler executes the file as `./{file}`. Otherwise it constructs a command using the interpreter mapping: `{interpreter_command} {file}`.

