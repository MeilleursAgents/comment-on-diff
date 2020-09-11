import pytest

from main import check_match


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
    )
)
def test_check_match(regex, tests, expected):
    assert check_match(regex, tests) is expected
