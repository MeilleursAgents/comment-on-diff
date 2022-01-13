import pytest

from main import check_match, normalize_comment, read_params


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
    ("comment", "expected"),
    (
        ("this is a test", "this is a test"),
        ("[ ] a check box unchecked", "[ ] a check box unchecked"),
        ("[x] a check box checked", "[ ] a check box checked"),
    ),
)
def test_normalize_comment(comment, expected):
    assert normalize_comment(comment) == expected


@pytest.mark.parametrize(
    ("params", "expected"),
    (
        ("some message", ("some message", False)),
        ({"msg": "some message", "absent": True}, ("some message", True)),
    ),
)
def test_read_params__ok(params, expected):
    assert read_params(params) == expected


def test_read_params__invalid():
    with pytest.raises(ValueError):
        read_params(["invalid", "parmas"])
