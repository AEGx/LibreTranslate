import libretranslate.app as app_module
import libretranslate.init as init_module
import libretranslate.language as language_module
from libretranslate.app import create_app
from libretranslate.main import get_parser


class DummyTranslation:
    """Minimal translation stub for create_app tests."""

    def __init__(self, to_lang):
        self.to_lang = to_lang


class DummyLanguage:
    """Minimal language stub for create_app tests."""

    def __init__(self, code):
        self.code = code
        self.name = code
        self.translations_from = []


def test_create_app_with_disabled_file_translation(monkeypatch):
    """Ensure create_app skips file format discovery when file translation is disabled."""

    dummy_en = DummyLanguage("en")
    dummy_es = DummyLanguage("es")
    dummy_en.translations_from = [DummyTranslation(dummy_es)]
    dummy_es.translations_from = [DummyTranslation(dummy_en)]

    monkeypatch.setattr(init_module, "boot", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        language_module, "load_languages", lambda: [dummy_en, dummy_es]
    )

    def _fail_if_formats_accessed():
        raise AssertionError("get_supported_formats should not be called")

    monkeypatch.setattr(app_module, "get_supported_formats", _fail_if_formats_accessed)

    parser = get_parser()
    args = parser.parse_args(["--load-only", "en,es", "--disable-files-translation"])
    if args.url_prefix and not args.url_prefix.startswith("/"):
        args.url_prefix = "/" + args.url_prefix

    app = create_app(args)

    assert app is not None
