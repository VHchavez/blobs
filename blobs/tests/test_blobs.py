"""
Unit and regression test for the blobs package.
"""

# Import package, test suite, and other packages as needed
import blobs
import pytest
import sys

def test_blobs_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "blobs" in sys.modules
