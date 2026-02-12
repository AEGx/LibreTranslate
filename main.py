import importlib.util
import os
import sys
from pathlib import Path


def _venv_python(root_path=None):
    base_path = Path(root_path) if root_path is not None else Path(__file__).resolve().parent
    venv_path = base_path / "venv"
    if sys.platform == "win32":
        python_path = venv_path / "Scripts" / "python.exe"
    else:
        python_path = venv_path / "bin" / "python"
    return python_path if python_path.is_file() else None


def _ensure_venv_python(root_path=None):
    if importlib.util.find_spec("flask") is not None:
        return
    venv_python = _venv_python(root_path)
    if venv_python is not None and Path(sys.executable).resolve() != venv_python.resolve():
        os.execv(str(venv_python), [str(venv_python), *sys.argv])
        return
    raise SystemExit(
        "Flask is required to run LibreTranslate. Install dependencies with "
        "'pip install .' or use the Python executable from the project's venv."
    )


def _run():
    _ensure_venv_python()
    from libretranslate import main as libretranslate_main

    libretranslate_main()


if __name__ == "__main__":
    _run()
