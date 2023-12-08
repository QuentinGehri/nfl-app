# Imports
import streamlit as st
import pandas as pd

# Constantes
NB_TOUR_POUR_NOM_FAMILLE = 4


# Procédures et fonctions
def load_data(year):
    url = "https://www.pro-football-reference.com/years/" + str(year) + "/passing.htm"
    html = pd.read_html(url, header=0)
    df = html[0]
    # Supprime les lignes répétitives
    df = df[~df.duplicated()].reset_index(drop=True)
    # Supprime la colonne 'Rk'
    df = df.drop(['Rk'], axis=1)
    player_to_remove = 'Player'
    df = df[df['Player'] != player_to_remove]
    # Réinitialiser l'index après la suppression
    df.reset_index(drop=True, inplace=True)
    # Remplace les valeurs NaN par 0
    df = df.fillna(0)
    return df


def load_data_by_player(index):
    # https://www.pro-football-reference.com/players/H/HoweSa00.htm URL du WebScrapping (avec par exemple Sam Howell)
    position_espace = index[0].find(" ")
    position_espace = int(position_espace)
    st.markdown(index[0])
    initiale = ""
    nom_raccourci = ""
    i = position_espace + 1
    nb_tour = 0
    while nb_tour < NB_TOUR_POUR_NOM_FAMILLE:
        if index[0][i] != "'":
            nom_raccourci += index[0][i]
            if i == position_espace + 1:
                initiale = index[0][i]
            nb_tour += 1
        i += 1
    for i in range(2):
        if index[0][i] == ".":
            nom_raccourci += index[0][i+1]
        else:
            nom_raccourci += index[0][i]
    url = "https://www.pro-football-reference.com/players/" + str(initiale) + "/" + str(nom_raccourci) + "00.htm"
    st.markdown(url)
    # Spécifier header=1 pour utiliser la première ligne comme en-tête
    # Lire le HTML avec header=1
    df = pd.read_html(url, header=1)[0]
    # Remplacer les valeurs NaN par 0
    df = df.fillna(0)
    # Remplacer le nom de la 3ᵉ colonne par un nouveau nom
    new_column_name = "Lieu"
    df.rename(columns={df.columns[2]: new_column_name}, inplace=True)
    return df


def show_tableau_entier(player_stats):
    st.title("Resume des statistiques de passe à la NFL")

    # Afficher les données dans un tableau
    st.dataframe(player_stats)


def show_graphique(player_stats):
    # Supposons que player_stats['QBrec'] contienne une chaîne telle que '7-5-0'
    qbrec_str = player_stats['QBrec']
    liste_pourcentage_victoire = []
    # Parcourir la liste
    for resultat in qbrec_str:
        # Vérifier si qbrec_str n'est pas égal à 0 (non vide)
        if resultat != 0 and resultat != 'QBrec':
            nombres = [int(nombre) for nombre in resultat.split('-')]
            tot_match = sum(nombres)
            # Vérifier si tot_match n'est pas égal à 0 pour éviter une division par zéro
            if tot_match != 0:
                pourcentage_victoire = nombres[0] / tot_match
                pourcentage_victoire *= 100
            else:
                pourcentage_victoire = 0
        else:
            pourcentage_victoire = 0
        liste_pourcentage_victoire.append(pourcentage_victoire)

    # Créer un DataFrame avec les colonnes nécessaires
    age_nom_joueur = pd.DataFrame({
        'Joueur': player_stats['Player'],
        'Pourcentage': liste_pourcentage_victoire,
    })

    # Afficher le graphique à points
    st.title("Graphique representant le pourcentage de victoire de chaque joueur")
    st.bar_chart(data=age_nom_joueur, x='Joueur', y='Pourcentage', use_container_width=True)


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
        stat_par_match = load_data_by_player(index)
        st.dataframe(selected_player_data)
        st.dataframe(stat_par_match)


# Procédure main()
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


# Appel de la procédure main()
if __name__ == "__main__":
    main()
