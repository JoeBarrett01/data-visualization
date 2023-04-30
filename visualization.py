import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objs as go
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import numpy as np
import statsmodels.api as sm
from statsmodels.nonparametric.smoothers_lowess import lowess
from scipy.interpolate import CubicSpline

# Load data
df = pd.read_csv(
    "https://raw.githubusercontent.com/JoeBarrett01/data-visualization/main/lancaster-contacts-data-store-2021-10-15.csv")

newdf = df[['Search Consent Given?',
            'Race',
            'Search Basis: Officer Safety/Safety of Others?',
            'Search Basis: Search Warrant?',
            'Search Basis: Condition of Parole/Probation/PRCS/Mandatory Supervision?',
            'Search Basis: Suspected Weapons?',
            'Search Basis: Visible Contraband?',
            'Search Basis: Odor of Contraband?',
            'Search Basis: Canine Detection?',
            'Search Basis: Evidence of Crime?',
            'Search Basis: Incident to Arrest?',
            'Search Basis: Exigent Circumstances/Emergency?',
            'Search Basis: Vehicle inventory?',
            'Search Basis: Suspected of Violating of School Policy?',
            'Contraband Evidence Discovered: Suspected Stolen Property?',
            'NUMBER_OF_MINUTES',
            'Lat',
            'Lng'
            ]]

color_scale = [(0, 'orange'), (1, 'red')]


# initialize app:
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Lancaster Search Consent App"

# app layout:
app.layout = html.Div([
    # header:
    dbc.Container([
        dbc.Row([
        dbc.Col([
            html.H3(
                ['Search Consent Prior to Arrest in Lancaster, California (USA)'])
        ], className='fs-2')
    ], className='py-4 my-2 text-center bg-white')
    ]),

    dbc.Container([
        dbc.Row([
            # drop down:
            dbc.Col([
                dcc.Dropdown(
                    id='dropdown',
                    options=[
                        {'label': col, 'value': col} for col in newdf.columns if col not in ['Lat', 'Lng', 'Race']
                    ],
                    value='Search Consent Given?',
                    clearable=False,
                    className='dropdown'
                )
            ], width=12),
            
            # scatter plot:
            dbc.Col([
                dcc.Graph(
                    id='scatter_plot',
                    figure={}
                )
            ], width=12),

            # histogram:
            dbc.Col([
                dcc.Graph(
                    id='distribution_graph',
                    figure={}
                )
            ], width=12)
        ], className='py-3')
    ], className='border border-2 border-light bg-white')
])

# Update scatter plot and distribution graph when dropdown is changed
@app.callback(
    [Output('scatter_plot', 'figure'), Output('distribution_graph', 'figure')],
    [Input('dropdown', 'value'), Input('scatter_plot', 'hoverData')]
)
def update_figure(selected_column, hoverData):
    filtered_df = newdf[newdf[selected_column]]

    # Create scatter plot
    color_scale = [(0, 'orange'), (1, 'red')]
    fig = px.scatter_mapbox(
        filtered_df,
        lat="Lat",
        lon="Lng",
        hover_name="Race",
        hover_data=newdf.columns,
        color="Search Basis: Search Warrant?",
        color_continuous_scale=color_scale,
        size="NUMBER_OF_MINUTES",
        zoom=10,
        height=600,
    )

    fig.update_layout(mapbox_style="open-street-map", showlegend=True)

    fig.add_annotation(
        x=.5,  
        y=-0.15,  
        xref='paper',  
        yref='paper',  
        text="Note: Larger circle = longer arrest time",  # text to be displayed
        showarrow=True,  # do not display an arrow
        font=dict(size=12)  # set the font size of the text
    )
    # Create distribution graph
    hist_data = [filtered_df['NUMBER_OF_MINUTES']]
    group_labels = ['distplot'] # name of the dataset

    dist_fig = ff.create_distplot(hist_data, group_labels, show_rug=False)
    dist_fig.update_layout(
        title_text='Distribution of NUMBER_OF_MINUTES',
        xaxis_title='Minutes',
        yaxis_title="Distribution",
    )

    # Add red dot on the smoother curve when a Lat/Lng is hovered
    if hoverData is not None:
        lat = hoverData['points'][0]['lat']
        lon = hoverData['points'][0]['lon']

        fig.add_trace(
            go.Scattermapbox(
                lat=[lat],
                lon=[lon],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=14,
                    color='red',
                    opacity=0.7
                ),
                name='Selected point'
            )
        )

        # Add a vertical line to the distribution plot at the x-coordinate of the selected point
        selected_row = filtered_df[(filtered_df['Lat'] == lat) & (filtered_df['Lng'] == lon)]
        if not selected_row.empty:
            selected_minutes = selected_row['NUMBER_OF_MINUTES'].iloc[0]
            dist_fig.add_trace(
                go.Scatter(
                    x=[selected_minutes, selected_minutes],
                    y=[0, 0.7],
                    mode='lines',
                    line=dict(color='red', width=3, dash='dash'),
                    name='Selected point'
                )
        )

    return fig, dist_fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8054)
