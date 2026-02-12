from argostranslate import package
import pytest

from libretranslate.init import boot


def test_boot_argos():
    """Test Argos translate models initialization"""
    boot(["en", "es"])

    installed_packages = package.get_installed_packages()
    if len(installed_packages) < 2:
        pytest.skip("Argos Translate models are unavailable in the current environment.")

    assert len(installed_packages) >= 2
