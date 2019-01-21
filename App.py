# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import base64
from draw_plotly import draw
from settlement import settlement as settl


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop Files: Ctrl + ',
                html.I('"Strains.xlsx"'),
                ' and ',
                html.I('"Settlements.xlsx"'),
                ' (Order Matters!)'
            ]),
            style={
                'width': '1200px',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=True
        ),
        html.Div(id='output-data')
        ]),
        # html.Button('Convert to PDF', id='pdf-button')
])


def parse_contents(contents):
    file_A, file_B = contents
    content_type_A, content_string_A = file_A.split(',')
    content_type_B, content_string_B = file_B.split(',')

    decoded_A = base64.b64decode(content_string_A)
    decoded_B = base64.b64decode(content_string_B)
    try:
        x, y = settl(decoded_A, decoded_B)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    else:
        fig = draw(x, y)
        return html.Div([
            dcc.Graph(
                figure=fig
            )
        ])


@app.callback(
    Output('output-data', 'children'),
    [Input('upload-data', 'contents')]
)
def update_output_div(files):
    if files is not None:
        children = [parse_contents(files)]
        return children


if __name__ == '__main__':
    app.run_server(debug=True)
