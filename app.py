import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import lxml

st.title('NFL Football Stats (Rushing) Explorer')

st.markdown("""
This app performs simple webscraping of NFL Football player stats data (focusing on Rushing)!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [pro-football-reference.com](https://www.pro-football-reference.com/).
""")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1990, 2024))))

# Web scraping of NFL player stats
# https://www.pro-football-reference.com/years/2019/rushing.htm


@st.cache_data()
def load_data(year):
    url = "https://www.pro-football-reference.com/years/" + str(year) + "/passing.htm"
    html = pd.read_html(url, header=0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index)  # Deletes repeating headers in content
    raw = raw.fillna(0)
    stat_joueur = raw.drop(['Rk'], axis=1)
    return stat_joueur


player_stats = load_data(selected_year)

st.dataframe(player_stats)

age_nom_joueur = pd.DataFrame({
    'Joueur': player_stats['Player'],
    'Age': player_stats['Age'],
})


st.scatter_chart(data=age_nom_joueur, x='Joueur', y='Age', use_container_width=True)





