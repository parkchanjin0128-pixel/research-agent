"""Disposable test roots stay within the writable workspace on managed Windows."""
from pathlib import Path


def test_temp_root():
    path = Path(__file__).resolve().parents[1]/'.local/test-temp'
    path.mkdir(parents=True, exist_ok=True)
    return path
