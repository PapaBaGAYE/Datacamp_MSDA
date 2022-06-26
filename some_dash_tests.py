import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


mois_lettres = [
    "Janvier",
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
    "Decembre",
]

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.LITERA],
)


def changer_mois_ch(colonne):
    mois_lettres = [
        "Janvier",
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
        "Decembre",
    ]
    # print(colonne-1)
    return mois_lettres[colonne - 1]


def recup_and_process_data():
    try:
        df = pd.read_csv("data/cleaned/terror.csv")

        # print(df.dtypes)
        # regroupons les données par pays, année et mois
        df: pd.DataFrame = df.groupby(["country_txt", "iyear"], as_index=False).sum(
            "nkill"
        )

        df.rename(
            columns={
                "country_txt": "Pays",
                "nkill": "Nombre de morts",
                "iyear": "Année",
            },
            inplace=True,
        )

        fig = px.choropleth(
            df,
            locations="Pays",
            locationmode="country names",
            featureidkey="properties.name",
            color="Nombre de morts",
            color_continuous_scale="YlOrRd",
            scope="world",
            hover_name="Pays",
        )
        fig.update_layout(margin={"l": 0, "r": 0, "t": 0, "b": 0})

        fig.update_layout(
            dict(
                title=dict(
                    text="Animation par année de la représentation géographique du nombre de morts par pays"
                )
            )
        )

        return fig

    except Exception as e:
        print(f"Error occured {e}")


app.layout = html.Div(
    [
        html.H4(
            "Tache de visualisation",
            className="display-5 bg-light text-center",
            style={"padding": "2rem", "margin-bottom": "2rem"},
        ),
        dbc.Container(
            dbc.Card(
                dbc.CardBody(dcc.Graph(figure=recup_and_process_data(), id="graphic")),
                className="bg-light",
            )
        ),
    ]
)

if __name__ == "__main__":
    print("port 8050")
    app.run_server(debug=True)
