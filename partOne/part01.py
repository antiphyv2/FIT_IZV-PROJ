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
    x_axe = np.linspace(0, 6 * np.pi, 1000)
    reshaped_list = np.array(a).reshape(-1, 1)
    result_matrix = reshaped_list ** 2 * np.sin(x_axe)

    
    plt.figure(figsize=(12, 6))
    for index, row in enumerate(result_matrix):
        plt.plot(x_axe, row, label=f'$y_{a[index]}(x)$')
        plt.fill_between(x_axe, row, alpha=0.1)
    
    pi_ticks = np.arange(0, 6 * np.pi + 1, step=(np.pi/2))
    pi_labels = ['0', r'$\frac{1}{2}π$', 'π', r'$\frac{3}{2}π$', '2π', r'$\frac{5}{2}π$', '3π', r'$\frac{7}{2}π$', '4π', r'$\frac{9}{2}π$', '5π', r'$\frac{11}{2}π$', '6π']
    plt.xticks(pi_ticks, pi_labels)
    plt.xlim(0, 6 * np.pi)
    plt.xlabel('x')
    plt.ylabel('$f_{a}(x)$')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=3)

    if(show_figure):
        plt.show()

    if(save_path is not None):
        plt.savefig(f'{save_path}')
    



def generate_sinus(show_figure: bool = False, save_path: str | None = None):
    x_axe = np.linspace(0, 100, 10000)
    f1 = 0.5 * np.cos(0.02 * np.pi * x_axe)
    f2 = 0.25 * (np.sin(np.pi * x_axe) + np.sin(1.5 * np.pi * x_axe))
    f3 = f1 + f2

    x_ticks = np.arange(0, 101, 25)
    x_labels = ['0', '25', '50', '75', '100']
    y_ticks = np.arange(-0.8, 0.81, 0.4)
    y_labels = ['-0.8', '-0.4', '0.0', '0.4', '0.8']

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 6), sharey=True)

    for ax in [ax1, ax2, ax3]:
        ax.set_xlim(0, 100)
        ax.set_xticks(x_ticks)
        if(ax == ax3):
            ax.set_xticklabels(x_labels)
        else:
            ax.set_xticklabels([])
        
        
    ax1.set_ylim(-0.8, 0.8)
    ax1.set_yticks(y_ticks)
    ax1.set_yticklabels(y_labels)

    ax1.plot(x_axe, f1, label='$f_1(t)$')
    ax2.plot(x_axe, f2, label='$f_2(t)$')

    # greater = np.ma.masked_where(f3 < f1, f3)
    # lower = np.ma.masked_where(f3 >= f1, f3)
    # middle_right = np.ma.masked_where(x_axe < 50, lower)
    # midle_left = np.ma.masked_where(x_axe >= 50, lower)


    # ax3.plot(x_axe, greater, color='green', label='$f_1(t) + f_2(t)$')
    # ax3.plot(x_axe, middle_right, color='orange')
    # ax3.plot(x_axe, midle_left, color='red')

    f3_upper = np.where(f3 >= f1, f3, np.nan)
    f3_bottom = np.where(f3 < f1, f3, np.nan)

    ax3.plot(x_axe, f3_upper, color='green', label='f3 >= f1')
    ax3.plot(x_axe[x_axe < 50], f3_bottom[x_axe < 50], color='red', label='f3 < f1 and (x < 50)')
    ax3.plot(x_axe[x_axe >= 50], f3_bottom[x_axe >= 50], color='orange', label='f3 < f1 and (x >= 50)')

    if(show_figure):
        plt.show()

    if(save_path is not None):
        plt.savefig(f'{save_path}')


def download_data() -> Dict[str, List[Any]]:
    url = 'https://ehw.fit.vutbr.cz/izv/st_zemepis_cz'
    page = requests.get(url)
    page.encoding = 'utf-8'
    soup = BeautifulSoup(page.text, 'html.parser')

    dict = {
        'positions': [],
        'lats': [],
        'longs': [],
        'heights': []
    }
    
    stations = soup.find_all(class_='nezvyraznit')
    for station in stations:
        td_elements = station.find_all('td')
        dict['positions'].append(station.strong.text)
        dict['lats'].append(float(td_elements[2].text.replace(',', '.')[:-1]))
        dict['longs'].append(float(td_elements[4].text.replace(',', '.')[:-1]))
        dict['heights'].append(float(td_elements[6].text.replace(',', '.')))

    return dict

if __name__ == "__main__":
    distance(np.array([[-1, -1, -1], [0, 1, 2], [3, -3, 1], [-2, -2, 0], [4, 5, 6]]), np.array([[1, 1, 1], [0, 0, 0], [3, 3, 3], [-2, 1, 2], [0, 0, 0]]))
    generate_graph([7, 4, 3])
    generate_sinus()
    download_data()
