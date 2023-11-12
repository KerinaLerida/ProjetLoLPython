import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import os
import prepa

current_directory = os.path.dirname(os.path.realpath(__file__))
repertoire = os.path.join(current_directory,'data')

seasons = [] # Regroupe toutes des années de saison
seasons_int=[] # Pour le slider (graph 1)

for fichier in os.listdir(repertoire): # Recup les saisons disponibles en fonction des csv présents
    if fichier.endswith(".csv") and fichier.startswith("season_"):
        annee = fichier.split("_")[1].split(".")[0]
        seasons_int.append(int(annee))
        seasons.append(annee)

data = {}  # Dictionnaire : pour stocker les données de chaque saison, via les csv des saisons
for season in seasons:
    df = pd.read_csv(f'data/season_{season}.csv', encoding='ISO-8859-1', delimiter=';', keep_default_na=False)  # Spécifiez l'encodage
    df.columns= df.columns.str.replace('ï»¿name', 'team_name')
    df['winRate'] = df['winRate'].str.replace('%', '').astype(float)
    data[season] = df

#print(data['2015'].keys())
#print(data['2015']['winRate'])

ranged={ # Range pour la colorimétrie des données consultés sur le dashboard
    'nbGames': {
        'min': 0,
        'max': None,
        },
    'winRate': {
        'min': 0,
        'max': 100,
        },
    'KD': {
        'min': 0,
        'max': 2,
        },
    'GPM': {
        'min': 1000,
        'max': 2000,
        },
    'killsPerGame': {
        'min': 0,
        'max': 30,
        },
    'deathsPerGame': {
        'min': 0,
        'max': 30,
        },
    'towersKilled': {
        'min': 0,
        'max': 11,
        },
    'towersLost': {
        'min': 0,
        'max': 11,
        },
}

# EXCEPTION : Pays dont l'iso2 ne correspond pas au iso/abrev du dictionnaire (servers_countries) crée dans prepa.py
LE=['WC','CIS','UK','PCS','SWE','CZ/SK'] # Liste des exceptions
E = {
    'WC': {
        'except': 'RU',
    },
    'CIS': {
        'except': 'RU',
    },
    'UK': {
        'except': 'GB',
    },
    'PCS': {
        'except': 'TW',
    },
    'SWE': {
        'except': 'FI',
    },
    'CZ/SK': {
        'except': 'CZ',
    }
}

def generate_histogram(selected_season,selected_info):
    selected_season = str(selected_season)
    selected_info = str(selected_info)
    df = data[selected_season][selected_info]
    df = data[selected_season][data[selected_season][selected_info] != '-'] # Nettoie la donnée

    maxi=ranged[selected_info]['max'] # Récupération de la Range
    if ranged[selected_info]['max'] is None:
        maxi=max(df[selected_info])
    mini=ranged[selected_info]['min']

    return px.histogram(df, x=selected_info,
                       title=f'{selected_info} des équipes - Saison {selected_season}',
                       nbins= 20,
                       range_x=[mini, maxi],
                       labels={'value': selected_info},
                       template='plotly_dark',
                       opacity=0.7,
                       color_discrete_sequence=['skyblue'])

def generate_map_team(selected_season, selected_info, selected_team):
    selected_season = str(selected_season)
    selected_info = str(selected_info)
    selected_team = str(selected_team)

    df = data[selected_season]
    df = df[df['team_name'] == selected_team] # Récupération du dataframe associée à la saison et à l'équipe sélectionnées

    if df.empty: # Vérification
        error_message = f"Aucune information disponible pour {selected_info} de l'équipe {selected_team} dans la saison {selected_season}."
        fig = px.scatter(title=error_message)
    else:
        iso = df['region'].iloc[0]
        c = []
        v = []
        t=[]

        if iso in prepa.servers_countries: # Trouver les pays associés à l'équipe
            for country in prepa.servers_countries[str(iso)]['countries']:
                c.append(country)
                v.append(df[selected_info].iloc[0])
                t.append(selected_team)
        else:
            error_message = f"Aucune information disponible pour {selected_info} de l'équipe {selected_team} dans la saison {selected_season}."
            fig = px.scatter(title=error_message)

        df_map = pd.DataFrame({'country': c, 'value': v, 'team_name':t}) # Création du DataFrame pour la carte
        df_map = df_map.dropna(subset=['value']) # Nettoie la donnée

        if df_map.empty: # Vérification
            error_message = f"Aucune information disponible pour {selected_info} de l'équipe {selected_team} dans la saison {selected_season}."
            fig = px.scatter(title=error_message)
        else:
            fig = px.choropleth( # Création de la carte choropleth
                df_map,
                locations='country',
                locationmode='country names',
                color='value',
                title=f'Position géographique de l\'équipe {selected_team} - Saison {selected_season}',
                template='plotly_dark',
                hover_data={'country': True, 'value': True, 'team_name':True},
                color_continuous_scale="Plasma",
                range_color=[min(data[selected_season][selected_info]), max(data[selected_season][selected_info])],  # Définissez la plage de couleurs
            )
            fig.update_geos( # Apparence de la carte
                projection_type="natural earth",
                showcoastlines=True, coastlinecolor="Black",
                showland=True, landcolor="lightgrey",
                showocean=True, oceancolor="lightblue",
                showframe=False,
                showcountries=True,
                countrycolor="Black",
            )
            fig.update_layout( # Ajustement
                geo=dict(
                    showland=True,
                    showcoastlines=True,
                    landcolor= 'rgb(56, 111, 72)',
                    center=dict(lon=-0, lat=0),
                    projection_scale=1,
                ),
                height=500
            )
            fig.update_geos(fitbounds="locations", visible=False) # Zoom sur les pays concernés/colorés

    return fig


def generate_map(selected_season,selected_info):
    df = data[selected_season][['region', str(selected_info), 'team_name']]
    c=[]
    v=[]
    for info, iso in zip(df[str(selected_info)], df['region']): # Récupération des pays pour chaque team et leur attribué la valeur de l'info de la team
        if iso in prepa.servers_countries:
            for country in prepa.servers_countries[str(iso)]['countries']:
                c.append(country)
                v.append(info)

    df_map=pd.DataFrame({'country': c, 'value': v}) # Création du DataFrame pour la carte

    # Agrégation par pays des valeurs
    if selected_info =='nbGames':
        df_map = df_map.groupby('country', as_index=False).sum()
    else :
        df_map = df_map.groupby('country', as_index=False).mean()

    fig = px.choropleth( # Création de la carte choropleth
        df_map,
        locations='country',
        locationmode='country names',
        color='value',
        color_continuous_scale="Plasma",
        range_color=[min(df_map['value']), max(df_map['value'])],
        labels={'Value': str(selected_info)},
        template='plotly_dark',
    )
    fig.update_geos( # Apparence de la carte
        projection_type="natural earth",
        showcoastlines=True, coastlinecolor="Black",
        showland=True, landcolor="lightgray",
        showocean=True, oceancolor="lightblue",
        showframe=False,
        showcountries=True,
        countrycolor="Black",
    )
    fig.update_layout( # Ajustement
        geo=dict(
            showland=True,
            showcoastlines=True,
            landcolor='rgb(217, 217, 217)',
            center=dict(lon=-0, lat=0),
            projection_scale=1,
        ),
        height=500
    )
    return fig


app = Dash(__name__,external_stylesheets=[dbc.themes.CYBORG])
seasons_as_years = [str(season) for season in seasons]

app.layout = html.Div([
    html.H1(children='Projet League of Legends', style={'textAlign': 'center', 'color': 'purple', 'fontSize': 40, 'font-weight': 'bold', 'font-family': 'Algerian'}),
    html.Div([
        html.Div([
            html.H1("Histogramme du Winrate en fonction de la Saison [ Seul graphique indépendant des autres ]", style={'textAlign': 'center','fontSize': 24,'font-weight': 'bold', 'font-family': 'Callibri'}),
            html.H2("Sélectionne une saison, correspondant à une année :", style={'fontSize': 16}),
            dcc.Slider(
                min=min(seasons_int),
                max=max(seasons_int),
                step=None,
                id='year--slider',
                value=max(seasons_int),
                marks={str(annee): str(annee) for annee in seasons_int},
             ),
            dcc.Graph(id='graph-content-1'),
            html.Br()
        ], style={'display': 'inline-block', 'width': '50%'}),
        html.Div([
            html.H1("Carte du Monde en fonction de la Saison, dépendant de la caractéristique choisie", style={'textAlign': 'center','fontSize': 24,'font-weight': 'bold', 'font-family': 'Callibri'}),
            html.H2("Sélectionne une saison, correspondant à une année :", style={'fontSize': 16}),
            dcc.Dropdown([{'label': str(season), 'value': season} for season in seasons], str(seasons[0]), id='dropdown-selection'),
            html.H2("Sélectionne une caractéristique à visualiser :", style={'fontSize': 16}),
            dcc.Dropdown([{'label': str(info), 'value': info} for info in ['nbGames', 'winRate', 'KD', 'GPM','killsPerGame', 'deathsPerGame', 'towersKilled', 'towersLost'] ], str('nbGames'), id='dropdown-selection-2'),
            html.Br(),
            dcc.Graph(id='graph-content-2'),
            html.H2("On peut voir que le jeu League of Legends n'est pas implanté dans tout le monde.", style={'fontSize': 16}),
        ], style={'display': 'inline-block', 'width': '50%'}),
    ]),
    html.Br(),
    html.Div([
        html.Div([
            html.H1("Carte du Monde en fonction de la Saison des Teams, dépendant de la caractéristique choisie", style={'textAlign': 'center','fontSize': 24,'font-weight': 'bold', 'font-family': 'Callibri'}),
            html.H2("Sélectionne une Team participant à la Saison choisie :", style={'fontSize': 16}),
            dcc.Dropdown(id='dropdown-selection-3'),
            #dcc.Dropdown([{'label': str(team_name), 'value': team_name} for team_name in data[str(season)]['team_name']], str(data[str(season)]['team_name'][0]), id='dropdown-selection-3'),
            dcc.Graph(id='graph-content-3')
        ], style={'display': 'inline-block', 'width': '50%'}),
        html.Div([
            html.H1("Histogramme en fonction de la saison, dépendant de la caractéristique choisie", style={'textAlign': 'center','fontSize': 24,'font-weight': 'bold', 'font-family': 'Callibri'}),
            dcc.Graph(id='graph-content-4')
        ], style={'display': 'inline-block', 'width': '50%'}),
    ]),
])

@callback(
    Output('graph-content-2', 'figure'),
    Input('dropdown-selection', 'value'),
    Input('dropdown-selection-2', 'value')
)
def update_choropleth_map(selected_season,selected_info):
    return generate_map(selected_season,selected_info)

@app.callback(
    Output('dropdown-selection-3', 'options'),
    Input('dropdown-selection', 'value'),
)
def update_teams(selected_season):
    teams = data[selected_season]['team_name']
    options = [{'label': str(team_name), 'value': team_name} for team_name in teams]
    return options

@app.callback(
    Output('dropdown-selection-3', 'value'),
    Input('dropdown-selection', 'value'),
)
def update_team_value(selected_season):
    return data[selected_season]['team_name'][0]

@callback(
    Output('graph-content-3', 'figure'),
    Input('dropdown-selection', 'value'),
    Input('dropdown-selection-2', 'value'),
    Input('dropdown-selection-3', 'value'),
)
def update_graph3(selected_season,selected_info,selected_team):
    return generate_map_team(selected_season,selected_info,selected_team)


@callback(
    Output('graph-content-4', 'figure'),
    Input('dropdown-selection', 'value'),
    Input('dropdown-selection-2', 'value')
)
def update_graph4(selected_season,selected_info):
    return generate_histogram(selected_season,selected_info)

@app.callback(
    Output('graph-content-1', 'figure'),
    Input('year--slider', 'value')
)
def update_slider(selected_season): # Première version de l'histogramme
    selected_season = str(selected_season)
    df = data[selected_season]
    df = df[df['winRate'] != '-']

    return px.histogram(df, x='winRate',
                       title=f'Winrate des équipes - Saison {selected_season}',
                       nbins=20,
                       range_x=[0, 100],
                       labels={'winRate': 'Winrate (%)'},
                       template='plotly_dark',
                       opacity=0.7,
                       color_discrete_sequence=['purple']
                       )

if __name__ == '__main__':
    app.run(debug=True)
