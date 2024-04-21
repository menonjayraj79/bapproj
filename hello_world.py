import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objs as go
import pandas as pd
import openpyxl
app = dash.Dash()

# np.random.seed(50)
# x_rand = np.random.randint(1, 61, 60)
# y_rand = np.random.randint(1, 61, 60)

# Define data
data = {
    'Sales': [100, 200, 300, 400, 500],
    'Profit': [10, 20, 30, 40, 50]
}

# Create DataFrame
df = pd.DataFrame(data)

# Write to Excel
df.to_excel('sales.xlsx', index=False, engine='openpyxl')

orders = pd.read_excel('sales.xlsx')

colors = {
    'background': '#111111',
    'text': '#ff0000',
    'plot_color': '#d3d3d3',
    'paper_color': '#00FFFF'
}

app.layout = html.Div(children=[
    html.H1(children='Hello Dash',

            style={
                'textAlign': 'center',
                'color': colors['text']
            }
            ),

    html.Div(children='''
        Dash: A web application framework for Python.
    ''',
             style={
                 'textAlign': 'center',
                 'color': '#7FDBFF'
             }),

    # dcc.Graph(
    #     id='example-graph',
    #     figure={
    #         'data': [
    #             {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
    #             {'x': [1, 2, 3], 'y': [2, 4, 5],
    #                 'type': 'bar', 'name': u'Montréal'},
    #         ],
    #         'layout': {
    #             'plot_bgcolor': '#111111',
    #             'paper_bgcolor': '#00FFFF',
    #             'font': {
    #                 'color': '#7FDBFF'
    #             },
    #             'title': 'Dash Data Visualization'
    #         }
    #     }
    # )

    # dcc.Graph(
    #     id='scatter_chart',
    #     figure={
    #         'data': [
    #             go.Scatter(
    #                 x=x_rand,
    #                 y=y_rand,
    #                 mode='markers',
    #                 marker={
    #                     'size': 12,
    #                     'color': 'rgb(51,204,153)',
    #                     'symbol': 'pentagon',
    #                     'line': {'width': 2}
    #                 }
    #             )
    #         ],
    #         'layout': go.Layout(
    #             title='Scatter Plot of Random 60 points',
    #             xaxis={'title': 'Random X-Values'},
    #             yaxis={'title': 'Random Y-Values'},
    #             plot_bgcolor=colors['plot_color'],
    #             paper_bgcolor=colors['paper_color']
    #         )
    #     }
    # )

    dcc.Graph(
        id='scatter_chart',
        figure={
            'data': [
                go.Scatter(
                    x=orders['Sales'],
                    y=orders['Profit'],
                    mode='markers',
                    marker={
                        'size': 12,
                        'color': 'rgb(51,204,153)',
                        'symbol': 'pentagon',
                        'line': {'width': 2}
                    }
                )
            ],
            'layout': go.Layout(
                title='Scatter Plot of Sales and Profit',
                xaxis={'title': 'Sales'},
                yaxis={'title': 'Profit'},
                plot_bgcolor=colors['plot_color'],
                paper_bgcolor=colors['paper_color'],
                hovermode='closest'
            )
        }
    )

])
if __name__ == '__main__':
    app.run_server(debug=True)

# help(html.Div)

# help(html.H1)
