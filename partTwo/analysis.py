#!/usr/bin/env python3.12
# coding=utf-8

from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import zipfile
import lxml

# muzete pridat libovolnou zakladni knihovnu ci knihovnu predstavenou na prednaskach
# dalsi knihovny pak na dotaz

# Ukol 1: nacteni dat ze ZIP souboru


def load_data(filename : str, ds : str) -> pd.DataFrame:

    with zipfile.ZipFile(filename, 'r') as zipFile:

        # Obtain a list of all files in the zip archive
        fileList = zipFile.namelist()

        # Filter only files with name in db argument ending with .xls
        targetedFileNames = [file for file in fileList if file.endswith(f'{ds}.xls')]

        df = []

        # Obtain dataframe from each file and append it to the list
        for file in targetedFileNames:
            with zipFile.open(file) as f:
                df.extend(pd.read_html(f, encoding="cp1250"))


        # Concatenate all dataframes into one (ignore index for not using index values from original dataframes)
        df = pd.concat(df, ignore_index=True)

        # Drop unnamed columns containing NaN values
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        return df
# Ukol 2: zpracovani dat


def parse_data(df: pd.DataFrame, verbose: bool = False) -> pd.DataFrame:

    regionDict = {
        0: "PHA", 1: "STC", 2: "JHC", 3: "PLK",
        4: "ULK", 5: "HKK", 6: "JHM", 7: "MSK",
        14: "OLK", 15: "ZLK", 16: "VYS", 17: "PAK",
        18: "LBK", 19: "KVK"
    }

    newDf = pd.DataFrame()
    newDf["date"] = pd.to_datetime(df["p2a"], format="%d.%m.%Y")
    newDf["region"] = df["p4a"].map(regionDict)
    print(newDf)

# Ukol 3: počty nehod v jednotlivých regionech podle stavu vozovky
def plot_state(df: pd.DataFrame, fig_location: str = None,
                    show_figure: bool = False):
    pass

# Ukol4: alkohol a následky v krajích
def plot_alcohol(df: pd.DataFrame, df_consequences : pd.DataFrame, 
                 fig_location: str = None, show_figure: bool = False):
    pass

# Ukol 5: Druh nehody (srážky) v čase
def plot_type(df: pd.DataFrame, fig_location: str = None,
              show_figure: bool = False):
    pass


if __name__ == "__main__":
    # zde je ukazka pouziti, tuto cast muzete modifikovat podle libosti
    # skript nebude pri testovani pousten primo, ale budou volany konkreni
    # funkce.

    df = load_data("data_23_24.zip", "nehody")
    # print(f"Table1:\n{df}")
    # df_consequences = load_data("data_23_24.zip", "nasledky")
    # print(f"Table2:\n{df_consequences}")
    df2 = parse_data(df, True)
    
    # plot_state(df2, "01_state.png")
    # plot_alcohol(df2, df_consequences, "02_alcohol.png", True)
    # plot_type(df2, "03_type.png")

# Poznamka:
# pro to, abyste se vyhnuli castemu nacitani muzete vyuzit napr
# VS Code a oznaceni jako bunky (radek #%%% )
# Pak muzete data jednou nacist a dale ladit jednotlive funkce
# Pripadne si muzete vysledny dataframe ulozit nekam na disk (pro ladici
# ucely) a nacitat jej naparsovany z disku
