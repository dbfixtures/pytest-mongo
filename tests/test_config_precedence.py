"""CLI options override ini values for both boolean MongoDB settings."""

import pytest

pytest_plugins = ["pytester"]


@pytest.mark.parametrize("option", ["tls", "tz_aware"])
@pytest.mark.parametrize(
    ("ini_value", "flag", "expected"),
    [
        (None, None, False),
        (None, True, True),
        (None, False, False),
        ("true", None, True),
        ("true", True, True),
        ("true", False, False),
        ("false", None, False),
        ("false", True, True),
        ("false", False, False),
    ],
)
def test_boolean_config_precedence(
    pytester: pytest.Pytester,
    option: str,
    ini_value: str | None,
    flag: bool | None,
    expected: bool,
) -> None:
    """An explicit false flag must remain distinct from an unspecified flag."""
    if ini_value is not None:
        pytester.makeini(f"[pytest]\nmongo_{option} = {ini_value}\n")
    pytester.makepyfile(
        f"""
        from pytest_mongo.config import get_config

        def test_config(request):
            assert get_config(request).{option} is {expected}
        """
    )
    args = []
    if flag is not None:
        prefix = "--mongo-" if flag else "--no-mongo-"
        args.append(prefix + option.replace("_", "-"))
    result = pytester.runpytest(*args, "-p", "pytest_mongo.plugin", "--disable-plugin-autoload")
    result.assert_outcomes(passed=1)
