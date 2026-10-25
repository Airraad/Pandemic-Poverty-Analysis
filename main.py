import pandas as pd
import numpy as np
from pathlib import Path

def importdata():
#Imports the datasets and turns them into dataframes

  current_dir = Path(__file__).parent
  csv_path2020 = current_dir / "2020NeighborhoodData.csv"
  csv_path2018_2020 = current_dir / "2018&2020NeighborhoodData.csv"

  df2020 = pd.read_csv(csv_path2020)
  df2018_2020 = pd.read_csv(2018_2020)
  return df2020, df2018_2020
df2020, df2018_2021 = importdata()

def clean_data(df2020, df2018_2021):
#Cleans the dataframes by removing unnecessary columns and renaming columns for merging
  df2020 = df2020.drop(columns=['Borough', 'CD', 'Join', 'Perc_White', 'Perc_Hispanic', 'Perc_Black','Perc_Asian', 'GoalName', 'GoalFullName', 'GoalRank','ScoreRank'])
  df2018_2021 = df2018_2021.drop(columns=['Borough', 'CD', 'Join', 'Perc_White', 'Perc_Hispanic', 'Perc_Black','Perc_Asian', 'GoalID', 'GoalName', 'GoalFullName', 'GoalRank','ScoreRank'])
  #All left is year, puma, neighborhood, indicator, indicator name, score, and index score.
  return df2020, df2018_2021
df2020, df2018_2021 = clean_data(df2020, df2018_2021)

def splitdata(df2018_2021):
 #Splits the 2018 & 2020 dataframe into two
  df2018 = df2018_2021[df2018_2021['Year'] == 2018]
  df2021 = df2018_2021[df2018_2021['Year'] == 2021]
   
  
  
  return df2018, df2021



def improved_data(merged_df):
#checks for improvements of poverty rate and median salary, listing rate of change.
  return imp_df

def ranked_data(imp_df):
#Organizes data ranking by most improved and giving highest and lowest poverty rate and rate of change.
  return data_ranks

def success(merged_df, imp_df):
#analyzes index and indicator scores to check for success
  #Succes for goal achievements is a high OR growing index score
  #Success for specific goal indicators is high OR gorwing idicator score

  #We want to see if these solutions are working, we will organize them to see which goals have deemed successful and which haven't found much success. 
  #*We will find a problem since some goals have less indicators than others which shows as blank space or NA.*

  #Still not sure what output might look like.
  return success_df#???



splitdata(df2018_2021)

print(f'{df2020.head()}')



