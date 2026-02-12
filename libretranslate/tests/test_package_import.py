import importlib
import sys


def test_package_import_without_flask(monkeypatch):
    """Package import should not fail if Flask is missing."""

    class FlaskImportBlocker:
        def find_spec(self, fullname, path=None, target=None):
            if fullname.startswith("flask"):
                raise ModuleNotFoundError("blocked")
            return None

    finder = FlaskImportBlocker()
    monkeypatch.delitem(sys.modules, "libretranslate", raising=False)
    monkeypatch.delitem(sys.modules, "flask", raising=False)
    monkeypatch.setattr(sys, "meta_path", [finder, *sys.meta_path], raising=False)

    libretranslate = importlib.import_module("libretranslate")

    assert libretranslate is not None
