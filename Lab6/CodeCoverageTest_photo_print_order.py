import pytest
from photo_print_order import extra_print_charge, order_valid, dispatch_status


def test_unknown_print_size():
    with pytest.raises(ValueError):
        extra_print_charge("3x5", 10, "matte", False)


def test_negative_copies():
    with pytest.raises(ValueError):
        extra_print_charge("4x6", -1, "matte", False)


def test_member_extra_prints():
    assert extra_print_charge("4x6", 30, "matte", True) == 20


def test_canvas_large_order():
    assert extra_print_charge("8x10", 70, "canvas", False) == 840


def test_large_file_invalid():
    assert order_valid(30, 100, False) is False


def test_rush_order():
    assert order_valid(10, 40, True) is True


def test_dispatch_on_time():
    assert dispatch_status(24, False, False) == "on_time"


def test_dispatch_tight():
    assert dispatch_status(20, True, False) == "tight"


def test_dispatch_missed():
    assert dispatch_status(10, True, False) == "missed"


def test_international_dispatch():
    assert dispatch_status(40, False, True) == "on_time"