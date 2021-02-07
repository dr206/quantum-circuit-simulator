import numpy as np

from .utils import log2

def measure_all(state_vector):
    """ Select a single binary index at random from the state vector.
    
    Using a weighted random selection, select a single element from state_vector and convert
    the numeric index of the selection to a binary string.

    Args:
        state_vector: a list of probability amplitudes

    Returns:
        a single binary index as a string

        For the state
            [0.70710678, 0, 0, -0.70710678]
        either of the following two options may be returned:
            '00'
        or
            '11'
    """

    def get_probability(amplitude):
        pa = np.abs(amplitude)**2
        return pa

    # create probability distribution based on the state vectors amplitudes 
    probabilities = np.fromiter((get_probability(amplitude) for amplitude in state_vector), state_vector.dtype) 

    # select a single state randonly based on a probability distribution
    # mark the resulting index for this state with a 1 
    result_array = np.random.multinomial(1, probabilities)

    # filter for the indices of all selected states (in our case there is only one such state)
    indices = np.where(result_array == 1)
    index = indices[0][0]

    # covert the numeric index into a binary string, whose length equals the number of qubits
    bin_index = bin(index)[2:].zfill(log2(len(state_vector)))

    return bin_index

def get_counts(state_vector, num_shots):
    """ Select a single binary index at random from the state vector.
    
    Using a weighted random selection, select a single element from state_vector and convert
    the numeric index of the selection to a binary string.

    Args:
        state_vector: the input state vector to be measured
        num_shots: the number of times to perform a measurement

    Returns:
        the measurement statistics of only the states that were measured

        For 1,000 measurement of the example state:
            [0.70710678, 0, 0, -0.70710678]
        the statistics can look like
            {
                "00": 485,
                "11": 515
            }
            
        Note that states '01' and '10' are not included here,
        as they are not measurement outcomes for the example state.
        
        Due to the probabilistic nature of quantum measurement,
        this example state will not produce a perfect 50/50 split of possible outcomes after measurement.

        In the limit as num_shots tends to infinity,
        the statistics of the measurement for this example state will approach a 50/50 split.
    """

    # initialise an empty dictionary to hold the count of outcomes for each of the measurements
    counts = {} 
    for x in range(num_shots):

        index = measure_all(state_vector)

        # increment the count for the index'th state
        # counts are initialised to zero
        # only the counts returned in a measurememt are included
        counts[index] = counts.get(index, 0) + 1
    
    # sort dictionary by keys to present data in the expected format
    sorted_counts = dict(sorted(counts.items()))

    return sorted_counts
