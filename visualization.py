from packages import *

# from packages.fonctions.supprimer_valeurs import supprimer_valeurs
# from packages.fonctions.remplacer_valeurs import remplacer_valeurs
from packages.fonctions.make_graphics import make_metrics, make_graphics, make_tables
from packages.collecte.extract_data import extract_mongodb
from packages.graphiques_metriques import nombre_de_morts_blesses as nmb
from packages.graphiques_metriques import type_cibles as tc
from packages.graphiques_metriques import type_armes as ta
from packages.graphiques_metriques import en_det_po as edp
from packages.graphiques_metriques import groupes_terroristes as gt
from packages.graphiques_metriques import attaques_afrique as aa
from packages.graphiques_metriques import mode_revendication as mr
from packages.graphiques_metriques import dommages_proprietes as dp
from packages.graphiques_metriques import attaques_suicides as asu
from packages.graphiques_metriques import demande_rancons as dr
from packages.graphiques_metriques import prédiction as pred
from packages.graphiques_metriques.attaques_afrique import traitement

# =========================================================================

# récupération du temps pour les mises-à-jour
# try:
#     # heure actuel
#     with open("data")
# except Exception as e:


# =========================================================================

# Récupérons à nouveau les données de la base de données s'il est 6h du matin
if str(dt.now().time())[:8] == '06:00:00':
    extract_mongodb("mongodb+srv://admin:root@cluster0.zblzd.mongodb.net/?retryWrites=true&w=majority")
    
# try:
#     extract_mongodb("mongodb+srv://admin:root@cluster0.zblzd.mongodb.net/?retryWrites=true&w=majority")
# except Exception as e:
#     print("Error", e)

# initialisation de df_terror
data = None

# Récupération des données prétraitées
try:
    with open("packages/data/cleaned/terror.txt", "rb") as f:
        pick = pickle.Unpickler(f)
        data = pick.load()

except Exception as e:
    print("Pickle File Error:", e)

# =========================================================================

# configurer lien jquery
external_scripts = [
    "https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js",
    "/assets/js/dynamique.js",
]

# configurer font-awesome pour les icones
external_style = ["/assets/fontawesome/css/all.css"]

# Initialisation de l'application
app = dash.Dash(
    __name__, external_scripts=external_scripts, external_stylesheets=external_style,
    suppress_callback_exceptions = True
)

# ajout server
server = app.server

# =========================================================================

# print(df_terror.head())
# Mettons la date comme index
data.set_index("date", inplace=True)


# renommons certaines colonnes
data.rename(
    columns={
        "nkill": "Nombre de morts",
        "nwound": "Nombre de blessés",
        "iday": "Jour",
        "iyear": "Année",
        "imonth": "Mois",
        "country_txt": "Pays",
        "region_txt": "Région",
        "city": "Ville",
    },
    inplace=True,
)

# recuperation du jeu de données des pays africains
df_africa = traitement(data)


# Récupérons la liste des pays
pays = data["Pays"].unique().tolist()

# Récupérons la liste des pays africains
pays_africains = df_africa["Pays"].unique().tolist()

# Créons une liste contenant les mois de l'année
mois = [
    "Janvier",
    "Fevrier",
    "Mars",
    "Fevrier",
    "Mars",
    "Avril",
    "Mai",
    "Juin",
    "Juillet",
    "Aout",
    "Septembre",
    "Octobre",
    "Novembre",
    "Novembre",
    "Décembre",
]

# Récupérons la première date ou la date minimale
first_date = data[["Jour", "Mois", "Année"]].head(1)

# Récupérons la dernière date ou la date maximale
last_date = data[["Jour", "Mois", "Année"]].tail(1)

# =========================================================================

# liste de pages
pages = [
    "Visualisation des nombres de morts et de blessés",
    "Visualisation des types de cibles",
    "Visualisation des types d'armes",
    "Visualisation des nombres d'enlèvements, de détournements ou de prises d'otages",
    "Visualisation des groupes terroristes",
    "Visualisation du terrorisme en Afrique",
    "Visualisation des modes de revendication",
    "Visualisation des dommages de propriétés",
    "Visualisation des nombres d'attaques suicides",
    "Visualisation des demandes de rançon",
    "Prédiction du succès d'une attaque terroriste"
]

# liste des nombres de graphiques pour chaque page
graphics_numbers = [
    12,
    3,
    4,
    3,
    3,
    2,
    1,
    2,
    2,
    2,
    1
]

# les noms des graphiques
graphic_names = [
    [
        "nombre total de personnes mortes à cause du terrorisme",
        'Nombre total de personnes blessées à cause du terrorisme',
        "nombre de morts causés par des attaques terroristes par pays et par année"
        ,
        "nombre de morts causés par des attaques terroristes par région et par année"
        ,
        "Nombre de morts par pays et par région"
        ,
        "Nombre de blessés par pays et par région"
        ,
        "nombre de morts causés par des attaques terroristes par province/Etat et par année",
        "répartition géographique du nombre de morts causés par des attaques terroristes par pays"
        ,
        "évolution annuelle de la répartition géographique du nombre de morts"
        ,
        "évolution annuelle de la répartition géographique du nombre de personnes blessées"
        ,
        "cumul annuel du nombre de morts par pays"
        ,
        "cumul annuel du nombre de morts causés par des attaques terroristes par région"
    ],
    [
        "nombre d’attaques terroristes par catégorie de cible de première classe",
        "nombre d’attaques terroristes par catégorie de cible de deuxième classe",
        "nombre d’attaques terroristes par catégorie de cible de troisième classe"
    ],
    [
        "nombre d’attaques terroristes par types d’armes de première classe",
        "nombre d’attaques terroristes par types d’armes de deuxième classe",
        "nombre d’attaques terroristes par types d’armes de troisième classe",
        "nombre d’attaques terroristes par types d’armes de quatrième classe"
    ],
    [
        "top 20 des pays qui ont été utilisés pour des opérations d’évasion",
        "répartition géographique du nombre d'attaques terroristes par pays d'évasion",
        "nombre d'attaques terroristes par dénouements d'enlèvements/de prises d'otages et par pays"
    ],
    [
        "top 10 des perpétrateurs d'attaques terroristes qui ont causés le plus de morts",
        "top 10 des perpétrateurs qui ont effectués le plus grand nombre d’attaques terroristes",
        "top 20 des nationalités de perpétrateurs avec le plus grand nombre d’attaques terroristes"
    ],
    [
        "nombre d’africains morts à cause du terrorisme par pays africains et par année",
        "nombre d’africains blessés à cause du terrorisme par pays africains et par année"
    ],
    [
        "nombre d’attaques terroristes par mode de revendication"
    ],
    [
        "nombre d’attaques terroristes par catégorie de dommages de propriété(s)",
        "liste des attaques accompagnées de dommages de propriétés très grave"
    ],
    [
        "nombre d’attaques terroristes accompagnées de suicides par année",
        "répartition géographique du nombre d’attaques terroristes accompagnés de suicide"
    ],
    [
        "répartition géographique du nombre d’attaques avec demande de rançons par pays",
        "nombre d’attaques terroristes avec demande de rançons par région et par année"
    ],
    [
        
    ]
]


# liste de boutons de navigation (tests)
navs = []
boutons = [dbc.NavLink(pages[0], href="/", active="exact")]

# on va creer en meme temps les dictionnaires des liens
link_dict = {"/": graphics_numbers[0]}
title_dict = {"/": graphic_names[0]}

for j in range(2, len(pages) + 1):
    boutons.append(dbc.NavLink(pages[j - 1], href=f"/page-{j-1}", active="exact"))
    link_dict[f"/page-{j-1}"] = graphics_numbers[j-1]  # type: ignore
    title_dict[f"/page-{j-1}"] = graphic_names[j-1]

# =========================================================================

# Ajout de la barre de navigation
sidebar = dbc.Card(
    dbc.CardBody(
        html.Div(
            [
                html.Div(
                    [
                        html.H2("Attaques terroristes", className="display-4"),
                        html.Hr(),
                        html.P("Choisissez une page", className="lead"),
                        dbc.Nav(boutons, vertical=True, pills=True)
                    ],
                    className="h-100 nav-container p-2"
                ),
                html.Div(
                    html.Div(
                        [
                            html.I(
                                className="fa-solid fa-circle-arrow-right shadow-lg rounded-circle right-arrow icone-bleu fa-3x",
                                style={
                                    "position": "absolute",
                                    "top": "50%",
                                    "left": "30%",
                                },
                            ),
                            html.I(
                                className="fa-solid fa-circle-arrow-left shadow-lg rounded-circle left-arrow icone-bleu fa-3x",
                                style={
                                    "position": "absolute",
                                    "top": "50%",
                                    "left": "30%",
                                },
                            ),
                        ],
                        className="h-100",
                    ),
                    className="h-100 indic-slide shadow-md rounded-end",
                    style={
                        "position": "fixed",
                        "top": 0,
                        "left": "100%",
                        "width": "80px",
                    },
                ),
            ],
            className="h-100",
            style={"position": "relative"},
        ),
        className="h-100"
    ),
    color="light",
    className="h-100 sidebar shadow-md pd-0",
    style={
        "width": "49rem",
        "position": "fixed",
        # "overflowY": "auto",
        "top": 0,
        "left": "-49rem",
    },
)

# =========================================================================

# Définition de la squelette principale du contenu
content = dbc.Container(
    [
        html.Div(
            [
                html.Div(
                    [
                    html.Label("Plage de dates", className = "m-2"),
                    dcc.DatePickerRange(
                        id="date-picker",
                        calendar_orientation="horizontal",
                        day_size=39,
                        end_date_placeholder_text="Dernière date",
                        start_date_placeholder_text="Première date",
                        with_portal=True,
                        first_day_of_week=0,
                        reopen_calendar_on_clear=True,
                        is_RTL=False,
                        clearable=True,
                        number_of_months_shown=1,
                        min_date_allowed=dt(
                            int(first_date["Année"]),
                            int(first_date["Mois"]),
                            int(first_date["Jour"]),
                        ),
                        max_date_allowed=dt(
                            int(last_date["Année"]),
                            int(last_date["Mois"]),
                            int(last_date["Jour"]),
                        ),
                        # initial_visible_month=dt(
                        #     2020,
                        #     1,
                        #     1
                        # ),
                        start_date=dt(
                            int(first_date["Année"]),
                            int(first_date["Mois"]),
                            int(first_date["Jour"]),
                        ).date(),
                        end_date=dt(
                            int(last_date["Année"]),
                            int(last_date["Mois"]),
                            int(last_date["Jour"]),
                        ).date(),
                        display_format="YY, MMM DD",
                        month_format="MMMM, YYYY",
                        minimum_nights=4,
                        persistence=True,
                        persisted_props=["start_date", "end_date"],
                        persistence_type="session",
                        updatemode="singledate",
                        className="shadow-lg"
                    )
                    ],
                    style={"textAlign": "right", "margin": "1rem"}
                ),
                dbc.Row(
                    [
                        html.Label(id="content-title", style={"margin-bottom": "1rem"}),
                        dbc.Col(
                            dcc.Dropdown(
                                id="pays",
                                # value = "form-control pd-3",
                                # className="form-control",
                                placeholder="Choisissez un pays",
                                multi=True,
                                style={"verticalAlign": "middle", "padding": "4px!important"},
                            ),
                            width=9,
                        ),
                        dbc.Col(
                            dbc.Button(
                                "Filtrer par pays",
                                id="filtre",
                                className="btn btn-lg btn-tertiary rounded-0",
                            ),
                            width=3,
                            className="justify-content-around"
                        ),
                    ],
                    className="text-center m-0"
                ),
                dbc.Row(
                [
                    dbc.Col(
                        html.Label("Choisissez un graphique", id="content-title-2", className = "m-2"),
                        width = 2
                    )
                    ,
                    dbc.Col(
                        dcc.Dropdown(
                            id="graphics",
                            # value = "form-control pd-3",
                            placeholder="Choisissez un graphique à afficher",
                            multi=False,
                            value = 1,
                            className = "pl-3 mt-2",
                            style={"verticalAlign": "middle", "padding": "4px!important"},
                        ),
                        width=8
                    )
                ],
                className = "justify-content-center"
                )
            ],
            id = "header-1"
        ),
        html.Div(
            [
                html.Div(
                    html.H2("Prédiction du succès d'une attaque terroriste"),
                    className="w-100"
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                            dbc.Row(
                                [
                                html.Label("Date de l'attaque", className = "text-center"),
                                dcc.DatePickerSingle(
                                    date=date(2023, 6, 21),
                                    display_format='Y, MMMM DD',
                                    id = "date-single",
                                    className = "m-1"
                                ),
                                ],className = "justify-content-center text-center"
                            ),
                            dbc.Row(
                                dcc.Dropdown(
                                id="suicide",
                                options = [{"value": 1, "label": "Oui"}, {"value": 0, "label": "Non"}],
                                # className="form-control",
                                placeholder="Avec suicide",
                                multi = False,
                                className = "m-1"
                            )
                            ),
                            dbc.Row(
                                dcc.Dropdown(
                                    id="attacktype",
                                    options = [{"value": attack, "label": attack} for attack in data["attacktype1_txt"].unique().tolist()],
                                    # className="form-control",
                                    placeholder="Type d'attaque",
                                    multi = False,
                                    className = "m-1"
                                )
                            ),
                            dbc.Row(
                                dcc.Dropdown(
                                    id="targtype",
                                    options = [{"value": targ, "label": targ} for targ in data["targtype1_txt"].unique().tolist()],
                                    # className="form-control",
                                    placeholder="Type de cible",
                                    multi = False,
                                    className = "m-1"
                                )
                            ),
                            dbc.Row(
                                dcc.Dropdown(
                                    id="natlty",
                                    options = [{"value": nat, "label": nat} for nat in data["natlty1_txt"].unique().tolist()],
                                    # className="form-control",
                                    placeholder="Nationalité du groupe terroriste",
                                    multi = False,
                                    className = "m-1"
                                )
                            ),
                            dbc.Row(
                                dcc.Dropdown(
                                    id="weaptype",
                                    options = [{"value": weap, "label": weap} for weap in data["weaptype1_txt"].unique().tolist()],
                                    # className="form-control",
                                    placeholder="Type d'arme",
                                    multi = False,
                                    className = "m-1"
                                )
                            ),
                            dbc.Row(
                                dcc.Dropdown(
                                    id="pays_",
                                    options = [{"value": count, "label": count} for count in data["Pays"].unique().tolist()],
                                    # className="form-control",
                                    placeholder="Pays",
                                    multi = False,
                                    className = "m-1"
                                )
                            ),
                            dbc.Row(
                                daq.NumericInput(  # type: ignore
                                    id = "nkill",
                                    label='Nombre de morts',
                                    labelPosition='bottom',
                                    className = "m-1",
                                    max = 100000
                                )
                            ),
                            dbc.Row(
                                dbc.Button(
                                    "Effectuer une prédiction",
                                    id="prediction",
                                    className="btn btn-lg btn-tertiary rounded-0"
                                ),
                                className = "m-1"
                            )
                            ],
                            style={"border-right": "solid 2px"}
                        ),
                        dbc.Col(
                            html.Div(id="principal-content-2", style = {"display": "none"})
                        )
                    ]
                ) 
            ],
            id = "header-2",
            className = "text-center w-100 p-3",
            style = {"display": "none"}
        ),
        # html.Div(
        #     id = "slider-top",
        #     className="text-center",
        #     children = [
        #         html.Label("Choisissez le nombre de pays dans le top"),
        #         dcc.Slider(
        #             id = "choose-number",
        #             value = 10,
        #             # className="form-control",
        #             min = 5,
        #             max = 100,
        #             marks={i: str(i) for i in range(5, 100+1, 5)}
        #         )
        #     ],
        #     style={"display": "none"}
        # ),
        

        html.Div(id = "links", className = "change-graphic"),
        html.Div(id="principal-content-1"),
        
    ]
)

# =========================================================================

# Réunissons le location, la barre de navigation et le contenu dans le layout
app.layout = dbc.Container(
    [
        dcc.Location(id="url"),
        dbc.Row(
            [
                dbc.Col(sidebar, width=2, style={"zIndex": 100}),
                dbc.Col(
                    content,
                    width=9,
                    # style = {
                    # "margin-left": "20rem"
                    # }
                ),
            ]
        ),
        html.Div(id = "shad", style = {"display": "none"})
    ],
    fluid=True,
)


# =========================================================================
# =========================================================================

######
# @contextmanager
# def change(path):
#     try:
#         f = open(path, "w")
#         base = sys.stdout
#         sys.stdout = f
#         yield
#     finally:
#         sys.stdout = base


######

# # Définition d'un callback pour ajouter ou supprimer un header
@app.callback(
    [
        # Output(component_id="slider-top", component_property="children"),
        Output(component_id="header-1", component_property="style"),
        Output(component_id="header-2", component_property="style"),
        Output(component_id="principal-content-1", component_property="style"),
        Output(component_id="principal-content-2", component_property="style"),
        Output(component_id = "links", component_property = "style")
    ],
    [Input(component_id="url", component_property="pathname")]
)
def add_header(pathname: str):
    '''Cette fonction rend un header visible ou pas 
    Args:
        pathname(str): contient le chemin d'accés
    Returns:
        style du slider
    '''
    if pathname == "/page-10":
        return (
            {"display": "none"}
        ,
            {"padding": "0"}
        ,
            {"display": "none"}
        ,
            {"padding": "0"}
        ,
            {"display": "none"}
        )  
    return (
        {"padding": "0"}
    ,
        {"display": "none"}
    ,
        {"padding": "0"}
    ,
        {"display": "none"}
    ,
        {"padding": "0"}
    )

######

@app.callback(
    Output(component_id = "pays", component_property = "options"),
    [Input(component_id="url", component_property = "pathname")]
)
def add_pays(pathname):
    global df_terror 
    
    if pathname == "/page-5":
        df_terror = df_africa
        return [{"label": p, "value": p} for p in pays_africains]
    df_terror = data
    return [{"label": p, "value": p} for p in pays]
######

@app.callback(
    Output(component_id="graphics", component_property= "options"),
    [Input(component_id="url", component_property="pathname")]
)
def add_links(pathname: str):
    '''Permet fonction permet d'ajouter des liens vers les graphiques
    '''
    return [{"value" : i+1, "label": title_dict[pathname][i]} for i in range(link_dict[pathname])]  # type: ignore

######

# Définition des callbacks pour la résolution des questions
@app.callback(
    Output(component_id="principal-content-1", component_property="children"),
    [
        Input(component_id="url", component_property="pathname"),
        Input(component_id="date-picker", component_property="start_date"),
        Input(component_id="date-picker", component_property="end_date"),
        Input(component_id="graphics", component_property = "value")
    ],
    [
        Input(component_id="filtre", component_property="n_clicks"),
        State(component_id="pays", component_property="value"),
        # Input(component_id="choose-number", component_property="value")
    ],
)
def add_response(pathname, start_date, end_date, graphique, n, pays):
    """Fonction qui renvoie une réponse à une question selon le pathname donné en entrée.
    Args:
        pathname(str): Contient le chemin d'accés
        start_date(str): La date de départ
        end_date(str): La date de fin
        pays(str ou list): Contient le pays ou les pays qui est/sont recherchés dans le dataset
        top(int): Définit le numéro du top des pays à afficher dans les pages 8 et 9
    """
    global df_terror
    
    # Filtrage des données par dates et par pays avant de retourner les résultats
    # en fonction du pathname
    df = df_terror.loc[start_date:end_date]
    
    # filtrage par pays si nécessaire
    if n != None:
        if pays != None and pays != "" and pays != []:
            if not type(pays) is list:
                pays = [pays]
            df = df[df["Pays"].isin(pays)]


    if pathname == "/":
        
        if graphique == 2:
            # Titre2
            title2 = "nombre total de personnes blessées à cause du terrorisme"

            total_blesses = df["Nombre de blessés"].sum()
            # ligne 0
            
                
            return dbc.Col(make_metrics(title2, total_blesses), width=11, id = "2")
            
        elif graphique == 3:
            # ligne 2
            
                
            return dbc.Col(make_graphics(*nmb.graphique_1(df)), width=11, id = "3")
            
        elif graphique == 4:
            # ligne 3
            
                
            return dbc.Col(make_graphics(*nmb.graphique_2(df)), width=11, id = "4")
            
        elif graphique == 5:
            # ligne 4
            
                
            return dbc.Col(make_graphics(*nmb.graphique_12(df)), width=11, id = "5")
            
        elif graphique == 6:
            # ligne 5
            
                
            return dbc.Col(make_graphics(*nmb.graphique_13(df)), width=11, id = "6")
            
        elif graphique == 7:
            # ligne 6
            
                
            return dbc.Col(make_graphics(*nmb.graphique_3(df)), width=11, id = "7")
            
        elif graphique == 8:
            # ligne 7
            
                
            return dbc.Col(make_graphics(*nmb.graphique_4(df)), width=11, id = "8")
            
        elif graphique == 9:
            # ligne 8
            
                
            return dbc.Col(make_graphics(*nmb.graphique_5(df)), width=11, id = "9")
            
        elif graphique == 10:
            # ligne 9
            
                
            return dbc.Col(make_graphics(*nmb.graphique_6(df)), width=11, id = "10")
            
            
        elif graphique == 11:
            # ligne 10
            
                
            return dbc.Col(make_graphics(*nmb.graphique_7(df)), width=11, id = "11")
            
        elif graphique == 12:
        
            return dbc.Col(make_graphics(*nmb.graphique_8(df)), width=11, id = "12")
        
        # Titre1
        title1 = "nombre total de personnes mortes à cause du terrorisme"

        # Calcul du nombre total de morts enregistrés
        total_morts = df["Nombre de morts"].sum()
        # ligne 0
        return dbc.Col(make_metrics(title1, total_morts), width=11, id = "1")
            

    elif pathname == "/page-1":
        
         
        if graphique == 2:
            
            # ligne 2
            
                
            return dbc.Col(make_graphics(*tc.graphique_2(df)), width = 11, id = "2")
        
        
        # ligne 3
        elif graphique == 3:
            
            return dbc.Col(make_graphics(*tc.graphique_3(df)), width = 11, id = "3")
            
                
        return dbc.Col(make_graphics(*tc.graphique_1(df)), width = 11, id = "1")
           
        
        
    elif pathname == "/page-2":
      
            
            
        if graphique == 2:
            # ligne 2
            
                
            return dbc.Col(make_graphics(*ta.graphique_2(df)), width = 11, id = "2")
            
        elif graphique == 3:
        
            # ligne 3
            
                
            return dbc.Col(make_graphics(*ta.graphique_3(df)), width = 11, id = "3")
            
        elif graphique == 4:
        # ligne 4
        
            return dbc.Col(make_graphics(*ta.graphique_4(df)), width = 11, id = "4")
        return dbc.Col(make_graphics(*ta.graphique_1(df)), width = 11, id = "1")
        
  
    elif pathname == "/page-3":
        
        if graphique == 2:
            
            # ligne 1
            return dbc.Col(make_graphics(*edp.graphique_2(df)), width = 11, id = "2")
        
        elif graphique == 3:
            return dbc.Col(make_graphics(*edp.graphique_3(df)), width = 11, id = "3")  # type: ignore
            
            
        return dbc.Col(make_graphics(*edp.graphique_1(df)), width = 11, id = "1")
        
      
    elif pathname == "/page-4":
        
        # dbc.Col(make_graphics(*ta.graphique_2(df)), width = 5)
        if graphique == 2:
            # ligne 2
            return dbc.Col(make_graphics(*gt.graphique_2(df)), width = 11, id = "2")
            # dbc.Col(make_graphics(*ta.graphique_2(df)), width = 5)
        
        elif graphique == 3:
            return dbc.Col(make_graphics(*gt.graphique_3(df)), width = 11, id = "3")
        
        return dbc.Col(make_graphics(*gt.graphique_1(df)), width = 11, id = "1")
        

    elif pathname == "/page-5":
      
      
        if graphique == 2:
            # ligne 1
            
            return dbc.Col(make_graphics(*aa.graphique_2(df)), width = 11, id = "2"),
     
        return dbc.Col(make_graphics(*aa.graphique_1(df)), width = 11, id = "1"),   
            
         # dbc.Col(make_graphics(*ta.graphique_2(df)), width = 5)
        
    elif pathname == "/page-6":
       
        # ligne 1
        return dbc.Col(make_graphics(*mr.graphique_1(df)), width = 11, id = "1"),
         # dbc.Col(make_graphics(*ta.graphique_2(df)), width = 5)
      

    elif pathname == "/page-7":
        
        
        if graphique == 2:
            # ligne 2
            
            return dbc.Col(make_tables(*dp.graphique_2(df)), width = 11, id = "2")
        
        return dbc.Col(make_tables(*dp.graphique_1(df)), width = 11, id = "1")
        
            

    elif pathname == "/page-8":
        
     
        if graphique == 2:
            # ligne 2
            
            return dbc.Col(make_graphics(*asu.graphique_2(df)), width = 11, id = "2")
        
        return dbc.Col(make_graphics(*asu.graphique_1(df)), width = 11, id = "1")
        

    elif pathname == "/page-9":
     
        
        if graphique == 2:
            # ligne 2
            
            return dbc.Col(make_graphics(*dr.graphique_2(df)), width = 11, id = "2")
            
                
        return dbc.Col(make_graphics(*dr.graphique_1(df)), width = 11, id = "1")
          
            
    
    # S'il y a un problème alors faisont en sort que la page ne change pas d'aspect
    # raise dash.exceptions.PreventUpdate


######


@app.callback(
    Output(component_id="principal-content-2", component_property="children"),
    [
        Input(component_id="url", component_property="pathname")
    ],
    [
        Input(component_id="prediction", component_property="n_clicks"),
        State(component_id="date-single", component_property="date"),
        State(component_id="suicide", component_property="value"),
        State(component_id="attacktype", component_property="value"),
        State(component_id="targtype", component_property="value"),
        State(component_id="natlty", component_property="value"),
        State(component_id="weaptype", component_property="value"),
        State(component_id="pays_", component_property="value"),
        State(component_id="nkill", component_property="value"),
        
        # Input(component_id="choose-number", component_property="value")
    ],
)
def add_prediction(pathname, n, date, suicide, attacktype, targtype, natlty, weaptype, country, nkill):
    
    date = pd.to_datetime(date)
    if pathname == "/page-10":
        return make_metrics(*pred.true_prediction(date.month, date.day, suicide, attacktype, targtype, natlty, weaptype, country, nkill))  # type: ignore
    

# =========================================================================

# Activons l'application sur le port 4000
if __name__ == "__main__":
    app.run_server(port=4000, debug=True)
