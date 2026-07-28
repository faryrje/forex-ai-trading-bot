from risk.position_sizing import calculate_position_size


def test_position_size():
    size = calculate_position_size(10000, 1, 50)
    assert size == 2
