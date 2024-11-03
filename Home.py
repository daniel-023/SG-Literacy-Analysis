import streamlit as st
import pandas as pd
import plotly.express as px


# Page config
st.set_page_config(
    page_title="Language Literacy Analysis",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_data
def load_data():
    return pd.read_csv('data/processed_data.csv')

df = load_data()


st.title("Language Literacy Analysis in Singapore")

with st.expander("About the Data"):
    st.markdown("""
        **Source:**  
        [Census of Population 2020: Language Literacy by Qualification and Sex](https://www.singstat.gov.sg/publications/reference/cop2020/cop2020-sr1)
        
        **Population Coverage:**
        
        Singapore residents aged 15 years and over
        
        **Variables:**      
        `Language Literacy`
        `Qualification`
        `Gender`
        `Count`
    """)


st.header("Key Metrics")

# Calculate key metrics 
total_population = df['Count'].sum()
literacy_rate = (
    df[df['Language Literacy'] != 'Not Literate']['Count'].sum() / 
    total_population * 100
)
multilingual_rate = (
    df[df['num_languages'].isin([2, 3])]['Count'].sum() / 
    total_population * 100
)
english_speakers = df[df['eng_speaker'] == 1]['Count'].sum() / total_population * 100

# Display metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Population", f"{total_population:,.0f}")
with col2:
    st.metric("Literacy Rate", f"{literacy_rate:.1f}%")
with col3:
    st.metric("Multilingual Rate", f"{multilingual_rate:.1f}%")
with col4:
    st.metric("English Speakers", f"{english_speakers:.1f}%")


st.header("Overview")

qualification_order = ['No Qualification', 'Primary', 'Lower Secondary', 'Secondary', 'Post-Secondary (Non-Tertiary)', 'Polytechnic Diploma', 'Professional Qualification and Other Diploma', 'University']
df['Qualification'] = pd.Categorical(df['Qualification'], categories=qualification_order, ordered=True)

col1, col2 = st.columns(2)

with col1:
    edu_dist = df.groupby(['Qualification', 'Gender'])['Count'].sum().reset_index()
    fig1 = px.bar(
        edu_dist,
        x='Qualification',
        y='Count',
        title='Population by Gender and Education Level',
        color='Gender',
        barmode='stack'  
    )
    fig1.update_xaxes(tickangle=45, categoryorder="array", categoryarray=qualification_order)
    fig1.update_layout(showlegend=True)  
    st.plotly_chart(fig1, use_container_width=True)


with col2:
    lang_dist = df.groupby(['Qualification', 'num_languages'])['Count'].sum().reset_index()
    fig2 = px.line(
        lang_dist,
        x='Qualification', 
        y='Count',         
        color='num_languages', 
        title='Language Proficiency by Education Level',
        markers=True  
    )
    fig2.update_xaxes(tickangle=45, categoryorder="array", categoryarray=qualification_order)
    st.plotly_chart(fig2, use_container_width=True)


st.header('Data Preview')
# Add filters in columns
col1, col2 = st.columns(2)
with col1:
    selected_gender = st.selectbox(
        "Filter by Gender",
        ["All"] + list(df['Gender'].unique())
    )
with col2:
    selected_qual = st.selectbox(
        "Filter by Qualification",
        ["All"] + list(df['Qualification'].unique())
    )


# Filter data based on selections
preview_df = df.copy()
if selected_gender != "All":
    preview_df = preview_df[preview_df['Gender'] == selected_gender]
if selected_qual != "All":
    preview_df = preview_df[preview_df['Qualification'] == selected_qual]

# Display data with pagination
st.dataframe(
    preview_df,
    use_container_width=True,
    height=250
)

# Show dimensions
st.caption(f"Displayed data shape: {preview_df.shape[0]} rows × {preview_df.shape[1]} columns")


st.download_button(
label="Download Data as CSV",
data=df.to_csv(index=False).encode('utf-8'),
file_name='language_literacy_data.csv',
mime='text/csv'
)