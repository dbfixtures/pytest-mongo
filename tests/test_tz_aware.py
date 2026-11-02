"""Tests for mongo_tz_aware config option and CLI flag overrides."""

import pytest

pytest_plugins = ["pytester"]


@pytest.mark.parametrize(
    ("ini_val", "cli_args", "expected"),
    [
        (None, [], False),
        (None, ["--mongo-tz-aware"], True),
        (None, ["--no-mongo-tz-aware"], False),
        ("true", [], True),
        ("true", ["--mongo-tz-aware"], True),
        ("true", ["--no-mongo-tz-aware"], False),
        ("false", [], False),
        ("false", ["--mongo-tz-aware"], True),
        ("false", ["--no-mongo-tz-aware"], False),
    ],
)
def test_tz_aware_flag_overrides_ini(
    pytester: pytest.Pytester,
    ini_val: str | None,
    cli_args: list[str],
    expected: bool,
) -> None:
    """CLI flag should override ini setting for mongo_tz_aware."""
    if ini_val is not None:
        pytester.makeini(f"[pytest]\nmongo_tz_aware = {ini_val}\n")
    pytester.makepyfile(
        f"""
        from pytest_mongo.config import get_config

        def test_check_tz(request):
            assert get_config(request).tz_aware is {expected}
        """
    )
    result = pytester.runpytest(*cli_args, "-p", "pytest_mongo.plugin", "-p", "no:nonebug")
    result.assert_outcomes(passed=1)
