import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import argparse

def zipf_law(rank, a, b, c):
    return c / (rank + b) ** a

def read_data_from_file(file_path):
    """
    Reads data from a specified file. The file is expected to have a format where each line contains
    a frequency and a word, separated by a comma, followed by an empty line and a word count summary.
    """
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            # Skip empty lines or lines starting with a dash (word count summary)
            if line.strip() == '' or line.startswith('---'):
                continue
            parts = line.split(',')
            if len(parts) == 2:
                rank = len(data) + 1
                frequency = int(parts[0].strip())
                data.append((rank, frequency))
    
    return data

def main():
    parser = argparse.ArgumentParser(description='Fit Zipf’s Law to word frequency data.')
    parser.add_argument('file', type=str, help='The path to the input file containing word frequency data.')
    
    args = parser.parse_args()
    file_path = args.file

    # Read data from the file
    data = read_data_from_file(file_path)
    
    # Convert data into numpy arrays
    rank = np.array([d[0] for d in data])
    frequency = np.array([d[1] for d in data])

    # Perform curve fitting to find the best values of a, b, c
    # Add bounds to ensure b stays positive and avoid invalid values
    # params, _ = curve_fit(zipf_law, rank, frequency, p0=[1.0, 1.0, 1000], bounds=([0, 0, 0], [5, 100, 100000]))
    params, _ = curve_fit(zipf_law, rank, frequency, p0=[0.6774311104374595, 3.8780010055037454e-20, 99999.99999990955], bounds=([0, 0, 0], [5, 100, 1000000]))


    # Extract the fitted parameters
    a, b, c = params
    print(f"Fitted parameters: a={a}, b={b}, c={c}")
    # params = (0.68, 3, 99999.99999976926)
    params = (a, b, c)

    # Plotting the actual data
    plt.scatter(rank, frequency, label='Data')

    # Generate fitted frequencies based on the model
    fitted_frequency = zipf_law(rank, *params)

    # Plot the fitted curve
    plt.plot(rank, fitted_frequency, color='red', label='Fitted power law')

    # Set the plot to log-log scale
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Rank')
    plt.ylabel('Frequency')
    plt.legend()
    plt.title('Zipf’s Law Fitting')

    # Save the plot to a file instead of showing it interactively
    plt.savefig('zipf_law_fit.png')
    print("Plot saved as 'zipf_law_fit.png'.")

if __name__ == "__main__":
    main()
