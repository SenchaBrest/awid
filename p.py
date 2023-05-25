import numpy as np

def convert_to_dat(filename, *lists):
    data = np.column_stack(lists)
    np.savetxt(filename, data, fmt='%f')

# Example usage
person = [1.5, 2.3, 1.7, 3.2]
bicycle = [0.8, 1.2, 1.5, 0.9]
car = [5.6, 4.3, 6.1, 5.9]

convert_to_dat('data.dat', person, bicycle, car)
