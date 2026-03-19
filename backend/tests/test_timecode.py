from app.utils.timecode import seconds_to_hhmmss


def test_seconds_to_hhmmss() -> None:
    assert seconds_to_hhmmss(0) == "00:00:00"
    assert seconds_to_hhmmss(10) == "00:00:10"
    assert seconds_to_hhmmss(600) == "00:10:00"
    assert seconds_to_hhmmss(3661) == "01:01:01"
    assert seconds_to_hhmmss(-5) == "00:00:00"
