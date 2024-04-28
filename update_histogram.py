import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

app = dash.Dash(__name__)

# Load datasets
Acomplete = pd.read_excel('Acomplete.xlsx')  # Load data for Course A
Bcomplete = pd.read_excel('Bcomplete.xlsx')  # Load data for Course B
Ccomplete = pd.read_excel('Ccomplete.xlsx')  # Load data for Course C
Dcomplete = pd.read_excel('Dcomplete.xlsx')  # Load data for Course D
Ecomplete = pd.read_excel('Ecomplete.xlsx')  # Load data for Course E


value=int(2010300075)

# Callback function to update the output container
@app.callback(
    Output('output-container', 'children'),
    [Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('uid-input', 'value')]
)
def update_output(n_clicks, value):
    
    if value is None:
        print('Enter a UID')
        return 'Enter a UID'
    else:
        # Filter dataframes based on UID
        print(value)
        A = Acomplete[Acomplete['uid'] == value]
        B = Bcomplete[Bcomplete['uid'] == value]
        C = Ccomplete[Ccomplete['uid'] == value]
        D = Dcomplete[Dcomplete['uid'] == value]
        E = Ecomplete[Ecomplete['uid'] == value]

        print(A.head())
        print(B.head())
        print(C.head())
        print(D.head())
        print(E.head())
        print(A.columns)

        # Check if dataframes are empty
        if A.empty and B.empty and C.empty and D.empty and E.empty:
            return 'No data found for this UID'
        else:
            # Convert dataframes to HTML tables
            tables = [A.to_html(), B.to_html(), C.to_html(),
                      D.to_html(), E.to_html()]

    max_rows = 10  # Define max_rows. Change the value as per your requirement.
    return html.Div([
        # html.Table([
        #     html.Thead([
        #         html.Tr([html.Th(col) for col in dataframe.columns])
        #     ]),
        #     html.Tbody([
        #         html.Tr([
        #             html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        #         ]) for i in range(min(len(dataframe), max_rows))
        #     ])
        # ]) for dataframe in [A, B, C, D, E]
    ])

@app.callback(
    Output('histogram', 'figure'),
    [Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('uid-input', 'value')]
)
def update_histogram(n_clicks, value):
    if value is None:
        return go.Figure()
    else:
        A = Acomplete[Acomplete['uid'] == value]
        B = Bcomplete[Bcomplete['uid'] == value]
        C = Ccomplete[Ccomplete['uid'] == value]
        D = Dcomplete[Dcomplete['uid'] == value]
        E = Ecomplete[Ecomplete['uid'] == value]

        if A.empty and B.empty and C.empty and D.empty and E.empty:
            return go.Figure()

        # Concatenate grades from all courses
        grades = pd.concat(
            [A['grade'], B['grade'], C['grade'], D['grade'], E['grade']])

        # Create histogram
        trace = go.Histogram(
            x=grades,
            name='Grades',
            xbins=dict(start='A', end='F', size=1),
            marker=dict(color='rgb(0, 0, 255)'),
            opacity=0.7
        )

        data = [trace]

        layout = go.Layout(
            title='Grade Distribution Across Courses',
            xaxis=dict(title='Grade'),
            yaxis=dict(title='Number of Courses'),
            plot_bgcolor='rgb(17, 17, 17)',
            paper_bgcolor='rgb(17, 17, 17)',
            font=dict(color='rgb(255, 255, 255)')
        )
    return go.Figure(data=data, layout=layout)
