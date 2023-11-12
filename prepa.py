import pandas as pd

# CSV : de tous les pays du monde
countries_df = pd.read_csv('data/curiexplore-pays.csv', delimiter=';', encoding='utf-8', keep_default_na=False) # Charger le fichier CSV de tous les pays

# EXCEPTION
servers_bonus = {
    'EUNE': {
        'name': 'Europe Nordic & East',
        'countries': ["Norway", "Sweden", "Finland", "Estonia", "Latvia", "Lithuania", "Belarus", "Ukraine", "Crimea", "Moldova", "Romania", "Bulgaria", "Greece", "Albania", "Macedonia", "Kosovo", "Montenegro", "Serbia", "Bosnia and Herzegovina", "Croatia", "Hungary", "Slovakia", "Slovenia", "Czech Republic" , "Poland"],
        'relation': None
    },
    'LAN': {
        'name': 'Latin America North',
        'countries': ["Venezuela", "Colombia", "Ecuador", "Peru"],
        'relation': "central_america_caraibes"
    },
    'LAS': {
        'name': 'Latin America South',
        'countries': ["Bolivia", "Paraguay", "Argentina", "Uruguay", "Chile"],
        'relation': None
    },
    'NA': {
        'name': 'North America',
        'countries': None,
        'relation': "north_america"
    },
    'OCE': {
        'name': 'Oceania',
        'countries': ["Australia", "New Zealand"],
        'relation': None
    },
    'LAT': {
        'name': 'Latin America',
        'countries': ["Bolivia", "Paraguay", "Argentina", "Uruguay", "Chile","Venezuela", "Colombia", "Ecuador", "Peru"],
        'relation': None
    },
    'SEA': {
        'name': 'Asia East South',
        'countries': ["Singapore", "Malaysia", "Indonesia", "Philippines", "Thailand", "Indonesia", "Taiwan"],
        'relation': None
    },
    'EUW': {
        'name': 'Europe West',
        'countries': ["France", "United Kingdom of Great Britain and Northern Ireland", "Ireland", "Spain", "Portugal", "Monaco", "Andorra", "Belgium", "Luxembourg", "Netherlands", "Switzerland", "Italy", "Saint Martin", "Vatican", "Malta", "Austria", "Germany"],
        'relation': None
    },
    'JPN': {
        'name': 'Japan',
        'countries': ["Japan"],
        'relation': None
    },
    'BRA':{
        'name': 'Brazil',
        'countries': ["Brazil"],
        'relation': None
    }
}

# Dictionnaire : pour le CSV des pays
pays_infos = {}

for index, row in countries_df.iterrows(): # Parcours chaque ligne du DataFrame et construire le dictionnaire
    name_en = row['name_en']
    iso2 = row['iso2']
    latlng = row['latlng']
    central_america_caraibes = row['central_america_caraibes']
    north_america = row['north_america']

    latlng_parts = latlng.split(',')
    if len(latlng_parts) == 2:
        latitude = float(latlng_parts[0].strip())
        longitude = float(latlng_parts[1].strip())
    else:
        latitude = None
        longitude = None

    pays_infos[name_en] = { # Ajout dans le dictionnaire
        'iso2': iso2,
        'latitude': latitude,
        'longitude': longitude,
        'central_america_caraibes': central_america_caraibes,
        'north_america': north_america,
    }

for abrev, server_info in servers_bonus.items(): # Pour ajouter les pays, à un serveur
    if server_info['relation'] is not None:
        relation = server_info['relation']
        for country_name, country_info in pays_infos.items():
            if(relation in country_info):
                if country_info[relation] == True:
                    if server_info['countries'] is None:
                        server_info['countries'] = []
                    server_info['countries'].append(country_name)

#print(servers_bonus)
#print(pays_infos['France'])
#print(servers_bonus['NA'])

# Dictionnaire final : regroupant les pays et les serveurs selon leur abrev/iso
servers_countries = {}

for abrev, server_info in servers_bonus.items(): # Parcours de servers_bonus
    server_data = {
        'name': server_info['name'],
        'countries': server_info['countries'],
        'latitude': None,
        'longitude': None,
        'coord': [None, None],
    }
    if server_info['countries']:
        coordinates = [[pays_infos[country_name]['longitude'], pays_infos[country_name]['latitude']] for country_name in server_info['countries'] if country_name in pays_infos]
        if coordinates:
            server_data['coord'] = coordinates
        else:
            server_data['coord'] = [None, None]

    servers_countries[abrev] = server_data # Ajout à servers_countries avec abrev

for country_name, country_info in pays_infos.items(): # Parcours du dictionnaire pour le CSV des pays
    country_data = {
        'name': country_name,
        'countries': [country_name],
        'latitude': country_info.get('latitude', None),
        'longitude': country_info.get('longitude', None),
        'coord': [[country_info.get('longitude', None), country_info.get('latitude', None)]],
    }
    servers_countries[country_info['iso2']] = country_data # Ajout à servers_countries avec iso2

#print(servers_countries["NA"])
#print(servers_countries["FR"])
#print(servers_countries["UK"])
#print(pays_infos["Bolivia"])

