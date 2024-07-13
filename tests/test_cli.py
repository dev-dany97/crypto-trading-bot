from pathlib import Path

from trader_bot.__main__ import main

DATA = Path(__file__).resolve().parent.parent / "data" / "etheur_1d.csv"


def test_offline_mode_prints_signal(capsys):
    signal = main(["--offline", str(DATA)])
    out = capsys.readouterr().out
    assert signal in ("BUY", "WAIT")
    assert "ETHEUR" in out


def test_offline_mode_with_custom_days(tmp_path, capsys):
    csv_file = tmp_path / "candles.csv"
    csv_file.write_text("dateTime,high\n1,100\n2,99\n3,98\n4,97\n")
    assert main(["--offline", str(csv_file), "--days", "3", "--symbol", "BTCEUR"]) == "WAIT"
    assert "BTCEUR: high fell on 3 of the last 3 days" in capsys.readouterr().out
