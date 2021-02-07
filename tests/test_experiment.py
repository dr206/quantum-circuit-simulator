import pytest
import numpy as np

from quantumcircuitsimulator.experiment import measure_all, get_counts

def test_measure_bell_00():
    actual_result = measure_all(np.array([0.70710678, 0, 0, -0.70710678]))
    expected_states = ['00', '11']
    assert actual_result in expected_states


def test_run_1000_shots():
    actual_result = get_counts(np.array([0.70710678, 0, 0, -0.70710678]), 1000)
    expected_result = pytest.approx({ "00": 500, "11": 500 }, rel=1e-1)
    assert actual_result == expected_result
