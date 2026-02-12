from argostranslate import package
import pytest

from libretranslate.init import boot


@pytest.mark.skipif(
    not package.get_installed_packages(),
    reason="Argos Translate models are unavailable in the current environment.",
)
def test_boot_argos():
    """Test Argos translate models initialization"""
    boot(["en", "es"])

    assert len(package.get_installed_packages()) >= 2
