from app.services.logo_service import stream_zip_filename


def test_stream_zip_filename_uses_title_and_date() -> None:
    name = stream_zip_filename("Турнир Весна", "19.03.2026")
    assert name.endswith("_assets.zip")
    assert "19.03.2026" in name


def test_stream_zip_filename_empty_title_fallback() -> None:
    name = stream_zip_filename("   ", "01.01.2026")
    assert name.startswith("stream_")
