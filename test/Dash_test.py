import networkx as nx
import pandas as pd
import numpy as np
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash_table.Format import Format
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import os

dash_app = dash.Dash()
server = dash_app.server
# app = dash_app.server

def get_query_table(i):
    eff_i=df['v'][i]
    return pd.DataFrame.from_dict({'x':np.linspace(0,10),'y':np.sin((np.linspace(0,10))*eff_i/2/np.pi)})
def get_second_table_el(i):
    return dash_table.DataTable(
        id='Second_Table',
        columns=[{"name": 'x', "id": 'x'},
                 {"name": 'y', "id": 'y'}
        ],
        data=get_query_table(i).to_dict('records'),
        style_table={'overflowY': 'scroll','maxHeight': '300px'})
def get_plot(i):
    eff_i=df['v'][i]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=np.linspace(0,10), y=np.sin((np.linspace(0,10))*eff_i/2/np.pi),
                        mode='lines',
                        name='sine'))
    fig.update_layout(title=str(eff_i))
    return fig

df=pd.DataFrame.from_dict({'x':np.linspace(1,10,10),'y':np.linspace(1,10,10),'v':np.random.rand(10)*20})
trace = go.Scatter(
    x=df['x'], y=df['y'],
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='viridis',
        reversescale=True,
        colorbar=dict(
            title='Trend Strenght',
            xanchor='left',
            titleside='right'
        ),
        line_width=0,
        opacity=1.))
trace.marker.color = df['v']
trace.text = df['v']
trace.ids = df['v']
fig = go.Figure(data=trace,
             layout=go.Layout(
                hovermode='closest',
                showlegend=False,
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                dragmode='pan',
                plot_bgcolor= "#ffffff")
                )

Main_table=dash_table.DataTable(
        id='Main_Table',
        columns=[{"name": 'x', "id": 'x', 'deletable': True},
                 {"name": 'y', "id": 'y', 'deletable': True},
                 {"name": 'v', "id": 'v', 'deletable': True}
        ],
        data=df.to_dict('records'))


dash_app.layout = html.Div(children=[
    html.Div(Main_table,style={'width': '40%', 'height':'50%', 'position': 'absolute'}),
    html.Div(get_second_table_el(0),style={'width': '40%', 'height':'50%', 'position': 'absolute','top':'50%'}),
    html.Div(dcc.Graph(figure=fig, id='graph',config={'scrollZoom': True}),style={'width': '50%', 'position': 'relative','left':'50%'}),
    html.Div(dcc.Graph(figure=get_plot(0), id='iot'),style={'width': '50%', 'position': 'relative','left':'50%','top':'50%'})])

@dash_app.callback([
    Output('Second_Table','data'),
    Output('iot','figure')],
    [Input('graph','clickData'),
     Input('Main_Table','active_cell')])
def update(clickData,active_cell):
    print (dash.callback_context.triggered)
    if dash.callback_context.triggered[0]['value'] is None:
        raise PreventUpdate
    elif dash.callback_context.triggered[0]['prop_id']=='graph.clickData':
        new_id=int(dash.callback_context.triggered[0]['value']['points'][0]['pointNumber'])
    elif dash.callback_context.triggered[0]['prop_id']=='Main_Table.active_cell':
        new_id=active_cell['row']
    return get_query_table(new_id).to_dict('records'),get_plot(new_id)


if __name__ == '__main__':
    dash_app.run_server(host='0.0.0.0', port=8080, debug=True)

