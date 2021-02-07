import numpy as np
import functools

from cmath import pi, sin, cos, exp

from .gates import *
from .utils import log2

def get_ground_state(num_qubits):
    """Create ground state for specified number of qubits.

    Args:
        num_qubits: the number of qubits that the ground state is comprised of.

    Returns:
        A array of size 2**num_qubits with all zeroes except first element which is 1.

        For 3 qubits it returns:

        [1, 0, 0, 0, 0, 0, 0, 0]
    """    
    ground_state = a = np.zeros(2**num_qubits)
    ground_state[0] = 1
    return ground_state


def get_operator(total_qubits, gate_unitary, target_qubits, params = None):
    """Create a matrix operator for a unitary gate for a circuit with specified number of qubits.

    Args:
        total_qubits: the total number of qubits in the circuit
        gate_unitary: the string name of the gate
        target_qubits: the indices of the qubits that the gate operates on
        params (optional): a dictionary of parameter

    Returns:
        an 2**total_qubits by 2**total_qubits matrix representation of the unitary gate
        operating on the specified target qubits
    """

    CONTOL_GATE_INDICATOR = 'C'
    
    # ensure that the gate name is all uppercase
    gate_unitary = gate_unitary.upper()

    
    def get_gate_from_name(name, params=None):
        PARAMETRIC_GATE_NAME = "U3"

        # only process a parametric gate if there are available parameters and the gate is named 'U3"
        # this does not yet handle the case for 'U3' without params, exception case
        if name == PARAMETRIC_GATE_NAME and params is not None:
            # replace the key for the angle 'lamda' to provent issue during eval() due to the Python keyword 'lambda'
            params["lambda_angle"] = params.pop("lambda")

            # create a function that can operate on a matrix (numpy array) that evaluates trigonometric functions using
            # the values specified in the params dictionary
            gate_evaluator = np.vectorize(lambda gate: eval(gate, { "sin": sin, "cos": cos, "exp": exp}, params))            

            parametric_gate = KNOWN_GATES[PARAMETRIC_GATE_NAME]
            return gate_evaluator(parametric_gate)
        return KNOWN_GATES[name]
    
    def multiply_gates(gate_unitary, operation_target_qubits, projector=None, control_target_qubit=None):
        # initialise a list of total_qubits copies of the identity matrix
        gates = [I] * total_qubits

        # replace an identity matrix with a gate operation for each target qubit
        for target_qubit in operation_target_qubits:
            gates[target_qubit] = gate_unitary

        # replace an identiy matrix with a projector operator if there is a control qubit
        if projector is not None and control_target_qubit is not None:
            gates[control_target_qubit] = projector

        # create a tensor product from the list of gate operators
        return functools.reduce(lambda a,b : np.kron(a, b), gates)
    
    # determine from the gate name if the gate is a control gate or not
    is_a_controlled_gate = (gate_unitary[0] == CONTOL_GATE_INDICATOR)

    if is_a_controlled_gate:
        gate = get_gate_from_name(gate_unitary[1:], params)

        matrix_operator \
        = multiply_gates(I,    [target_qubits[1]], P0x0, target_qubits[0]) \
        + multiply_gates(gate, [target_qubits[1]], P1x1, target_qubits[0])
        
        return matrix_operator
    else:
        gate = get_gate_from_name(gate_unitary, params)

        matrix_operator = multiply_gates(gate, target_qubits)

        return matrix_operator


def run_program(initial_state, program, global_params=None):
    """Execute a circuit on a given initial state.
    
    A circuit is defined by a program, which is a list of gate operations, and optional globally defined parameters.
    The globally defined paramters are applied to all gates that include such parameters names as values in their own parameters,
    e.g.
    for
        { "gate": "u3", "params": { "theta": "global_1", "phi": "global_2", "lambda": -3.1415 }, "target": [0] }
    the following global parameters can be applied
         { "global_1": 3.1415, "global_2": 1.5708 }

    Args:
        initial_state: the input state vector to be transformed
        program: a list of gate data that includes gate name, gate specific parameters, and target qubits.
        global_params (optional): parameters that are global to all gates

    Returns:
        the final state vector that corresponds to the output of the application of the programs gates to the initial state vector
    """

    # calculate the number of qubits based on the size of the state vector
    n = log2(len(initial_state))

    # the accumulated state for the application of each gate
    accumulated_state = initial_state

    for gate_application in program:
        gate = gate_application.get("gate")
        target = gate_application.get("target")
        params = gate_application.get("params")

        if global_params != None:
            # when global parameters are present:
            # replace a gates reference to the global param with the value of that global param
            for angle, potential_global_param in params.items():
                if potential_global_param in global_params:
                    params[angle] = global_params[potential_global_param]

        matrix_operator = get_operator(n, gate, target, params)
        
        accumulated_state = np.dot(matrix_operator, accumulated_state)

    return accumulated_state
