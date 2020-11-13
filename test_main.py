import pytest

from main import check_match, read_params


@pytest.mark.parametrize(
    ("regex", "tests", "expected"),
    (
        ("yes", ["idontmatch", "yes I do"], True),
        ("yes", ["yes I match", "nah"], True),
        ("yes", ["yes", "yesyes"], True),
        ("yes", ["I do yes", "really yes"], False),
        ("yes", ["nop", "still nop"], False),
        ("yes.*do", ["idontmatch", "yes I do"], True),
        ("yes.*do", ["yes I do match", "nah"], True),
        ("yes.*do", ["yes do", "yesyes do"], True),
        ("yes.*do", ["I do yes", "really yes do"], False),
        ("yes.*do", ["yes nop", "do still nop"], False),
    ),
)
def test_check_match(regex, tests, expected):
    assert check_match(regex, tests) is expected


@pytest.mark.parametrize(
    ("params", "expected"),
    (
        ("some message", ("some message", False)),
        ({"msg": "some message", "absent": True}, ("some message", True)),
    ),
)
def test_read_params(params, expected):
    assert read_params(params) == expected
