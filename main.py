import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')
print(df.info())

df['BMI'] = df['weight'] / (df['height'] / 100)**2

# Add 'overweight' column
df['overweight'] = np.where(df['BMI'] >25, 1, 0)
print(df.head())
#normilization. 0 is good, 1 is bad 
#collestroal collumn 1 --> 0, 2||3 --> 1
df.loc[df['cholesterol'] == 1, 'cholesterol'] = 0 #the second cholesterol is the name of the new column
df.loc[df['cholesterol'] >1, 'cholesterol'] = 1

#glucose column 1--> 0, 2||3 --> 1
df.loc[df['gluc'] == 1, 'gluc'] = 0
df.loc[df['gluc'] > 1, 'gluc'] = 1

print(df['cholesterol'])
print(df['gluc'])

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.


# Function to draw Categorical Plot
def draw_cat_plot():
  # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
  df_cat = pd.melt(df, id_vars='cardio', value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

  # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
  df_cat['total']=0
  df_cat = df_cat.groupby(['cardio','variable','value'], as_index=False).count()
  print(df_cat)

  # Draw the catplot with 'sns.catplot()'
  plot = sns.catplot(x='variable', y='total', data=df_cat, hue='value', kind='bar', col='cardio')
  # Get the figure for the output
  fig = plot.figure

  # Do not modify the next two lines
  fig.savefig('catplot.png')
  return fig


# Function to draw Heat Map
def draw_heat_map():
  # Clean the data
  # leave out patients where their diastolic (resting) is higher than their systolic pressure
  df_heat = df[df['ap_lo'] <= df['ap_hi']]
  #leave out "extreme values" by using extreme values
  df_heat = df_heat[df['height'] >= df['height'].quantile(0.025)] 
  df_heat = df_heat[df['height'] <= (df['height'].quantile(0.975))]
  
  df_heat = df_heat[df['weight'] >= df['weight'].quantile(0.025)] 
  df_heat = df_heat[df['weight'] <= (df['weight'].quantile(0.975))]
  # Calculate the correlation matrix
  corr = df_heat.corr()

  # Generate a mask for the upper triangle
  mask = np.triu(corr)

  # Set up the matplotlib figure
  fig, ax = plt.subplots(figsize=(16, 16))

  # Draw the heatmap with 'sns.heatmap()'
  sns.heatmap(corr, mask=mask, annot=True, fmt='.2f',)
  # Do not modify the next two lines
  fig.savefig('heatmap.pdf')
  return fig


# RUN FUNCTIONS
draw_cat_plot()
draw_heat_map()

