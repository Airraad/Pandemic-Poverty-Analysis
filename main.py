import pandas as pd
import numpy as np
from pathlib import Path

pd.set_option('display.max_colwidth', None)

def importdata():
#Imports the datasets and turns them into dataframes
  current_dir = Path(__file__).parent
  csv_path2018_2021 = current_dir / "2018_2021Neighborhood.csv"
  df2018_2021 = pd.read_csv(csv_path2018_2021)
  return df2018_2021
df2018_2021 = importdata()

def clean_data(df2018_2021):
#Cleans the dataframes by removing unnecessary columns and renaming columns for merging
  df2018_2021 = df2018_2021.drop(columns=[
      'Borough', 'CD', 'Join', 'Perc_White', 'Perc_Hispanic', 'Perc_Black','Perc_Asian', 
      'GoalName', 'GoalFullName', 'GoalRank','ScoreRank', 'Ind3', 'Ind3Outcome',
      'Ind3Rank', 'Ind3Definition', 'Ind4', 'Ind4Outcome', 'Ind4Rank',
      'Ind4Definition', 'Ind5', 'Ind5Outcome', 'Ind5Rank', 'Ind5Definition',
      'Ind6', 'Ind6Outcome', 'Ind6Rank', 'Ind6Definition', 'Ind7',
      'Ind7Outcome', 'Ind7Rank', 'Ind7Definition', 'Ind8', 'Ind8Outcome',
      'Ind8Rank', 'Ind8Definition'
  ]) 
  #All left is (['Year Published', 'PUMA', 'Neighborhoods', 'NYC_Poverty_Rate',
 #      'Median_Income', 'Perc_Other', 'Goal', 'TotalOutcome', 'IndexScore',
 #      'Ind1', 'Ind1Outcome', 'Ind1Rank', 'Ind1Definition', 'Ind2',
 #      'Ind2Outcome', 'Ind2Rank', 'Ind2Definition'],

#We need poverty rates, scores, and ranks to be in integer or float.
#We need Year to be a datetime object as well.

#We also want to sort it my neighborhood, AKA PUMA. I don't think we need to convert the puma to integer since it is a code and not a number.
  df2018_2021 = df2018_2021.sort_values(by=['PUMA', 'Goal'])
  return df2018_2021
df2018_2021 = clean_data(df2018_2021)

def splitdata(df2018_2021):
 #Splits the 2018 & 2021 dataframe into two
  df2018 = df2018_2021[df2018_2021['Year'] == 2018].reset_index(drop=True)
  df2021 = df2018_2021[df2018_2021['Year'] == 2021].reset_index(drop=True)
  return df2018, df2021
df2018, df2021 = splitdata(df2018_2021)

def improved_data(df2018, df2021):
#checks for improvements of poverty rate and median salary, listing rate of change.
  imp_df = pd.DataFrame()
  imp_df['PUMA'] = df2021['PUMA'].values
  imp_df['Neighborhoods'] = df2021['Neighborhoods'].values
  imp_df['Goal'] = df2021['Goal'].values 
  
#Calculate the change in the poverty rate by looping through all entries on both dataframes getting the difference, Then we make a seperate list to save the output and then we append that list to a new dataframe. We repeat this for the median income as well. Then we rename the columns to show that they are the difference.
  list = ['NYC_Poverty_Rate', 'Median_Income', 'IndexScore']
  
  for column in list:
      diff = [] 
      for i in range(len(df2018)):
          result = df2021[column].iloc[i].astype(float) - df2018[column].iloc[i].astype(float)
          diff.append(result)      
      imp_df[column] = diff

  imp_df = imp_df.rename(columns={'NYC_Poverty_Rate': 'Poverty_Rate_Change', 'Median_Income': 'Income_Rate_Change', 'IndexScore': 'IndexScore_Change'})
  return imp_df
imp_df = improved_data(df2018, df2021)

def ranked_data(imp_df):
  #Organizes data ranking by most improved and giving highest and lowest poverty rate and rate of change.
  unique_neighborhoods = imp_df.drop_duplicates(subset=['PUMA'])
  
  top_income = unique_neighborhoods.sort_values(by='Income_Rate_Change', ascending=False)
  bottom_income = unique_neighborhoods.sort_values(by='Income_Rate_Change', ascending=True)
  top_poverty = unique_neighborhoods.sort_values(by='Poverty_Rate_Change', ascending=True)
  bottom_poverty = unique_neighborhoods.sort_values(by='Poverty_Rate_Change', ascending=False)
  
  # Removed the invalid goals.df["goal", "cummalation"] line
  # Replaced .value_counts() with len() to get a single number
  # Changed 'goal' to 'Goal' and mapped to the short names since clean_data dropped GoalFullName
  goal1cummalation = len(imp_df[(imp_df['IndexScore_Change'] > 0) & (imp_df['Goal'] == "Financial Services")])
  goal2cummalation = len(imp_df[(imp_df['IndexScore_Change'] > 0) & (imp_df['Goal'] == "Goods & Services")])
  goal3cummalation = len(imp_df[(imp_df['IndexScore_Change'] > 0) & (imp_df['Goal'] == "Jobs & Income")])
  goal4cummalation = len(imp_df[(imp_df['IndexScore_Change'] > 0) & (imp_df['Goal'] == "Financial Shocks")])
  goal5cummalation = len(imp_df[(imp_df['IndexScore_Change'] > 0) & (imp_df['Goal'] == "Build Assets")])
  
  # Removed the trailing semicolons from the strings
  goallist = ["Goal 1: Access to Affordable, High-Quality Financial Services",
      "Goal 2: Access to Affordable, High-Quality Goods & Services",
      "Goal 3: Access to Quality Jobs & Income Supports",
      "Goal 4: Stable Housing & Capacity to Limit Financial Shocks",
      "Goal 5: Opportunities to Build Assets & Plan for the Future"]
      
  # Changed goals.df to goals_df (variables cannot contain periods)
  goals_df = pd.DataFrame({'goal': goallist, 'cummalation': [goal1cummalation, goal2cummalation, goal3cummalation, goal4cummalation, goal5cummalation]})
  goals_df = goals_df.sort_values(by='cummalation', ascending=False)
  
  return goals_df, top_income, bottom_income, top_poverty, bottom_poverty, unique_neighborhoods
goals_df, top_income, bottom_income, top_poverty, bottom_poverty, unique_neighborhoods = ranked_data(imp_df)

#def success(df2018, df2020, df2021, imp_df):
#analyzes index and indicator scores to check for success
  #Succes for goal achievements is a high OR growing index score
  #Success for specific goal indicators is high OR gorwing idicator score

  #We want to see if these solutions are working, we will organize them to see which goals have deemed successful and which haven't found much success. 
  #*We will find a problem since some goals have less indicators than others which shows as blank space or NA.*

  #Still not sure what output might look like.
  #return 


improving_count = len(unique_neighborhoods[(unique_neighborhoods['Poverty_Rate_Change'] < 0) & (unique_neighborhoods['Income_Rate_Change'] > 0)])

avg_pov_change = unique_neighborhoods['Poverty_Rate_Change'].mean()
avg_inc_change = unique_neighborhoods['Income_Rate_Change'].mean()

annual_pov_rate = avg_pov_change / 3
annual_inc_rate = avg_inc_change / 3

base_pov_2021 = df2021.drop_duplicates(subset=['PUMA'])['NYC_Poverty_Rate'].astype(float).mean()
base_inc_2021 = df2021.drop_duplicates(subset=['PUMA'])['Median_Income'].astype(float).mean()

proj_pov_2025 = base_pov_2021 + (annual_pov_rate * 4)
proj_inc_2025 = base_inc_2021 + (annual_inc_rate * 4)

print("Improving Neighborhoods (Poverty Down, Income Up):", improving_count)
print("\nTop 3 Income Increases:\n", top_income.head(3)[['Neighborhoods', 'Income_Rate_Change']].to_string(index=False))
print("\nBottom 3 Income Increases:\n", bottom_income.head(3)[['Neighborhoods', 'Income_Rate_Change']].to_string(index=False))
print("\nTop 3 Poverty Declines:\n", top_poverty.head(3)[['Neighborhoods', 'Poverty_Rate_Change']].to_string(index=False))
print("\nBottom 3 Poverty Declines:\n", bottom_poverty.head(3)[['Neighborhoods', 'Poverty_Rate_Change']].to_string(index=False))
print("\nAverage Poverty Change:", avg_pov_change)
print("Average Income Change:", avg_inc_change)
print("2025 Poverty Projection:", proj_pov_2025)
print("2025 Income Projection:", proj_inc_2025)
print("\nGoal Success Counts:\n", goals_df.to_string(index=False))