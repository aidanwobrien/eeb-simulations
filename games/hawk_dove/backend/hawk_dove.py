import matplotlib.pyplot as plt
import random

def hawk_dove_payoff(a, b, value, cost):
    if a == "hawk" and b == "hawk":
        return (value - cost) / 2
    if a == "hawk" and b == "dove":
        return value
    if a == "dove" and b == "hawk":
        return 0
    if a == "dove" and b == "dove":
        return value / 2
    
