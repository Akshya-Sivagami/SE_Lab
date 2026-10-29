from photo_print_order import extra_print_charge


def test_large_non_canvas_order():
    assert extra_print_charge("4x6", 80, "matte", False) == 360