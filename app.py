import dash
import pandas as pd 
import dash_table
import dash_core_components as dcc 
import dash_html_components as html 
import plotly.express as px
from dash.dependencies import Input, Output

app = dash.Dash(
    __name__,
    external_stylesheets=['C:/Users/STARTSUPER/Desktop/dash_tutorial/style.css']
    )

colors = {
    'background': '#111111',
    'text': 'white'
}
yt_channel = 'Dave2D'
app.title = f'{yt_channel} channel dashboard'

df = pd.read_csv('C:/Users/STARTSUPER/Desktop/Jupyter/Cleaning_Data/Dave2D.csv')

fig = px.line(df, x="Date", y='View',
              title='Total views by time', color_discrete_sequence=['#05F4B7'], custom_data=['Title'])

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    
    hoverlabel=dict(
        font_size=16,
    ),

    xaxis={
        'showgrid': False,
        'title' : 'Time'
    },
    yaxis={
        'title': 'Views',
        'showgrid':False
    },
    title={
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font' :{
            'size': 25,
            'family': 'Arial'
        }
    }
)

fig.update_traces(
    hovertemplate="<br>".join([
        'Date: <b>%{x}</b>',
        'Total views: <b>%{y:,}</b>',
        'Title: <b>%{customdata[0]}</b>',
    ])      
)

fig2 = px.bar(
    df.sort_values(by=['View'])[-5:],
    orientation='h',
    x='View',
    y='Title',
    text='View',
    title='Top 5 videos with most views',
    color_discrete_sequence=['#05F4B7', '#086972', '#071a52'])

fig2.update_traces(
    texttemplate='%{text:.2s}',
    textposition='inside',
    hovertemplate='Title: <b>%{y}</b> <br>View: <b>%{x:,}</b>', 
)

fig2.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    
    hoverlabel=dict(
        font_size=16,
    ),
    xaxis={
        'showgrid': False,
        'title': 'Views',
    },
    yaxis={
        'title': None,
    },
    title={
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {
            'size': 25,
            'family': 'Arial'}
    },
    
)

fig3 = px.bar(
    df.sort_values(by=['Like'])[-5:],
    orientation='h',
    barmode='group',
    x= ["Like", "Dislike","Comment"],
    y= "Title",
    title="Top 5 videos with most likes",
    color_discrete_sequence=['#05F4B7', '#b31e6f', '#ee5a5a',])

fig3.update_traces(
    texttemplate='%{x:.2s}',
    textposition='inside',
    hovertemplate='Title: <b>%{y}</b> <br>Engagement: <b>%{x:,}</b>',

    
)

fig3.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    legend_title_text='Types of engagement',
    hoverlabel=dict(
        font_size=16,
    ),
    xaxis={
        'showgrid': False,
        'title': 'Number of engagements',
        
    },
    yaxis={
        'title':None,
    },
    legend=dict(
        # yanchor="bottom",
        # y=0.01,
        # xanchor="right",
        # x=0.99,
        title_font_size=8,
        font=dict(
            size=8,
        ),
        itemsizing='trace'
    ),
    title={
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {
            'size': 25,
            'family': 'Arial',
            }
    }
)


app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1(f'{yt_channel} channel dashboard', className='header_title',),
            html.P('Updated 27/2/21', className='header_sub'),
            html.Img(
                src=app.get_asset_url('avatar.jpg'),
                alt='Youtuber Avatar',
                className='avatar',
                style={
                    'display': 'flex', 'vertical-align': 'middle'}
            ),
        ], className='header'),
    ]),

    html.Div([
        html.Div([
            html.P('Total videos puplished', className='P2'),
            html.P(df.Title.count(), className='P1')
        ], className='card', style={'display':'inline-block', 'width':'20%'}),
        
        html.Div([
            html.P('Total views', className='P2'),
            html.P(f'{df.View.sum():,}', className='P1')
        ], className='card', style={'display': 'inline-block', 'width': '20%'}),

        

        html.Div([
            html.P('Average video duration', className='P2'),
            html.P(str(round(df.Time.mean()-df.Time.mean() % 1))+':' + str(round(df.Time.mean() % 1*60)), className='P1')
        ], className='card', style={'display': 'inline-block', 'width': '20%', 'float': 'right'}),

        html.Div([
            html.P('Subcribers', className='P2'),
            html.P('23,000,000', className='P1')
        ], className='card', style={'display': 'inline-block', 'width': '20%', 'float': 'right'}),
    ]),

    html.Div([
        html.Div([
            dcc.Graph(
                id='view_by_time',
                figure=fig,
                className='card3',
                style={
                    'color': '#12151F',
                    'backgroundcolor': '#12151F',
                }
            ),
        ])
    ]),
    
    html.Div([
        html.Div([
            dcc.Graph(
                id='like_chart',
                figure=fig3, className='card3'
        , style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(
                id='view_chart',
                figure=fig2
                )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}, className='card3'),
    ]),
])
])

if __name__=='__main__':
    app.run_server(debug=True)
