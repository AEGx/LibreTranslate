import sys

import pytest

import libretranslate.init as init_module
import libretranslate.language as language_module
from libretranslate.app import create_app
from libretranslate.main import get_args


class DummyHypothesis:
    def __init__(self, value):
        self.value = value


class DummyTranslator:
    def __init__(self, to_lang):
        self.to_lang = to_lang

    def hypotheses(self, text, count):
        return [DummyHypothesis(text) for _ in range(count)]


class DummyTranslation:
    def __init__(self, to_lang):
        self.to_lang = to_lang


class DummyLanguage:
    def __init__(self, code, name=None):
        self.code = code
        self.name = name or code
        self.translations_from = []

    def get_translation(self, to_lang):
        if to_lang and any(t.to_lang.code == to_lang.code for t in self.translations_from):
            return DummyTranslator(to_lang)
        return None


@pytest.fixture()
def app(monkeypatch):
    dummy_en = DummyLanguage("en", "English")
    dummy_es = DummyLanguage("es", "Spanish")
    dummy_en.translations_from = [DummyTranslation(dummy_es)]
    dummy_es.translations_from = [DummyTranslation(dummy_en)]

    monkeypatch.setattr(init_module, "boot", lambda *args, **kwargs: None)
    monkeypatch.setattr(language_module, "load_languages", lambda: [dummy_en, dummy_es])
    language_module.load_lang_codes.cache_clear()

    sys.argv = ['', '--load-only', 'en,es']
    app = create_app(get_args())

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
