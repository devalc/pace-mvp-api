from pace_downloader.core import run_download, download_daily, download_monthly

def test_imports():
    """Verify core functions import correctly."""
    assert callable(run_download)
    assert callable(download_daily)
    assert callable(download_monthly)

def test_cli_help():
    import subprocess
    result = subprocess.run(
        ["pace-download", "--help"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "PACE data downloader" in result.stdout
