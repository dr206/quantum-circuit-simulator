import pytest
import numpy as np

from numpy.testing import assert_array_almost_equal as np_assert

from quantumcircuitsimulator.circuit import get_ground_state, get_operator, run_program

@pytest.mark.parametrize(
    "num_qubits, expected",
    [
        (
            # single qubit
            1,
            [1, 0]
        ),
        (
            # multi qubits
            3,
            [1, 0, 0, 0, 0 ,0, 0, 0]
        ),
    ]
)
def test_get_ground_state(num_qubits, expected):
    np_assert(get_ground_state(num_qubits), expected)


@pytest.mark.parametrize(
    "num_qubits, gate, target_qubits, params, expected",
    [
        (
            # n=1 X on qubit 0
            1, "X", [0], None,
            [
                [0, 1],
                [1, 0]
            ]
        ),
        (
            # n=2 X on qubits 0
            2, "X", [0], None,
            [
                [0,0,1,0],
                [0,0,0,1],
                [1,0,0,0],
                [0,1,0,0]
            ]
        ),
        (
            # n=2 X on qubit 1
            2, "X", [1],  None,
            [
                [0,1,0,0],
                [1,0,0,0],
                [0,0,0,1],
                [0,0,1,0]
            ]
        ),
        (
            # n=2 H on qubits 0 and 1
            2, "H", [0,1], None,
            [
                [0.5, 0.5, 0.5, 0.5],
                [0.5,-0.5, 0.5,-0.5],
                [0.5, 0.5,-0.5,-0.5],
                [0.5,-0.5,-0.5, 0.5]
            ]
        ),
        (
            # n=3 X on qubit 2
            3, "X", [2], None,
            [
                [0, 1, 0, 0, 0, 0, 0, 0,],
                [1, 0, 0, 0, 0, 0, 0, 0,],
                [0, 0, 0, 1, 0, 0, 0, 0,],
                [0, 0, 1, 0, 0, 0, 0, 0,],
                [0, 0, 0, 0, 0, 1, 0, 0,],
                [0, 0, 0, 0, 1, 0, 0, 0,],
                [0, 0, 0, 0, 0, 0, 0, 1,],
                [0, 0, 0, 0, 0, 0, 1, 0,]
            ]

        ),
        (
            # n=3 CNOT on 2 controlled by 0
            3, "CX", [0,2], None,
            [
                [1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 1, 0]
            ]
        ),
        (
            # n=1 U3 on qubit 0
            1, "U3", [0], { "theta": 3.1415, "phi": 1.5708, "lambda_angle": -3.1415 },
            [
                [0+0j, 1+0j],
                [0+1j, 0+0j]
            ]
        )
    ]
)
def test_get_operator(num_qubits, gate, target_qubits, params, expected):
    np_assert(
        get_operator(num_qubits, gate, target_qubits, params),
        expected,
        decimal=4
    )

    
@pytest.mark.parametrize(
    "ground_state, circuit, global_params, expected",
    [
        (
            # Create Bell state 00
            np.array([1, 0, 0, 0]),
            [
                { "gate": "h", "target": [0] },
                { "gate": "cx", "target": [0, 1] }
            ],
            None,
            np.array([0.70710678, 0, 0, 0.70710678])
        ),
        (
            # Create uniform superposition
            np.array([1, 0, 0, 0]),
            [
                { "gate": "h", "target": [0,1] }
            ],
            None,
            [0.5]*4
        ),
        (
            # Execute parametric gate
            np.array([1, 0]),
            [
                { "gate": "u3", "params": { "theta": 3.1415, "phi": 1.5708, "lambda_angle": -3.1415 }, "target": [0] }
            ],
            None,
            np.array([ 0+0j, 0+1j])
        ),
        (
            # Execute parametric gate with global parameters
            np.array([1, 0]),
            [
                { "gate": "u3", "params": { "theta": "global_1", "phi": "global_2", "lambda_angle": -3.1415 }, "target": [0] }
            ],
            { "global_1": 3.1415, "global_2": 1.5708 },
            np.array([ 0+0j, 0+1j])
        ),
    ]
)
def test_run_program(ground_state, circuit, global_params, expected):
    np_assert(
        run_program(ground_state, circuit, global_params),
        expected,
        decimal=4
    )
