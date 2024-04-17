import pandas as pd
import streamlit as st
import plotly.express as px

# Load data
path = "D:\\OneDrive\\energia_lab\\data\\"
df1 = pd.read_csv(path + 'projetos-eficiencia-energetica-empresa-geocoded.csv')
df2 = pd.read_csv(path + 'aggregated_scores.csv')
df3 = pd.read_csv(path + 'grouped_df.csv')
df4 = pd.read_csv(path + 'sorted_tipologia_summary.csv')

# Sort the dataframe in descending order and get the top 10
df2_sorted = df2.sort_values('Score', ascending=False).head(10)

# Create a bar chart with Plotly
fig = px.bar(df2_sorted, x='NomAgente', y='Score', title='Top 10 Agent Scores')

# Sort bars in descending order
fig.update_layout(xaxis={'categoryorder':'total descending'})

# Display the chart in Streamlit
st.plotly_chart(fig)

# Convert 'DatInicioProjeto' and 'DatConclusaoProjeto' to datetime
df3['DatInicioProjeto'] = pd.to_datetime(df3['DatInicioProjeto'])
df3['DatConclusaoProjeto'] = pd.to_datetime(df3['DatConclusaoProjeto'])

# Calculate project duration in days
df3['ProjectDurationDays'] = (df3['DatConclusaoProjeto'] - df3['DatInicioProjeto']).dt.days

# Calculate the average project duration in years
average_project_duration_years = df3['ProjectDurationDays'].mean() / 365.25

# Display the average project duration
st.metric(label="Average Project Duration (years)", value=round(average_project_duration_years, 1))





