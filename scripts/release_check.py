#!/usr/bin/env python3
"""Local release verification for morning-intelligence-butler.

This checks the release path end-to-end:
- run the test suite
- run the first-run smoke test
- build a wheel
- install the wheel into a fresh virtual environment
- run the installed smoke test from that isolated environment
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path


def run_stage(label: str, cmd: list[str], *, cwd: Path) -> None:
    print(f"==> {label}")
    subprocess.run(cmd, cwd=cwd, check=True)


def venv_script_path(venv_dir: Path, name: str) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / f"{name}.exe"
    return venv_dir / "bin" / name


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        wheel_dir = tmp / "wheel"
        wheel_dir.mkdir(parents=True, exist_ok=True)
        venv_dir = tmp / "venv"

        try:
            run_stage("pytest", [sys.executable, "-m", "pytest", "tests", "-q"], cwd=repo_root)
            run_stage("smoke test", [sys.executable, str(repo_root / "scripts" / "smoke_test.py")], cwd=repo_root)
            run_stage(
                "build wheel",
                [sys.executable, "-m", "pip", "wheel", "--no-deps", "--wheel-dir", str(wheel_dir), "."],
                cwd=repo_root,
            )

            wheels = sorted(wheel_dir.glob("*.whl"))
            if not wheels:
                raise RuntimeError("No wheel artifact was produced")
            wheel = wheels[0]
            print(f"Wheel artifact: {wheel.name}")

            run_stage("create isolated venv", [sys.executable, "-m", "venv", str(venv_dir)], cwd=repo_root)

            venv_python = venv_script_path(venv_dir, "python")
            smoke_cmd = venv_script_path(venv_dir, "morning-butler-smoke")

            run_stage(
                "install wheel into isolated venv",
                [str(venv_python), "-m", "pip", "install", "--no-deps", str(wheel)],
                cwd=repo_root,
            )
            run_stage("run installed smoke test", [str(smoke_cmd)], cwd=repo_root)
        except subprocess.CalledProcessError as exc:
            print(f"Release check failed with exit code {exc.returncode}", file=sys.stderr)
            return exc.returncode or 1
        except Exception as exc:
            print(f"Release check failed: {exc}", file=sys.stderr)
            return 1

    print("Release check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())