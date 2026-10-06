from typer.testing import CliRunner

import codementor
from codementor.cli.main import app


def test_version_flag_prints_version() -> None:
    result = CliRunner().invoke(app, ["--version"])
    assert result.exit_code == 0
    assert codementor.__version__ in result.stdout
    assert "(kaynaktan)" in result.stdout
