import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import base64
import io
import plotly.graph_objs as go
import pandas as pd
import dash_table


"""
---------------------------------------------------------------------
Initializing the web app
---------------------------------------------------------------------
"""

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title = "Trainingszeiten"

app.layout = html.Div(className="customcss",
                      children=[
                          html.H1(children='TT Zeiten Auswertung'),

                          html.Div(children='''
                        Hier bitte die Exceldatei für den jeweiligen Tag hochladen
                      '''),
                          html.Hr(),
                          # dropdown menu
                          dcc.Dropdown(
                                    id='my-dropdown',
                                    options=[
                                        {'label': 'Tabelle anzeigen', 'value': 'table'},
                                        {'label': 'Liste der Fehlstunden anzeigen', 'value': 'list'},
                                        {'label': 'Diagramm der Fehlstunden anzeigen', 'value': 'dia'},
                                        {'label': 'Woche - Liste der Fehlstunden anzeigen', 'value': 'wlist'},
                                        {'label': 'Woche - Diagramm der Fehlstunden anzeigen', 'value': "wdia"}
                                    ],
                                    clearable=False,
                                    placeholder="Bitte Darstellungsformat wählen"
                                    ),
                          html.Div(id='output-container'),
                          html.Hr(),
                          # upload field
                          dcc.Upload(
                                id='upload-data',
                                children=html.Div([
                                    'Datei hier draufziehen oder ',
                                    html.A('aussuchen')
                                ],

                                    id="uploadedcontent"),

                                style={
                                    'width': '100%',
                                    'height': '60px',
                                    'lineHeight': '60px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                    },
                                # Allow multiple files to be uploaded
                                multiple=True
                            ),
                          # graph/table/list field
                          html.Div(id='output-data-upload')
                      ])

"""
---------------------------------------------------------------------
parse functions for loading the data into a pandas dataframe
---------------------------------------------------------------------
"""


def parse_contents_dia(contents, filename,):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            raise FileTypeError(filename)
    except FileTypeError as fte:
        y = str(fte).split(".")
        return html.Div([
                html.Hr(),
                html.H4(
                    "Bitte eine Datei vom Typ .xls, .xlsx oder .csv benutzen. Andere Dateiformate wie"
                    " .{} werden nicht unterstützt".format(
                        y[len(y) - 1].replace("\'", "").replace("\"", "")))
            ])
    except Exception as e:
        return html.Div([
            html.Hr(),
            'There was an error processing this file. -- {}'.format(e)
        ])
    return html.Div([
        html.Hr(),  # horizontal line
        # html.H5(filename.replace(".xlsx", "")),
        auswertung_dia(df, filename),
        html.Hr(),


    ])


def parse_contents_table(contents, filename,):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            raise FileTypeError(filename)
    except FileTypeError as fte:
        y = str(fte).split(".")
        return html.Div([
                html.Hr(),
                html.H4(
                    "Bitte eine Datei vom Typ .xls, .xlsx oder .csv benutzen. Andere Dateiformate wie .{} werden nicht "
                    "unterstützt".format(
                        y[len(y) - 1].replace("\'", "").replace("\"", "")))
            ])
    except Exception as e:
        return html.Div([
            html.Hr(),
            'There was an error processing this file. -- {}'.format(e)
        ])
    return html.Div([
        html.Hr(),  # horizontal line
        html.H5(filename.replace(".xlsx", "")),
        auswertung_table(df),
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),
        html.Hr(),


    ])


def parse_contents_list(contents, filename,):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            raise FileTypeError(filename)
    except FileTypeError as fte:
        y = str(fte).split(".")
        return html.Div([
                html.Hr(),
                html.H4(
                    "Bitte eine Datei vom Typ .xls, .xlsx oder .csv benutzen. Andere Dateiformate wie .{} werden nicht "
                    "unterstützt".format(
                        y[len(y) - 1].replace("\'", "").replace("\"", "")))
            ])
    except Exception as e:
        return html.Div([
            html.Hr(),
            'There was an error processing this file. -- {}'.format(e)
        ])
    return html.Div([
        html.Hr(),  # horizontal line
        html.H5(filename.replace(".xlsx", "")),
        auswertung_list(df),
        html.Hr(),


    ])


def parse_contents_wlist(contents, filename,):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            raise FileTypeError(filename)
    except FileTypeError as fte:
        y = str(fte).split(".")
        return html.Div([
                html.Hr(),
                html.H4(
                    "Bitte eine Datei vom Typ .xls, .xlsx oder .csv benutzen. Andere Dateiformate wie .{} werden nicht "
                    "unterstützt".format(
                        y[len(y) - 1].replace("\'", "").replace("\"", "")))
            ])
    except Exception as e:
        return html.Div([
            html.Hr(),
            'There was an error processing this file. -- {}'.format(e)
        ])
    return html.Div([
        html.Hr(),  # horizontal line
        html.H5(filename.replace(".xlsx", "")),
        auswertung_wlist(df),
        html.Hr(),


    ])


def parse_contents_wdia(contents, filename,):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            raise FileTypeError(filename)
    except FileTypeError as fte:
        y = str(fte).split(".")
        return html.Div([
            html.Hr(),
            html.H4("Bitte eine Datei vom Typ .xls, .xlsx oder .csv benutzen. Andere Dateiformate wie .{} werden nicht "
                    "unterstützt".format(y[len(y) - 1].replace("\'", "").replace("\"", "")))
        ])
    except Exception as e:
        return html.Div([
            html.Hr(),
            'There was an error processing this file. -- {}'.format(e)
        ])
    return html.Div([
        html.Hr(),  # horizontal line
        auswertung_wdia(df, filename),
        html.Hr(),


    ])


"""
---------------------------------------------------------------------
functions for choosing/calling the parse function with contents
---------------------------------------------------------------------
"""


def table(list_of_contents, list_of_names,):
    children = [
        parse_contents_table(c, n, ) for c, n, in
        zip(list_of_contents, list_of_names,)]
    return [children, list_of_names]


def dia(list_of_contents, list_of_names,):
    children = [
        parse_contents_dia(c, n,) for c, n, in
        zip(list_of_contents, list_of_names,)
    ]
    return [children, list_of_names]


def xlist(list_of_contents, list_of_names,):
    children = [
        parse_contents_list(c, n,) for c, n, in
        zip(list_of_contents, list_of_names,)
    ]
    return [children, list_of_names]


def wlist(list_of_contents, list_of_names,):
    children = [
        parse_contents_wlist(c, n,) for c, n, in
        zip(list_of_contents, list_of_names,)
    ]
    return [children, list_of_names]


def wdia(list_of_contents, list_of_names,):
    children = [
        parse_contents_wdia(c, n,) for c, n, in
        zip(list_of_contents, list_of_names,)
    ]
    return [children, list_of_names]


def default():
    return [html.H4("Bitte ein Darstellungsformat auswählen"), html.Div([
        'Datei hier draufziehen oder ',
        html.A('aussuchen')
    ])]


"""
---------------------------------------------------------------------
callback from the web app with information (content, style selection (value), etc...)
---------------------------------------------------------------------
"""


@app.callback([Output('output-data-upload', 'children'), Output("uploadedcontent", "children")],
              [Input('upload-data', 'contents'), Input('my-dropdown', 'value')],
              [State('upload-data', 'filename')
               ])
def update_output(list_of_contents, value, list_of_names,):
    if list_of_contents is not None:
        switcher = {
            "table": table(list_of_contents, list_of_names,),
            "dia": dia(list_of_contents, list_of_names,),
            "list": xlist(list_of_contents, list_of_names,),
            "wlist": wlist(list_of_contents, list_of_names,),
            "wdia": wdia(list_of_contents, list_of_names,),
            None: default()
        }

        func = switcher.get(value)
        return func
    else:
        return [html.Div(), html.Div([
            'Datei hier draufziehen oder ',
            html.A('aussuchen')
            ])]


"""
---------------------------------------------------------------------
functions for processing and visualizing the loaded data
---------------------------------------------------------------------
"""


def auswertung_table(dataframe):
    count = str(dataframe.count())
    count_list = count.split()
    num_rows = count_list[1]
    finalstring = ""
    for row in range(0, int(num_rows)):
        for col in list(dataframe.columns):
            finalstring += str(dataframe.iloc[row][col]) + " "
        finalstring += "| "
    pass
    # return html.Div([html.H5(finalstring), html.H3(cols[:2])])


def auswertung_dia(df, filename):
    count = str(df.count())
    count_list = count.split()
    num_rows = int(count_list[1])
    cols = list(df.columns)
    storage = [[0] * num_rows, [0] * num_rows, [""] * num_rows]
    cut_storage = [[0] * num_rows, [0] * num_rows, [""] * num_rows]

    # load values into storage
    for row in range(num_rows):
        for col in cols[2:]:
            if df.iloc[row][col] == "w" or df.iloc[row][col] == "abwesend":
                storage[0][row] += 1
            elif df.iloc[row][col] == "e" or df.iloc[row][col] == "entschuldigt":
                storage[1][row] += 1
        for col in cols[:2]:
            storage[2][row] += df.iloc[row][col] + " "

    # clear double names in storage
    for n in range(num_rows):
        double = False
        for i in range(num_rows):
            if i == n:
                break
            if storage[2][n] == storage[2][i]:
                cut_storage[2][i] = storage[2][n]
                cut_storage[1][i] = storage[1][n] + storage[1][i]
                cut_storage[0][i] = storage[0][n] + storage[0][i]
                storage[2][n] = ""
                storage[1][n] = 0
                storage[0][n] = 0
                double = True
        if not double:
            cut_storage[2][n] = storage[2][n]
            cut_storage[1][n] = storage[1][n]
            cut_storage[0][n] = storage[0][n]

    # determine numbers of not empty names in storage
    num_names = 0
    for n in range(num_rows):
        if cut_storage[2][n] != "":
            num_names += 1
    filled_storage = [[0] * num_names, [0] * num_names, [""] * num_names]
    sorted_storage = [[0] * num_names, [0] * num_names, [""] * num_names]

    # clear storage from empty names
    position = 0
    for n in range(num_rows):
        if cut_storage[2][n] != "":
            filled_storage[2][position] = cut_storage[2][n]
            filled_storage[1][position] = cut_storage[1][n]
            filled_storage[0][position] = cut_storage[0][n]
            position += 1

    # sorting algorithm
    for n in range(num_names):
        max_num = 0
        who = 0
        for i in range(num_names):
            if cut_storage[0][i] + cut_storage[1][i] >= max_num and cut_storage[2][i] != "":
                max_num = cut_storage[0][i] + cut_storage[1][i]
                who = i
        sorted_storage[0][num_names - n - 1] = cut_storage[0][who]
        sorted_storage[1][num_names - n - 1] = cut_storage[1][who]
        sorted_storage[2][num_names - n - 1] = cut_storage[2][who]
        cut_storage[0][who] = 0
        cut_storage[1][who] = 0
        cut_storage[2][who] = ""

    trace1 = go.Bar(
        hoverinfo='none',
        y=sorted_storage[2],
        x=sorted_storage[0],
        name='Anzahl unentschuldigte Tage',
        orientation='h',
        marker=dict(
            color='rgba(255, 0, 0, 0.7)',
            line=dict(
                color='rgba(255, 0, 0, 1.0)',
                width=3)
        )
    )
    trace2 = go.Bar(
        hoverinfo='none',
        y=sorted_storage[2],
        x=sorted_storage[1],
        name='Anzahl entschuldigte Tage',
        orientation='h',
        marker=dict(
            color='rgba(249, 246, 39, 0.6)',
            line=dict(
                color='rgba(249, 246, 39, 1.0)',
                width=3)
        )
    )
    height = (30 * len(sorted_storage[0]))
    data = [trace1, trace2]
    layout = go.Layout(
        title=filename.replace(".xlsx", ""),
        barmode='stack',
        autosize=True,
        height=height,
        yaxis=go.layout.YAxis(automargin=True),
        xaxis=dict(dtick=1)
    )
    return html.Div([dcc.Graph(id="dia-graph", figure=go.Figure(data=data, layout=layout))])


def auswertung_list(df):
    count = str(df.count())
    count_list = count.split()
    num_rows = int(count_list[1])
    cols = list(df.columns)
    storage = [None] * num_rows
    cut_storage = [None] * num_rows
    for i in range(num_rows):
        storage[i] = [0, 0, ""]
        cut_storage[i] = [0, 0, ""]

    # load values into storage
    for row in range(num_rows):
        for col in cols[2:]:
            if df.iloc[row][col] == "w" or df.iloc[row][col] == "abwesend":
                storage[row][0] += 1
            elif df.iloc[row][col] == "e" or df.iloc[row][col] == "entschuldigt":
                storage[row][1] += 1
        for col in cols[:2]:
            storage[row][2] += df.iloc[row][col] + " "

    # clear double names in storage
    for n in range(num_rows):
        double = False
        for i in range(num_rows):
            if i == n:
                break
            if storage[n][2] == storage[i][2]:
                cut_storage[i][2] = storage[n][2]
                cut_storage[i][1] = storage[n][1] + storage[i][1]
                cut_storage[i][0] = storage[n][0] + storage[i][0]
                storage[n][2] = ""
                storage[n][1] = 0
                storage[n][0] = 0
                double = True
        if not double:
            cut_storage[n][2] = storage[n][2]
            cut_storage[n][1] = storage[n][1]
            cut_storage[n][0] = storage[n][0]

    # determine numbers of not empty names in storage
    num_names = 0
    for n in range(num_rows):
        if cut_storage[n][2] != "":
            num_names += 1
    filled_storage = [None] * num_names
    sorted_storage = [None] * num_names
    for i in range(num_names):
        filled_storage[i] = [0, 0, ""]
        sorted_storage[i] = ["", "", 0, 0]

    # clear storage from empty names
    position = 0
    for n in range(num_rows):
        if cut_storage[n][2] != "":
            filled_storage[position][2] = cut_storage[n][2]
            filled_storage[position][1] = cut_storage[n][1]
            filled_storage[position][0] = cut_storage[n][0]
            position += 1

    # sorting algorithm
    for n in range(num_names):
        max_num = 0
        who = 0
        for i in range(num_names):
            if filled_storage[i][0] + filled_storage[i][1] >= max_num and filled_storage[i][2] != "":
                max_num = filled_storage[i][0] + filled_storage[i][1]
                who = i
        name = filled_storage[who][2].split()
        sorted_storage[n][0] = name[1]
        sorted_storage[n][1] = name[0]
        sorted_storage[n][2] = filled_storage[who][0]
        sorted_storage[n][3] = filled_storage[who][1]
        filled_storage[who][0] = 0
        filled_storage[who][1] = 0
        filled_storage[who][2] = ""

    dfobj = pd.DataFrame(sorted_storage, columns=["Vorname", "Nachname", "Anzahl unentschuldigte Tage",
                                                  "Anzahl entschuldigte Tage"])
    return dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in dfobj.columns],
        data=dfobj.to_dict('records'),
    )

def auswertung_wlist(df):
    count = str(df.count())
    count_list = count.split()
    num_cols = int((len(count_list) - 6) / 3 + 2)
    num_rows = int(count_list[1])
    cols = list(df.columns)
    storage = [None] * num_cols
    sorted_storage = [None] * (num_cols - 2)
    for i in range(2, num_cols):
        storage[i] = [0, 0, ""]
    for i in range(0, num_cols - 2):
        sorted_storage[i] = ["", 0, 0]
    for col in range(2, num_cols):
        for row in range(num_rows):
            if df.iloc[row][cols[col]] == "w" or df.iloc[row][cols[col]] == "abwesend":
                storage[col][0] += 1
            elif df.iloc[row][cols[col]] == "e" or df.iloc[row][cols[col]] == "entschuldigt":
                storage[col][1] += 1
        storage[col][2] = cols[col]

    for n in range(2, num_cols):
        max_num = 0
        who = 0
        for i in range(2, num_cols):
            if storage[i][0] + storage[i][1] >= max_num and storage[i][2] != "":
                max_num = storage[i][0] + storage[i][1]
                who = i

        sorted_storage[n - 2][0] = storage[who][2]
        sorted_storage[n - 2][1] = storage[who][0]
        sorted_storage[n - 2][2] = storage[who][1]
        storage[who][0] = 0
        storage[who][1] = 0
        storage[who][2] = ""
    dfobj = pd.DataFrame(sorted_storage, columns=["Woche", "Anzahl unentschuldigte Tage", "Anzahl entschuldigte Tage"])
    return dash_table.DataTable(
        id='wtable',
        columns=[{"name": i, "id": i} for i in dfobj.columns],
        data=dfobj.to_dict('records'),
    )


def auswertung_wdia(df, filename):
    count = str(df.count())
    count_list = count.split()
    num_cols = int((len(count_list) - 6) / 3 + 2)
    num_rows = int(count_list[1])
    cols = list(df.columns)
    storage = [None] * num_cols
    sorted_storage = [None] * (num_cols - 2)
    for i in range(2, num_cols):
        storage[i] = [0, 0, ""]
    for i in range(0, num_cols - 2):
        sorted_storage[i] = ["", 0, 0]

    # load values into storage
    for col in range(2, num_cols):
        for row in range(num_rows):
            if df.iloc[row][cols[col]] == "w" or df.iloc[row][cols[col]] == "abwesend":
                storage[col][0] += 1
            elif df.iloc[row][cols[col]] == "e" or df.iloc[row][cols[col]] == "entschuldigt":
                storage[col][1] += 1
        storage[col][2] = cols[col]

    # sorting algorithm
    for n in range(2, num_cols):
        max_num = 0
        who = 0
        for i in range(2, num_cols):
            if storage[i][0] + storage[i][1] >= max_num and storage[i][2] != "":
                max_num = storage[i][0] + storage[i][1]
                who = i

        sorted_storage[n - 2][0] = storage[who][2]
        sorted_storage[n - 2][1] = storage[who][0]
        sorted_storage[n - 2][2] = storage[who][1]
        storage[who][0] = 0
        storage[who][1] = 0
        storage[who][2] = ""
    transformed_storage = [[0] * (num_cols - 2), [0] * (num_cols - 2), [""] * (num_cols - 2)]
    for n in range(len(sorted_storage)):
        for i in range(len(sorted_storage[n])):
            transformed_storage[i][len(sorted_storage)- n - 1] = sorted_storage[n][i]
    trace1 = go.Bar(
        hoverinfo='none',
        y=transformed_storage[0],
        x=transformed_storage[1],
        name='Anzahl unentschuldigte Personen',
        orientation='h',
        marker=dict(
            color='rgba(255, 0, 0, 0.7)',
            line=dict(
                color='rgba(255, 0, 0, 1.0)',
                width=3)
        )
    )
    trace2 = go.Bar(
        hoverinfo='none',
        y=transformed_storage[0],
        x=transformed_storage[2],
        name='Anzahl entschuldigte Personen',
        orientation='h',
        marker=dict(
            color='rgba(249, 246, 39, 0.6)',
            line=dict(
                color='rgba(249, 246, 39, 1.0)',
                width=3)
        )
    )
    height = (100 * len(transformed_storage[0]))
    data = [trace1, trace2]
    layout = go.Layout(
        title=filename.replace(".xlsx", ""),
        barmode='stack',
        autosize=True,
        height=height,
        yaxis=go.layout.YAxis(automargin=True),
        xaxis=dict(dtick=1)
    )
    return html.Div([dcc.Graph(id="dia-graph", figure=go.Figure(data=data, layout=layout))])


"""
---------------------------------------------------------------------
Custom exceptions
---------------------------------------------------------------------
"""

# exception for wrong file format


class FileTypeError(Exception):
    def __init__(self, filename):
        self.filename = filename


# if executed directly turn debug mode on

if __name__ == '__main__':
    app.run_server(debug=True)
