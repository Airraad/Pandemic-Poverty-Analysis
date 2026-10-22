import pandas as pd
import numpy as np

2020df = pd.read_csv("2020NeighborhoodData.csv")


def splitdata(2018_2020df):
  return 2018df, 2021df
#Splits the 2018 & 2020 dataframe into two


def merge_data(2020df, 2018df, 2021df):
  return merged_df
#merges the datasets by PUMA (public use microdata areas)

def improved_data(merged_df):
#checks for improvements of the index score and indicators
  return imp_df
