import pytest

from quantumcircuitsimulator.utils import log2

@pytest.mark.parametrize(
    "num, expected",
    [
        (
            # log2(2)
            2,
            1
        ),
        (
            # log2(8)
            8,
            3
        ),
        (
            # log2(256)
            256,
            8
        ),
    ]
)
def test_log2(num, expected):
    assert log2(num) == expected

