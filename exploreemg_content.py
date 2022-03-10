from cProfile import label
from re import template
from dash import html, dcc, callback, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pipeline
import utils

datapath = ""
filename = "emg_example1.csv"
df, time_array = pipeline.import_emg(filename=filename)
exploreemg_content = html.Div([
    dcc.Store(id="df"),
    dcc.Store(id="current_emg_signal"),
    dcc.Store(id="time_array"),
    html.H1("Explore EMG"),
    html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files'),
            ]),
            filename=filename,
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
                df.columns[1],
                id='muscle_to_plot',
                style={'margin': '5px 5px'}

            ),
            html.Div([
                html.P("Acquisition frequency (Hz):", style={
                       'width': '49%', 'display': 'inline-block'}),
                dcc.Input(
                    id='acq_freq',
                    type='number',
                    value=2000,
                    style={'width': '49%', 'display': 'inline-block'}
                )
            ]),
            dcc.RadioItems(
                options=[
                    {'label': 'Rectified', 'value': 1},
                    {'label': 'Non-Rectified', 'value': 0}],
                value=1,
                id='rectified',
                labelStyle={'display': 'inline-block',
                            'marginTop': '5px', 'marginLeft': '5px'}
            ),
            dcc.RadioItems(
                options=[
                    {'label': 'Centered', 'value': 1},
                    {'label': 'Non-Centered', 'value': 0}],
                value=1,
                id='centered',
                labelStyle={'display': 'inline-block',
                            'marginTop': '5px', 'marginLeft': '5px'}
            )
        ],
            style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.H4("Band-pass filter (Hz)"),
            dcc.RangeSlider(
                40,
                500,
                5,
                value=[100, 300],
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True},
                id='band-pass-filter-freqs',
            ),
            html.H4("Low-pass filter (Hz)"),
            dcc.Slider(
                2,
                30,
                1,
                value=8,
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True},
                id='low-pass-filter-freq',
            ),
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'padding': '5px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='emg_graph',
            # hoverData={'points': [{'customdata': 'Japan'}]}
            figure=go.Figure(
                data=go.Scatter(x=time_array, y=df.iloc[:, 2]),
                layout=go.Layout(
                    xaxis={
                        'rangeslider': {'visible': True},
                        'rangeselector': {'visible': True}
                    },
                    template='simple_white'
                )
            ),
            style={'height': '80vh'}
        )
    ], style={'width': '100%', 'height': '700', 'display': 'inline-block', 'padding': '0px 0px', 'margin': '0px 0px'}),

])


@ callback([
    Output('df', 'data'),
    Output('time_array', 'data')],
    Input('upload-data', 'filename'),

)
def load_data(filename):
    df, time = pipeline.import_emg(filename)

    return df.to_dict(), time

# see dcc.Store


@callback(
    Output("current_emg_signal", "data"),
    Input("muscle_to_plot", "value"),
    Input("df", "data")
)
def select_muscle(muscle_to_plot, df):
    df = pd.DataFrame.from_dict(df)
    return np.array(df[muscle_to_plot])


@ callback(
    Output('emg_graph', 'figure'),
    Input('current_emg_signal', 'data'),
    Input('acq_freq', 'value'),
    Input('band-pass-filter-freqs', 'value'),
    Input('low-pass-filter-freq', 'value'),
    Input('centered', 'value'),
    Input('rectified', 'value'),
    State('time_array', 'data')
)
def update_graph(emg_signal, acq_freq, band_pass_freq, low_pass_freq, centered, rectified, time_array):
    emg_signal = pd.Series(emg_signal)

    emg_filtered = utils.band_pass(
        emg_signal, acq_freq, band_pass_freq[0], band_pass_freq[1])

    if centered:
        emg_signal = emg_signal-emg_signal.mean()
    if rectified:
        emg_signal = emg_signal.abs()
        emg_filtered = abs(emg_filtered)

    emg_envelope = utils.envelope(emg_filtered, acq_freq, low_pass_freq)

    fig = go.Figure(
        data=go.Scatter(x=time_array, y=emg_signal, name="Raw EMG signal"),
        layout=go.Layout(
            xaxis={
                'rangeslider': {'visible': True},
                'rangeselector': {'visible': True}
            },
            template='simple_white')
    )
    fig.add_scatter(x=time_array, y=emg_filtered,
                    name="Filtered EMG signal", marker={"color": 'black'})
    fig.add_scatter(x=time_array, y=emg_envelope,
                    name="EMG signal envelope", marker={"color": '#e9c46a'})
    return fig
