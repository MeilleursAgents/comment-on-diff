import pytest

from main import check_match


@pytest.mark.parametrize(
    ("regex", "test", "expected"),
    (
        ("yes", "yes I match", True),
        ("yes", "I do yes", False),
        ("yes", "nop", False),
        ("yes.*do", "yes I do", True),
        ("yes.*do", "really yes do", False),
        ("yes.*do", "yes nop", False),
    )
)
def test_check_match(regex, test, expected):
    assert check_match(regex, test) is expected
