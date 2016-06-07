#!/usr/bin/env python

'''
This script takes raw data from the AIT scanning 4pp system, UoL
and generates a coloured contour plot of sheet resistance.
Note that the colour scale is logarithmic.

To use: $ python rs_colour.py [path-to-file]
'''
# R. Treharne, 30th March 2016

import matplotlib.pyplot as plt
from matplotlib.mlab import griddata
import numpy as np
import csv
import sys
import os


def get_data(path):

    f = open(path, 'rb')
    reader = csv.reader(f)
    headers = reader.next()
    
    data = []
    error_list = ['Error', 'OverRange']
    for line in reader:
        if not any([i in line for i in error_list]):
            data.append(line)

    try:
        data = [[float(y) for y in x] for x in np.transpose(data)]
    except ValueError:
        return data

    return data

def format_data(data):
    x = data[0]
    y = data[1]
    z = (np.log10(np.array(data[2])*4.532))
    #z = (data[2])

    xi = np.linspace(min(x), max(x), 100)
    yi = np.linspace(min(y), max(y), 100)

    zi = griddata(x, y, z, xi, yi)

    return xi, yi, zi

def plot_contour(x, y, z):
    fig = plt.figure(figsize=(9,7))
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')

    S = ax.contour(x, y, z, 10, colors='k')
    CF = ax.contourf(x, y, z, 50, cmap='gist_rainbow')
    ax.clabel(S, fontsize=15, fmt='%1.1f')
    ax.set_xlabel('x (mm)', fontsize=25)
    ax.set_ylabel('y (mm)', fontsize=25)
    ax.tick_params(labelsize=15)
    

    CB = plt.colorbar(CF)
    CB.set_label('$\log_{10}(R_{S}$ $[\Omega/sq])$', fontsize=25)
    CB.ax.tick_params(labelsize=15)
    
    

if __name__ == "__main__":
    filename = sys.argv[1]
    d = get_data(filename)
    x, y, z = format_data(d)
    plot = plot_contour(x, y, z)
    plt.show()


