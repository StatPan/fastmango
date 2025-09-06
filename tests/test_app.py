import pytest
from fastmango.app import MangoApp

def test_app_initialization():
    """
    Tests that the MangoApp can be initialized.
    """
    app = MangoApp()
    assert app is not None
