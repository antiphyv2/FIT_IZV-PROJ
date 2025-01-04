#!/usr/bin/env python3.12
# coding=utf-8
# Author: Samuel Hejnicek, xhejni00

from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df_animals = df.copy()
    df_animals = df_animals[df_animals['p8a'] > 0]
    return df_animals


def plot_animal_hours(df: pd.DataFrame):
    
    # Create a copy of the dataframe to avoid SettingWithCopyWarning
    plotDf = df.copy()

    # Filter out non wild animal types
    plotDf = plotDf[plotDf['p8a'] < 13]

    # Filter out invalid hours (hour 25 found in the dataset)
    plotDf = plotDf[plotDf['p2b'] < 2359]

    # Extract hours from the time column
    plotDf['time'] = plotDf['p2b'].apply(lambda t: f'{t:04d}'[:2])

    # Convert the time column to an integer
    plotDf.loc[:, 'time'] = plotDf['time'].astype(int)

    # Calculate count of accidents for each hour
    count_data = plotDf.groupby('time').size().reset_index(name='count')

    # Create a color palette
    palette = sns.color_palette("muted", len(count_data))

    # Use a barplot to visualize the data
    sns.barplot(data=count_data, x='time', y='count', color=palette[0]) #, palette='viridis', hue='count')

    # Set the title of the plot
    plt.title('Počet nehod způsobených zvířaty v denních hodinách')

    # Set the labels for x and y axis
    plt.xlabel('Hodina')
    plt.ylabel('Počet nehod')

    # Save the figure
    plt.savefig('fig1.png')


def plot_animal_type(df: pd.DataFrame):

    plotDf = df.copy()

    plotDf = plotDf[plotDf['p8a'] < 13]

    wild_animal_map = {
        1: "srnec",
        2: "jiná zvěř",
        3: "jiná zvěř",
        4: "jiná zvěř",
        5: "zajíc",
        6: "jiná zvěř",
        7: "divoké prase",
        8: "jiná zvěř",
        9: "jiná zvěř",
        10: "jiná zvěř",
        11: "jiná zvěř",
        12: "jiná zvěř",
    }

    # Map the animal type to the dataframe's new column
    plotDf['animalType'] = plotDf['p8a'].map(wild_animal_map)

    # Count occurrences of each accident type
    accident_counts = plotDf["animalType"].value_counts()

    # Create a palette
    palette = sns.color_palette("muted", len(accident_counts))

    # Plot the pie chart
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        accident_counts,
        labels=accident_counts.index,
        autopct='%1.1f%%',
        startangle=20,
        labeldistance=1.1,  # Move labels further from the center
        wedgeprops={'edgecolor': 'black'},  # Add edge color to wedges
        colors=palette
    )

    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.axis('equal')


    # Set the title of the plot
    plt.title('Nehody dle typu divokého zvířete')

    # Save the figure
    plt.savefig("fig2.png")



def compute_data(df_accidents: pd.DataFrame, df_consequences: pd.DataFrame) -> pd.DataFrame:

    df_animals = filter_dataframe(df_accidents)

    # Print number of accidens
    print(f'Celkový počet nehod za uplynulé 2 roky: {len(df_accidents)}')

    # Percentage of accidents where animals were involved
    print(f'Procento nehod se zvířaty: {len(df_animals) / len(df_accidents) * 100:.2f}%')

    # Percentage of accidents caused by wild animals
    print(f'Procento nehod způsobených divokými zvířaty: {round(len(df_animals[df_animals["p8a"] < 13]) / len(df_animals) * 100)}%')

    roadMap = {
        0: "dálnice",
        1: "silnice 1. třídy",
        2: "silnice 2. třídy",
        3: "silnice 3. třídy",
        4: "uzel (křižovatka)",
        5: "komunikace sledovaná",
        6: "komunikace místní",
        7: "komunikace účelová (polní/lesní)",
        8: "komunikace účelová (ostatní)"
    }

    animal_map = {
        1: "srna/srnec",
        2: "jelen/laň",
        3: "daněk",
        4: "muflon",
        5: "zajíc",
        6: "bažant",
        7: "divoké prase",
        8: "liška",
        9: "sob",
        10: "vlk",
        11: "medvěd",
        12: "jiná zvěř",
        13: "vepř",
        14: "kráva, tele",
        15: "kůň",
        16: "koza",
        17: "ovce",
        18: "pes",
        19: "kočka",
        20: "slepice, kohout",
        21: "kachna, husa",
        22: "jiné zvíře",
    }

    visibilityMap = {
        1: "ve dne",
        2: "ve dne",
        3: "ve dne",
        4: "v noci",
        5: "v noci",
        6: "v noci",
        7: "v noci",
    }

    roadDirectionMap = {
        1: "přímý úsek",
        2: "přímý úsek",
        3: "zatáčka",
        4: "křižovatka",
        5: "křižovatka",
        6: "křižovatka",
        7: "kruhový objezd",
    }    

    # Map the road type to the dataframe new column
    df_animals['roadType'] = df_animals['p36'].map(roadMap)

    # Map the visibility to the dataframe new column
    df_animals['visibility'] = df_animals['p19'].map(visibilityMap)

    # Map the animal type to the dataframe new column
    df_animals['animalType'] = df_animals['p8a'].map(animal_map)

    # Map the road direction to the dataframe new column
    df_animals['roadDirection'] = df_animals['p28'].map(roadDirectionMap)

    # Print most common roadDirection
    print(f'Nejčastější směr vozovky při nehodě se zvířetem: {df_animals["roadDirection"].value_counts().idxmax()}')

    # Print percentage of accidents in most common roadDirection
    print(f'Procento nehod ve nejčastějším směru vozovky: {int(round(df_animals["roadDirection"].value_counts().max() / len(df_animals) * 100))}%')


    # Create a table with aggregated data
    table = df_animals.groupby('roadType').agg(
        road_accident_counts = ('roadType', 'size'),
        dominant_animal = ('animalType', lambda x: x.value_counts().idxmax()),
        dominant_animal_percentage = ('p8a', lambda x: f'{int(round(x.value_counts().max() / len(x) * 100))} %'),
        dominant_visibility = ('visibility', lambda x: x.value_counts().idxmax()),
        dominant_visibility_percentage = ('visibility', lambda x: f'{int(round(x.value_counts().max() / len(x) * 100))} %'),
    ).reset_index()

    # Rename columns for better readability
    table.rename(
        columns={
            'roadType': 'Typ vozovky',
            'road_accident_counts': 'Počet nehod',
            'dominant_animal': 'Nejčastější typ zvířete (NTZ)',
            'dominant_animal_percentage': 'Poměr nehod (NTZ)',
            'dominant_visibility': 'Nejčastější denní doba (NDD)',
            'dominant_weather': 'Nejčastější počasí',
            'dominant_visibility_percentage': 'Poměr nehod (NDD)',
        },
        inplace=True
    )
    print(table.to_string(index=False))

    return df_animals


if __name__ == "__main__":

    df_accidents = pd.read_pickle("accidents.pkl.gz")
    df_consequences = pd.read_pickle("consequences.pkl.gz")

    df_animals = compute_data(df_accidents, df_consequences)
    plot_animal_hours(df_animals)
    plot_animal_type(df_animals)