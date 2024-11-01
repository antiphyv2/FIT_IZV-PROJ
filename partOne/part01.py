#!/usr/bin/env python3
"""
IZV cast1 projektu
Autor: xhejni00

Detailni zadani projektu je v samostatnem projektu e-learningu.
Nezapomente na to, ze python soubory maji dane formatovani.

Muzete pouzit libovolnou vestavenou knihovnu a knihovny predstavene na prednasce
"""
from bs4 import BeautifulSoup
import requests
import numpy as np
from numpy.typing import NDArray
import matplotlib.pyplot as plt
from typing import List, Callable, Dict, Any


def distance(a: np.array, b: np.array) -> np.array:
    """Euclidian distance computation
    Computes the eucllidian distance with given formula:
    distance(a_i,b_i) = sqrt(sum((a_i - b_i) ** 2))

    :param a: np.array of size (n,d) where n is the number of items and d is the number of dimensions
    :param b: np.array of size (n,d) where n is the number of items and d is the number of dimensions
    :return: np.array of size (n,1) where n is the number of items
    """
    return(np.sqrt(np.sum(np.power((a-b), 2), axis=1)))


def generate_graph(a: List[float], show_figure: bool = False, save_path: str | None = None):
    """Generate graph
    Generates graph that visualises the function:
    f_a(x) = a^2 * sin(x)

    :param a: List of floats, the values of a for which the function will be generated
    :param show_figure: If true, the graph will be displayed using plt.show()
    :param save_path: If not none, the graph will be saved to the given path
    """

    #Generate x axis
    x_axe = np.linspace(0, 6 * np.pi, 10000)

    #Reshape to a column vector used for broadcasting
    reshaped_list = np.array(a).reshape(-1, 1)

    #Compute the function for every a and save to result matrix using broadcasting
    result_matrix = reshaped_list ** 2 * np.sin(x_axe)

    #Set graph size
    plt.figure(figsize=(12, 6))

    #Plot the sine graph for every function and fill the area under the appropiate curve
    for index, row in enumerate(result_matrix):
        plt.plot(x_axe, row, label=f'$y_{a[index]}(x)$')
        plt.fill_between(x_axe, row, alpha=0.1)
    
    #Set the x axis to show pi values, + 1 to include the last value
    pi_ticks = np.arange(0, 6 * np.pi + 1, step=(np.pi/2))

    #Create the pi labels
    pi_labels = []
    for index, tick in enumerate(pi_ticks):
        if index == 0:
            pi_labels.append('0')
        elif tick % np.pi == 0:
            pi_labels.append(f'{index // 2}π')
        else:
            #Latex formatting for fractions
            pi_labels.append(rf'$\frac{{{index}}}{2}π$')
    
    #Set x axies labels and the limit
    plt.xticks(pi_ticks, pi_labels)
    plt.xlim(0, 6 * np.pi)
    plt.xlabel('x')

    #Set y axis labels and the limit
    plt.ylabel('$f_{a}(x)$')

    #Set the legend to be outside the graph
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=3)

    #Plot graoh if show_figure is true
    if(show_figure):
        plt.show()

    #Save graph if save_path is not none
    if(save_path is not None):
        plt.savefig(f'{save_path}')


def generate_sinus(show_figure: bool = False, save_path: str | None = None):
    """Generate sinus
    Generates graph with three subgraphs that visualise the functions:
    f1(x) = 0.5 * cos(0.02 * π * x)
    f2(x) = 0.25 * (sin(π * x) + sin(1.5 * π * x))
    f3(x) = f1(x) + f2(x)

    :param show_figure: If true, the graph will be displayed using plt.show()
    :param save_path: If not none, the graph will be saved to the given path
    """

    """
    For Mr. Mrazek:
    In this function i tried different approach to plott the graph.
    Instead of just using plt.sth() (procedural approach) 
    I used fig and then ax_number to plot the graphs (object oriented approach).
    So I just wanted to let you know that i am not trying to mix the two approaches
    but just wanted to try both of them.
    """

    #Generate x axis
    x_axe = np.linspace(0, 100, 10000)

    #Compute all three functions
    f1 = 0.5 * np.cos(0.02 * np.pi * x_axe)
    f2 = 0.25 * (np.sin(np.pi * x_axe) + np.sin(1.5 * np.pi * x_axe))
    f3 = f1 + f2

    #Set the x and y ticks and labels for the graph
    x_ticks = np.arange(0, 101, 25)
    x_labels = ['0', '25', '50', '75', '100']
    y_ticks = np.arange(-0.8, 0.81, 0.4)
    y_labels = ['-0.8', '-0.4', '0.0', '0.4', '0.8']

    #Create three subgraohs with shared y axis
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 6), sharey=True)

    for ax in [ax1, ax2, ax3]:

        #Set x axis limit and ticks
        ax.set_xlim(0, 100)
        ax.set_xticks(x_ticks)

        #Set x axis labels just for the last subgraph
        if(ax == ax3):
            ax.set_xticklabels(x_labels)
        else:
            ax.set_xticklabels([])
        
    #Set y axis limit and ticks (shared for all subgraphs)
    ax1.set_ylim(-0.8, 0.8)
    ax1.set_yticks(y_ticks)
    ax1.set_yticklabels(y_labels)

    #Plot f1 function with y axis label
    ax1.plot(x_axe, f1, label='$f_1(t)$')
    ax1.set_ylabel('$f_1(t)$')

    #Plot f2 function with y axis label
    ax2.plot(x_axe, f2, label='$f_2(t)$')
    ax2.set_ylabel('$f_2(t)$')

    #Split f3 function to two parts
    f3_upper = np.where(f3 >= f1, f3, np.nan)
    f3_bottom = np.where(f3 < f1, f3, np.nan)

    #Plot the upper part of the f3 function in green color
    ax3.plot(x_axe, f3_upper, color='green', label='f3 >= f1')

    #Plot the bottom part of the f3 function in red and orange color based on the x value
    ax3.plot(x_axe[x_axe < 50], f3_bottom[x_axe < 50], color='red', label='f3 < f1 and (x < 50)')
    ax3.plot(x_axe[x_axe >= 50], f3_bottom[x_axe >= 50], color='orange', label='f3 < f1 and (x >= 50)')

    #Set y axis label for the last subgraph
    ax3.set_ylabel('$f_1(t) + f_2(t)$')

    #Plot graoh if show_figure is true
    if(show_figure):
        plt.show()

    #Save graph if save_path is not none
    if(save_path is not None):
        plt.savefig(f'{save_path}')


def download_data() -> Dict[str, List[Any]]:

    #URL obtained from manually digging through the website
    url = 'https://ehw.fit.vutbr.cz/izv/st_zemepis_cz'
    page = requests.get(url)
    page.encoding = 'utf-8'

    #Parse the page using BeautifulSoup and utf-8 encoding
    soup = BeautifulSoup(page.text, 'html.parser')

    #Define the dictionary that will hold the data
    dict = {
        'positions': [],
        'lats': [],
        'longs': [],
        'heights': []
    }
    
    #Find all rows with class nezvyraznit (that matches row with the station data)
    stations = soup.find_all(class_='nezvyraznit')

    #Iterate through all stations (rows)
    for station in stations:

        #Obtain all td elements in the station row (that matches the specific station data)
        td_elements = station.find_all('td')

        #Station position is in strong tag
        dict['positions'].append(station.strong.text)

        """
        Extract the latitude, longitude and height from the td elements
        Commas are replaced with dots and the last character is removed (degree symbol)
        """
        dict['lats'].append(float(td_elements[2].text.replace(',', '.')[:-1]))
        dict['longs'].append(float(td_elements[4].text.replace(',', '.')[:-1]))
        dict['heights'].append(float(td_elements[6].text.replace(',', '.')))

    return dict

if __name__ == "__main__":
    distance(np.array([[-1, -1, -1], [0, 1, 2], [3, -3, 1], [-2, -2, 0], [4, 5, 6]]), np.array([[1, 1, 1], [0, 0, 0], [3, 3, 3], [-2, 1, 2], [0, 0, 0]]))
    generate_graph([7,4,3], False, 'cs.png')
    # generate_sinus()
    # download_data()
