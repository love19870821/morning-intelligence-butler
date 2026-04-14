from scripts.smoke_test import main as smoke_main


def test_smoke_test_script_runs():
    assert smoke_main() == 0
