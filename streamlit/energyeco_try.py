import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Load data
path1 = r"D:\OneDrive\energia_lab\data\\"
path2 = r"D:\OneDrive\energia_lab\streamlit\\"
df1 = pd.read_csv(path1+'projetos-eficiencia-energetica-empresa-geocoded.csv')
df2 = pd.read_csv(path1+'aggregated_scores.csv')

try:
    df1 = pd.read_csv(df1)
    df2 = pd.read_csv(df2)
    
    # Sort the dataframe in descending order by 'Score' and select top 10
    df2_sorted = df2.sort_values('Score', ascending=False).head(10)
    
    # Set 'NomAgente' as the index and keep only the 'Score' column
    df2_sorted = df2_sorted.set_index('NomAgente')[['Score']]
    
    # Creating a color map based on scores
    # Map scores to a color gradient from red (high scores) to blue (low scores)
    max_score = df2_sorted['Score'].max()
    min_score = df2_sorted['Score'].min()
    colors = [plt.cm.viridis((score - min_score) / (max_score - min_score)) for score in df2_sorted['Score']]
    
    # Display the title
    st.markdown("# Top 10 Companies in Project Energy Efficiency Score")
    
    # Using matplotlib for plotting to handle custom label rotation and color mapping
    fig, ax = plt.subplots()
    bars = ax.barh(df2_sorted.index, df2_sorted['Score'], color=colors)
    ax.set_xlabel("Scores")
    ax.set_title("Top 10 Companies by Energy Efficiency Score")
    plt.xticks(rotation=45)
    st.pyplot(fig)
except FileNotFoundError:
    st.error(f"Failed to load data. Please check that the files exist at the specified paths.")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
