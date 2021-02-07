import numpy as np

# Define 2x2 Identity
I = np.identity(2)

# Define X gate
X = np.array([
    [0, 1],
    [1, 0]
])

# Define Y gate
Y = np.array([
    [0   , 0-1j],
    [0+1j, 0   ]
])

# Define Z gate
Z = np.array([
    [1,  0],
    [0, -1]
])

# Define H gate
H = np.array([
    [1,  1],
    [1, -1]
])/np.sqrt(2)

# Define parametric gate u3
# Here we use the parameter 'lambda_angle' so that when we perform eval(...)
# it is not conflicting with the Python keyword 'lambda'.)
U3 = np.array([
    [                "cos(theta / 2)", "-exp(1j * lambda_angle)            * sin(theta / 2)"],
    ["exp(1j * phi) * sin(theta / 2)", " exp(1j * lambda_angle + 1j * phi) * cos(theta / 2)"]    
])

# Define projection operator |0><0|
P0x0 = np.array([
    [1, 0],
    [0, 0]
])

# Define projection operator |1><1|
P1x1 = np.array([
    [0, 0],
    [0, 1]
])

KNOWN_GATES = {
    "I": I,
    "X": X,
    "Y": Y,
    "Z": Z,
    "H": H,
    "U3": U3,
    "P0": P0x0,
    "P1": P1x1
}
