"""
Unit and regression test for the pulsecalc package.
"""

import sys

# Import package, test suite, and other packages as needed
import pulsecalc
import pytest


def test_pulsecalc_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "pulsecalc" in sys.modules
