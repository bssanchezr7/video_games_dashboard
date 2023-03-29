from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv('./video_games_sales.csv')
df.rename(columns={'na_sales':'north america', 
                   'eu_sales': 'europe', 'jp_sales': 'japan', 
                   'other_sales':'other'}, 
          inplace=True)

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Video Games', style={'textAlign':'center'}, className='title'),
    html.Div(
        dcc.Dropdown(df.genre.unique(), value='Action', id='dropdown-selection'),
        className='options'
    ),
    dcc.Graph(id='bar-content', className='bar'),
    dcc.Graph(id='pie-content', className='pie')
], className='container')

@callback(
    Output('bar-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_bar(value):
    total_sales = (
        df.query(f'genre == "{value}"')
        .groupby(['name'])[['north america', 'europe', 'japan', 'other', 'global_sales']]
        .sum()
        .reset_index()
        .sort_values('global_sales', ascending=False)
        .head(10)
        
    )
    
    fig = px.bar(total_sales, 
             x="name", 
             y=['north america', 'europe', 'japan', 'other'], 
             labels={
                     "value": "Total",
                     "variable": "Paises",
                     "name" : "Juego"
                     
                 },
            )
    fig.update_layout( 
        title={
            'text': "Juegos más vendidos",
            'y':1,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        legend=dict(
            title=None, orientation="h", y=1.02, yanchor="bottom", x=0.5, xanchor="center"
        )
    )
    return fig

@callback(
    Output('pie-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_pie(value):
    name_region = pd.melt(df.query(f'genre == "{value}"'), 
                    id_vars=['name'], 
                    value_vars=['north america', 'europe', 'japan', 'other'],
                    var_name='country', 
                    value_name='sales'
                  )
    name_region = name_region.groupby(['name', 'country'])['sales'].sum().reset_index()
    
    fig = px.pie(name_region, values='sales', names='country')
    fig.update_layout( # customize font and legend orientation & position
        title={
            'text': "Ventas por región",
            'y':1,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        
        legend=dict(
            title=None, orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"
        )
    )

    return fig
    
if __name__ == '__main__':
    app.run_server(debug=True)