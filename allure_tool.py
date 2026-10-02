"""Local Allure CLI manager (like allure-maven): downloads Allure into ./.allure on first use.

Usage:
    uv run python allure_tool.py install   # download only
    uv run python allure_tool.py generate  # allure-results -> allure-report
    uv run python allure_tool.py serve     # generate + open in browser
"""
import io
import os
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

ALLURE_VERSION = os.environ.get("ALLURE_VERSION", "2.46.1")
ROOT = Path(__file__).parent
ALLURE_HOME = ROOT / ".allure" / f"allure-{ALLURE_VERSION}"
RESULTS = ROOT / "allure-results"
REPORT = ROOT / "allure-report"
URL = (
    "https://github.com/allure-framework/allure2/releases/download/"
    f"{ALLURE_VERSION}/allure-{ALLURE_VERSION}.zip"
)


def allure_bin() -> Path:
    return ALLURE_HOME / "bin" / ("allure.bat" if os.name == "nt" else "allure")


def install() -> Path:
    if allure_bin().exists():
        return allure_bin()
    if not shutil.which("java"):
        sys.exit("Java is required by Allure but was not found on PATH.")
    print(f"Downloading Allure {ALLURE_VERSION}...")
    with urllib.request.urlopen(URL) as resp:
        data = resp.read()
    ALLURE_HOME.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        z.extractall(ALLURE_HOME.parent)
    if os.name != "nt":
        allure_bin().chmod(0o755)
    print(f"Installed to {ALLURE_HOME}")
    return allure_bin()


def run(*args: str) -> int:
    return subprocess.call([str(install()), *args])


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "serve"
    if cmd == "install":
        install()
        return 0
    if cmd == "generate":
        return run("generate", str(RESULTS), "-o", str(REPORT), "--clean")
    if cmd == "serve":
        return run("serve", str(RESULTS))
    return run(*sys.argv[1:])  # pass-through, e.g. `allure_tool.py --version`


if __name__ == "__main__":
    sys.exit(main())
