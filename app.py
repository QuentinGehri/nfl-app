import streamlit as st
import pandas as pd


def load_data(year):
    url = "https://www.pro-football-reference.com/years/" + str(year) + "/passing.htm"
    html = pd.read_html(url, header=0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index)  # Deletes repeating headers in content
    raw = raw.fillna(0)
    stat_joueur = raw.drop(['Rk'], axis=1)
    return stat_joueur


def load_data_by_player(nom_joueur, index):
    # https://www.pro-football-reference.com/players/H/HoweSa00.htm URL du WebScrapping (avec par exemple Dak Prescott)
    position_espace = index[0].find(" ")
    position_espace = int(position_espace)
    st.markdown(index[0])
    initiale = ""
    nom_raccourci = ""
    #for i in range(position_espace + 1, position_espace + 5):
    i = position_espace + 1
    while (len(nom_raccourci) != 4)
        if index[0][i] != "'":
            nom_raccourci += index[0][i]
        if i == position_espace + 1:
            initiale = index[0][i]
        i+=1
    for i in range(2):
        if index[0][i] == ".":
            nom_raccourci += index[0][i+1]
        else:
            nom_raccourci += index[0][i]
    url = "https://www.pro-football-reference.com/players/" + str(initiale) + "/" + str(nom_raccourci) + "00.htm"
    st.markdown(url)
    html = pd.read_html(url, header=0)
    df = html[0]
    raw = df.drop(df.index[0])
    raw = raw.fillna(0)
    stat_joueur = raw
    return stat_joueur


def show_tableau_entier(player_stats):
    st.title("Resume des statistiques de passe à la NFL")

    # Afficher les données dans un tableau
    st.dataframe(player_stats)


def show_graphique(player_stats):
    st.title("Graphique à Points")

    # Créer un DataFrame avec les colonnes nécessaires
    age_nom_joueur = pd.DataFrame({
        'Joueur': player_stats['Player'],
        'Age': player_stats['Age'],
    })

    # Afficher le graphique à points
    st.scatter_chart(data=age_nom_joueur, x='Joueur', y='Age', use_container_width=True)


def show_details(player_stats):
    st.title("Détails du Joueur")

    # Créer un DataFrame avec les colonnes nécessaires
    age_nom_joueur = pd.DataFrame({
        'Joueur': player_stats['Player'],
        'Age': player_stats['Age'],
    })

    # Sélectionner un joueur dans la liste déroulante
    selected_player = st.selectbox('Sélectionnez un joueur', age_nom_joueur['Joueur'])

    selected_player_index = age_nom_joueur['Joueur'].tolist().index(selected_player)


    # Afficher les détails du joueur sélectionné
    if selected_player:
        selected_player_data = player_stats[player_stats['Player'] == selected_player]
        index = age_nom_joueur.loc[selected_player_index]
        stat_par_match = load_data_by_player(selected_player_data['Player'], index)
        st.dataframe(selected_player_data)
        st.dataframe(stat_par_match)


def show_stats_semaine_par_semaine():
    pass


def main():
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

    # Sélectionner la page à afficher
    selected_page = st.radio("Sélectionnez la page", ("Graphique à Points et Tableau", "Détails du Joueur"))

    # Charger les données pour une année spécifique
    player_stats = load_data(selected_year)

    # Afficher le contenu de la page sélectionnée
    if selected_page == "Graphique à Points et Tableau":
        show_tableau_entier(player_stats)
        show_graphique(player_stats)
    elif selected_page == "Détails du Joueur":
        show_details(player_stats)


if __name__ == "__main__":
    main()
