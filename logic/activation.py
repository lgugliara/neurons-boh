# logic/activation.py

def boolean_and(n):
    return n.potential > n.threshold
boolean_and.display_name = "AND"

def boolean_or(n):
    return n.potential > n.threshold
boolean_or.display_name = "OR"

def boolean_xor(n):
    return n.potential > n.threshold
boolean_xor.display_name = "XOR"


def apply_activation(neuron, func):
    return func(neuron)

activation_functions = [boolean_and, boolean_or, boolean_xor]