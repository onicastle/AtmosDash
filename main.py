import requests
import os
import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.express as px
import chart_studio.plotly as py

import plotly.figure_factory as ff
def getGrades(filename = None):

    if filename is not None:
        if os.path.isfile(filename):
            return

    url = "https://oiip.uprm.edu/wp-content/uploads/2020/12/Notas-2020-2021.xlsx"
    r = requests.get(url, allow_redirects=True)
    open("Notas-2020-2021.xlsx", "wb").write(r.content)

def set_data_frame(filename = None):

    if filename is not None:
        getGrades(filename)
    labels = [
        'Departamento',
        'Año Acedémico',
        'Asterisco',
        'Facultad',
        'Semestre',
        'S',
        'NS',
        'P'
    ]
    df = pd.read_excel("Notas-2020-2021.xlsx", index_col=False)
    df = df.drop(axis = 1, labels=labels)
    df = df.fillna(value=0)
    df.A = df.A + df.IA
    df.B = df.B + df.IB
    df.C = df.C + df.IC
    df.D = df.D + df.ID
    df.F = df.F + df.IF
    df["Total"] = df.A + df.B + df.C + df.D + df.F
    labels = [
        'I',
        'IA',
        'IB',
        'IC',
        'ID',
        'IF',
    ]
    df = df.drop(labels= labels, axis = 1)
    return df

def generate_table(dataframe, max_rows = 50):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])
def make():
    df = set_data_frame()

    app = dash.Dash(__name__)
    colors = {
        'background': '#111111',
        'text': '#7FDBFF'
    }
    fig = px.bar(
        df,
        x = df.Curso,
        y = df.columns[2:8],
        barmode="group",
        title= "Grade Distribution"
        )


    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    app.layout = html.Div(children=[
        html.H1(children='Atmos Visual'),
        generate_table(df, max_rows= 10),

        html.Div(children='''
            Dash: A web application framework for Python.
        ''', ),

        dcc.Graph(
            id='example-graph',
            figure=fig
        )
    ])

    app.run_server(debug=True)



if __name__ == "__main__":
    make()
