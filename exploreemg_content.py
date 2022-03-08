from cProfile import label
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import pipeline

datapath = ""
# df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')
df = pipeline.import_emg("S5_SE_1_emg.csv")

exploreemg_content = html.Div([
    html.H1("Explore EMG"),
    html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
        )
    ]),
    html.Div([

        html.Div([
            dcc.Dropdown(
                df.columns,
                'bic',
                id='muscle_to_plot',
            ),
            dcc.RadioItems(
                ['Rectified'],
                'Rectified',
                id='rectified',
                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
            ),
            dcc.RadioItems(
                ['Centered'],
                'Centered',
                id='centered',
                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
            )
        ],
            style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                ["[10,450]Hz", "[50,500]Hz"],
                '[10,450]Hz',
                id='crossfilter-yaxis-column',
                # label="Band-pass filter"
            ),
            dcc.Dropdown(
                ["2Hz", "5Hz", "10Hz"],
                '2Hz',
                id='crossfilter-yaxis-column',
                # label="low-pass filter (envelope)"
            ),
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='main_emg_graph',
            # hoverData={'points': [{'customdata': 'Japan'}]}
            figure=go.Figure(
                data=go.Scatter(x=df["time"], y=df["bic"]),
                layout=go.Layout(
                    xaxis={
                        'rangeslider': {'visible': True},
                        'rangeselector': {'visible': True}
                    },
                )
            )
        )
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 5'}),

    # html.Div(dcc.Slider(
    #     df['Year'].min(),
    #     df['Year'].max(),
    #     step=None,
    #     id='crossfilter-year--slider',
    #     value=df['Year'].max(),
    #     marks={str(year): str(year) for year in df['Year'].unique()}
    # ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
])


@ callback(
    Output('crossfilter-indicator-scatter', 'figure'),
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename'),
    Input('crossfilter-xaxis-column', 'value'),
    Input('crossfilter-yaxis-column', 'value'),
    Input('crossfilter-xaxis-type', 'value'),
    Input('crossfilter-yaxis-type', 'value'),
    Input('crossfilter-year--slider', 'value'))
def update_graph(contents, filename, xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = pipeline.import_emg(filename)
    # dff = df[df['Year'] == year_value]

    fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
                     y=dff[dff['Indicator Name'] ==
                           yaxis_column_name]['Value'],
                     hover_name=dff[dff['Indicator Name'] ==
                                    yaxis_column_name]['Country Name']
                     )

    fig.update_traces(
        customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])

    fig.update_xaxes(title=xaxis_column_name,
                     type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title=yaxis_column_name,
                     type='linear' if yaxis_type == 'Linear' else 'log')

    fig.update_layout(
        margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig


def create_time_series(dff, axis_type, title):

    fig = px.scatter(dff, x='Year', y='Value')

    fig.update_traces(mode='lines+markers')

    fig.update_xaxes(showgrid=False)

    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       text=title)

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig


@ callback(
    Output('x-time-series', 'figure'),
    Input('crossfilter-indicator-scatter', 'hoverData'),
    Input('crossfilter-xaxis-column', 'value'),
    Input('crossfilter-xaxis-type', 'value'))
def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    country_name = hoverData['points'][0]['customdata']
    dff = df[df['Country Name'] == country_name]
    dff = dff[dff['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    return create_time_series(dff, axis_type, title)


@ callback(
    Output('y-time-series', 'figure'),
    Input('crossfilter-indicator-scatter', 'hoverData'),
    Input('crossfilter-yaxis-column', 'value'),
    Input('crossfilter-yaxis-type', 'value'))
def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    dff = df[df['Country Name'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['Indicator Name'] == yaxis_column_name]
    return create_time_series(dff, axis_type, yaxis_column_name)
