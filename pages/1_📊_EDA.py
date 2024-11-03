import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from Home import load_data


st.title('Exploratory Data Analysis')
df = load_data()


tab1, tab2, tab3 = st.tabs([
    "Education and Language", 
    "Language Distribution", 
    "Gender Analysis",
])


qualifications = list(df['Qualification'].unique())
literacy_rates = []
multilingual_rates = []
english_rates = []

for qual in qualifications:
    qual_data = df[df['Qualification'] == qual]

    # Total population by qualification
    total_pop = qual_data['Count'].sum()
    
    # Literacy rate
    literate_count = qual_data[qual_data['num_languages'] != 0]['Count'].sum()
    literacy_rate = (literate_count / total_pop) * 100 if total_pop > 0 else 0
    literacy_rates.append(literacy_rate)
        
    # Multilingual rate 
    multilingual_count = qual_data[(qual_data['num_languages'] > 1)]['Count'].sum()
    multilingual_rate = (multilingual_count/total_pop) * 100
    multilingual_rates.append(multilingual_rate)

    # English speaker rate
    english_count = qual_data[qual_data['eng_speaker'] == 1]['Count'].sum()
    english_rate = (english_count / total_pop) * 100 if total_pop > 0 else 0
    english_rates.append(english_rate)

fig1 = go.Figure()

fig1.add_trace(go.Scatter(x=qualifications, y=literacy_rates, mode='lines+markers', name='Literacy Rate'))
fig1.add_trace(go.Scatter(x=qualifications, y=multilingual_rates, mode='lines+markers', name='Multilingual Rate'))
fig1.add_trace(go.Scatter(x=qualifications, y=english_rates, mode='lines+markers', name='English Rate'))

fig1.update_layout(
    title="Literacy by Qualification",
    xaxis_title="Qualification",
    yaxis_title="Percentage (%)",
    legend_title="Literacy Types",
    template="plotly"
)


with tab1: 
    st.plotly_chart(fig1, use_container_width=True)
    with st.expander("See insights"):
        st.markdown("* Higher education levels show increased multilingual rates")


with tab2:
    language_options = {"One Language": 1, "Two Languages": 2, "Three or More Languages": 3}
    selected_distribution = st.selectbox(
        "Filter by Number of Languages",
        ["All"] + list(language_options.keys())
    )

    pie_df = df.copy()
    if selected_distribution != "All":
        pie_df = pie_df[pie_df["num_languages"] == language_options[selected_distribution]]
        pie_data = pie_df.groupby('Language Literacy')['Count'].sum().reset_index()
        fig2 = px.pie(pie_df, values='Count', names='Language Literacy', title='Language Distribution')
        st.plotly_chart(fig2)
    else:
        all_data = pie_df.groupby('num_languages')['Count'].sum().reset_index()
        all_data['Language Category'] = all_data['num_languages'].map({
            0: 'Not Literate',
            1: 'One Language',
            2: 'Two Languages',
            3: 'Three or More Languages'
        })
        
        fig2 = px.pie(
            all_data,
            values='Count',
            names='Language Category',
            title='Overall Language Count Distribution'
        )
        st.plotly_chart(fig2)

    with st.expander("See insights"):
        st.markdown("""
                    * Largely unsurprising results, majority of population is bilingual
                    * Monolinguals: Greater proportion of Chinese-only speakers than English
            """
            )