import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


st.title("Overview")

df = pd.read_csv('data/processed_data.csv')
