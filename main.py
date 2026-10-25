import pandas as pd
import numpy as np
from pathlib import Path

def importdata():
#Imports the datasets and turns them into dataframes

  current_dir = Path(__file__).parent
  csv_path2020 = current_dir / "2020NeighborhoodData.csv"
  csv_path2018_2021 = current_dir / "2018_2021Neighborhood.csv"

  df2020 = pd.read_csv(csv_path2020)
  df2018_2020 = pd.read_csv(csv_path2018_2021)
  return df2018_2020
df2018_2021 = importdata()

def clean_data(df2018_2021):
#Cleans the dataframes by removing unnecessary columns and renaming columns for merging
  #df2020 = df2020.drop(columns=['Borough', 'CD', 'Join', 'Perc_White', 'Perc_Hispanic', 'Perc_Black','Perc_Asian', 'GoalName', 'GoalFullName', 'GoalRank','ScoreRank', 'Ind3', 'Ind3Outcome',
               #'Ind3Rank', 'Ind3Definition', 'Ind4', 'Ind4Outcome', 'Ind4Rank',
               #'Ind4Definition', 'Ind5', 'Ind5Outcome', 'Ind5Rank', 'Ind5Definition',
               #'Ind6', 'Ind6Outcome', 'Ind6Rank', 'Ind6Definition', 'Ind7',
               #'Ind7Outcome', 'Ind7Rank', 'Ind7Definition', 'Ind8', 'Ind8Outcome',
               #'Ind8Rank', 'Ind8Definition'])
  df2018_2021 = df2018_2021.drop(columns=['Borough', 'CD', 'Join', 'Perc_White', 'Perc_Hispanic', 'Perc_Black','Perc_Asian', 'GoalName', 'GoalFullName', 'GoalRank','ScoreRank', 'Ind3', 'Ind3Outcome',
               'Ind3Rank', 'Ind3Definition', 'Ind4', 'Ind4Outcome', 'Ind4Rank',
               'Ind4Definition', 'Ind5', 'Ind5Outcome', 'Ind5Rank', 'Ind5Definition',
               'Ind6', 'Ind6Outcome', 'Ind6Rank', 'Ind6Definition', 'Ind7',
               'Ind7Outcome', 'Ind7Rank', 'Ind7Definition', 'Ind8', 'Ind8Outcome',
               'Ind8Rank', 'Ind8Definition']) 
  #All left is (['Year Published', 'PUMA', 'Neighborhoods', 'NYC_Poverty_Rate',
 #      'Median_Income', 'Perc_Other', 'Goal', 'TotalOutcome', 'IndexScore',
 #      'Ind1', 'Ind1Outcome', 'Ind1Rank', 'Ind1Definition', 'Ind2',
 #      'Ind2Outcome', 'Ind2Rank', 'Ind2Definition'],


#We need poverty rates, scores, and ranks to be in integer or float.
#We need Year to be a datetime object as well.

#We also want to sort it my neighborhood, AKA PUMA. I don't think we need to convert the puma to integer since it is a code and not a number.
  #df2020 = df2020.sort_values(by='PUMA')
  df2018_2021 = df2018_2021.sort_values(by='PUMA')

  return df2018_2021
df2018_2021 = clean_data(df2018_2021)

def splitdata(df2018_2021):
 #Splits the 2018 & 2021 dataframe into two
  df2018 = df2018_2021[df2018_2021['Year'] == 2018]
  df2021 = df2018_2021[df2018_2021['Year'] == 2021]
  return df2018, df2021
df2018, df2021 = splitdata(df2018_2021)

def dropdupes(df2018, df2021):
#Drops duplicate rows in the dataframes
  df2018 = df2018.drop_duplicates(subset=['PUMA'], keep='first')
  #df2020 = df2020.drop_duplicates(subset=['PUMA'], keep='first')
  df2021 = df2021.drop_duplicates(subset=['PUMA'], keep='first')
  return df2018, df2021
df2018, df2021 = dropdupes(df2018, df2021)


def improved_data(df2018, df2021):
#checks for improvements of poverty rate and median salary, listing rate of change.
  imp_df = pd.DataFrame(df2021['PUMA'])
  list = ['NYC_Poverty_Rate', 'Median_Income']

#Calculate the change in the poverty rate by looping through all entries on both dataframes getting the difference, Then we make a seperate list to save the output and then we append that list to a new dataframe. We repeat this for the median income as well. Then we rename the columns to show that they are the difference.
  for column in list:
    diff = [] 

    for i in range(len(df2018)):
      result = df2021[column].iloc[i].astype(float) - df2018[column].iloc[i].astype(float)
      diff.append(result)     
    imp_df[column] = diff

  imp_df = imp_df.rename(columns={'NYC_Poverty_Rate': 'Poverty_Rate_Change', 'Median_Income': 'Income_Rate_Change'})
  return imp_df
imp_df = improved_data(df2018, df2021)

def ranked_data(imp_df):
#Organizes data ranking by most improved and giving highest and lowest poverty rate and rate of change.
  return data_ranks

def success(df2018, df2020, df2021, imp_df):
#analyzes index and indicator scores to check for success
  #Succes for goal achievements is a high OR growing index score
  #Success for specific goal indicators is high OR gorwing idicator score

  #We want to see if these solutions are working, we will organize them to see which goals have deemed successful and which haven't found much success. 
  #*We will find a problem since some goals have less indicators than others which shows as blank space or NA.*

  #Still not sure what output might look like.
  return success_df#???





