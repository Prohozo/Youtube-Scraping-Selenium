import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import webbrowser
import plotly.express as px
import dash
import pathlib
from datetime import date as dt
from threading import Timer
import os

def create_dashboard(df_export, yt_channel, subscribers):
    df_export['small_title'] = df_export.Title.apply(
        lambda x: ' '.join(x.split(' ')[:8])+'...')
    minute = str(round(df_export.Time.mean()-df_export.Time.mean() % 1))
    second = str(round(df_export.Time.mean() % 1*60))
    if len(second) == 1:
        second = '0' + second
    app = dash.Dash(
        __name__,
        external_stylesheets=[os.path.join(
            pathlib.Path().parent.absolute(), 'assets\\style.css')]
    )

    colors = {
        'background': '#111111',
        'text': 'white'
    }

    app.title = f'{yt_channel} Channel Dashboard'

    # Line graph 'View by time'
    fig = px.line(df_export, x="Date", y='View',
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
            'title': 'Time'
        },
        yaxis={
            'title': 'Views',
            'showgrid': False
        },
        title={
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'size': 25,
                'family': 'Arial'
            }
        }
    )

    fig.update_traces(
        mode='markers+lines',
        hovertemplate="<br>".join([
            'Date: <b>%{x}</b>',
            'Total views: <b>%{y:,}</b>',
            'Title: <b>%{customdata[0]}</b>',
        ])
    )
    # Top 5 video with most views
    fig2 = px.bar(
        df_export.sort_values(by=['View'])[-5:],
        orientation='h',
        x='View',
        y='small_title',
        text='View',
        title='Top 5 videos with most views',
        custom_data=['Title'],
        color_discrete_sequence=['#05F4B7', '#086972', '#071a52'])

    fig2.update_traces(
        texttemplate='%{text:.2s}',
        textposition='inside',
        hovertemplate='Title: <b>%{customdata[0]}</b> <br>View: <b>%{x:,}</b>',
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
    # Top 5 video with most likes
    fig3 = px.bar(
        df_export.sort_values(by=['Like'])[-5:],
        orientation='h',
        barmode='group',
        x=["Like", "Dislike", "Comment"],
        y="small_title",
        title="Top 5 videos with most likes",
        custom_data=['Title'],
        color_discrete_sequence=['#05F4B7', '#b31e6f', '#ee5a5a', ])

    fig3.update_traces(
        texttemplate='%{x:.2s}',
        textposition='inside',
        hovertemplate='Title: <b>%{customdata[0]}</b> <br>Engagement: <b>%{x:,}</b>',
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
            'title': None,
        },
        legend=dict(
            # yanchor="bottom",
            # y=0.01,
            # xanchor="right",
            # x=0.99,
            title_font_size=10,
            font=dict(
                size=10,
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

    today = f'Updated {dt.today().strftime("%B %d, %Y")}'
    df_export.Date = pd.to_datetime(df_export.Date)

    df_export['Year'] = df_export['Date'].apply(lambda x: x.year)
    app.layout = html.Div([
        html.Div([
            html.Div([
                html.H1(f'{yt_channel} Channel Dashboard',
                        className='header_title',),
                html.P(f'{today}', className='header_sub'),
                html.Img(
                    src=app.get_asset_url(f'{yt_channel}_avatar.png'),
                    alt='Youtuber Avatar',
                    className='avatar',
                    style={'display': 'flex', 'vertical-align': 'middle'}
                ),
            ], className='header'),
        ]),

        html.Div([
            html.Div([
                html.P('Total videos collected', className='P2'),
                html.P(df_export.Title.count(), className='P1')
            ], className='card', style={'display': 'inline-block', 'width': '20%'}),

            html.Div([
                html.P('Total views', className='P2'),
                html.P(f'{df_export.View.sum():,}', className='P1')
            ], className='card', style={'display': 'inline-block', 'width': '20%'}),

            html.Div([
                html.P('Average video duration', className='P2'),
                html.P(minute+':'+second, className='P1')
            ], className='card', style={'display': 'inline-block', 'width': '20%', 'float': 'right'}),

            html.Div([
                html.P('Subscribers', className='P2'),
                html.P(f'{subscribers}', className='P1')
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
                    figure=fig3, className='card3', style={'width': '49%', 'display': 'inline-block'}),
                html.Div([
                    dcc.Graph(
                        id='view_chart',
                        figure=fig2
                    )
                ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}, className='card3'),
            ]),
        ])
    ])

    print('------------------------------------------')
    print('Ctrl+C to turn it off!')
    print('------------------------------------------')
    port = 8050 

    def open_browser():
        webbrowser.open_new(f"http://localhost:{port}")

    Timer(1, open_browser).start()
    app.run_server(debug=True, port=port, use_reloader=False)
