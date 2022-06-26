# Environment used: dash1_8_0_env
import pandas as pd  # (version 1.0.0)
import plotly  # (version 4.5.0)
import plotly.express as px

import dash  # (version 1.8.0)
from dash import dcc, html

# import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# print(px.data.gapminder()[:15])

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# ------------------------------------------------------------


def make_figure():
    try:
        df = pd.read_csv("data/cleaned/terror.csv")
        # print(df[:3])
        df = df.groupby(["iyear", "country_txt"], as_index=False)["nwound"].sum()

        fig = px.choropleth(
            df,
            locations="country_txt",
            color="nwound",
            hover_name="country_txt",
            projection="natural earth",
            title="Animation annuel du nombre de blessés par pays",
            locationmode="country names",
            animation_frame="iyear",
            color_continuous_scale="peach",
            template="plotly_dark",
        )

        fig.update_layout(
            title=dict(font=dict(size=28), x=0.5, xanchor="center"),
            margin=dict(l=60, r=60, t=50, b=50),
        )

        return fig
    except Exception as e:
        print(f"Exeption {e}")


# ---------------------------------------------------------------
app.layout = html.Div([html.Div([dcc.Graph(id="the_graph", figure=make_figure())])])

# ---------------------------------------------------------------

if __name__ == "__main__":
    app.run_server(debug=True)
