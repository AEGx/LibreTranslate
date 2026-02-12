import sys
from pathlib import Path

import main


def _create_venv_python(tmp_path):
    venv_bin = tmp_path / "venv" / ("Scripts" if sys.platform == "win32" else "bin")
    venv_bin.mkdir(parents=True)
    python_name = "python.exe" if sys.platform == "win32" else "python"
    venv_python = venv_bin / python_name
    venv_python.write_text("")
    return venv_python


def test_ensure_venv_python_reexecs_when_flask_missing(tmp_path, monkeypatch):
    venv_python = _create_venv_python(tmp_path)
    system_python = tmp_path / "system" / venv_python.name
    system_python.parent.mkdir(parents=True)
    system_python.write_text("")
    monkeypatch.setattr(main.sys, "executable", str(system_python))
    monkeypatch.setattr(main.sys, "argv", ["main.py", "--help"])
    monkeypatch.setattr(main.importlib.util, "find_spec", lambda name: None)

    exec_calls = {}

    def fake_execv(path, args):
        exec_calls["path"] = path
        exec_calls["args"] = args

    monkeypatch.setattr(main.os, "execv", fake_execv)

    main._ensure_venv_python(root_path=tmp_path)

    assert exec_calls["path"] == str(venv_python)
    assert exec_calls["args"] == [str(venv_python), "main.py", "--help"]


def test_ensure_venv_python_skips_when_flask_present(tmp_path, monkeypatch):
    exec_called = {"called": False}

    def fake_execv(path, args):
        exec_called["called"] = True

    monkeypatch.setattr(main.os, "execv", fake_execv)
    monkeypatch.setattr(main.importlib.util, "find_spec", lambda name: object())

    main._ensure_venv_python(root_path=tmp_path)

    assert not exec_called["called"]
