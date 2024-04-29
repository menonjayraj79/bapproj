import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from update_histogram import update_histogram

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

# Callback function to update the line graph
@app.callback(
    Output('line-graph', 'figure'),
    [Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('uid-input', 'value')]
)
def update_graph(n_clicks, value):
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

        # Create traces for each course
        trace_A = go.Scatter(
            x=['iseA20', 'mse30', 'ese100'],
            y=[A['iseA20'].values[0], A['mse30'].values[0], A['ese100'].values[0]],
            mode='lines',
            name='Course A',
            line=dict(color='rgb(255, 0, 0)')
        )

        trace_B = go.Scatter(
            x=['iseA20', 'mse30', 'ese100'],
            y=[B['iseA20'].values[0], B['mse30'].values[0], B['ese100'].values[0]],
            mode='lines',
            name='Course B',
            line=dict(color='rgb(0, 255, 0)')
        )

        trace_C = go.Scatter(
            x=['iseA20', 'mse30', 'ese100'],
            y=[C['iseA20'].values[0], C['mse30'].values[0], C['ese100'].values[0]],
            mode='lines',
            name='Course C',
            line=dict(color='rgb(0, 0, 255)')
        )

        trace_D = go.Scatter(
            x=['iseA20', 'mse30', 'ese100'],
            y=[D['iseA20'].values[0], D['mse30'].values[0], D['ese100'].values[0]],
            mode='lines',
            name='Course D',
            line=dict(color='rgb(255, 255, 0)')
        )

        trace_E = go.Scatter(
            x=['iseA20', 'mse30', 'ese100'],
            y=[E['iseA20'].values[0], E['mse30'].values[0], E['ese100'].values[0]],
            mode='lines',
            name='Course E',
            line=dict(color='rgb(255, 0, 255)')
        )

        data = [trace_A, trace_B, trace_C, trace_D, trace_E]

        layout = go.Layout(
            title='Individual Student Performance Across Courses',
            xaxis=dict(title='Exam Types'),
            yaxis=dict(title='Scores'),
            plot_bgcolor='rgb(17, 17, 17)',
            paper_bgcolor='rgb(17, 17, 17)',
            font=dict(color='rgb(255, 255, 255)')
        )

        return go.Figure(data=data, layout=layout)

# Callback function to update the bar chart
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('uid-input', 'value')]
)
def update_bar_chart(n_clicks, value):
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

        # Create traces for each exam type
        trace_ise = go.Bar(
            x=['Course A', 'Course B', 'Course C', 'Course D', 'Course E'],
            y=[10,20,30,40,50],
            name='ISE',
            marker=dict(color='rgb(255, 0, 0)')
        )

        trace_mse = go.Bar(
            x=['Course A', 'Course B', 'Course C', 'Course D', 'Course E'],
            y=[10,20,30,40,50],
            name='MSE',
            marker=dict(color='rgb(0, 255, 0)')
        )

        trace_ese = go.Bar( 
            x=['Course A', 'Course B', 'Course C', 'Course D', 'Course E'],
            y=[10,20,30,40,50],
            name='ESE',
            marker=dict(color='rgb(0, 0, 255)')
        )

        data = [trace_ise, trace_mse, trace_ese]

        layout = go.Layout(
            title='Exam Type Performance Across Courses',
            xaxis=dict(title='Courses'),
            yaxis=dict(title='Scores'),
            barmode='group',
            plot_bgcolor='rgb(17, 17, 17)',
            paper_bgcolor='rgb(17, 17, 17)',
            font=dict(color='rgb(255, 255, 255)')
        )

        return go.Figure(data=data, layout=layout)

# Callback function to update the scatter plot
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('uid-input', 'value')]
)
def update_scatter_plot(n_clicks, value):
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

        # Create traces for each course
        trace_A = go.Scatter(
            x=[A['lecAttendance100'].values[0],
                A['labAttendance100'].values[0]],
            y=[A['total100'].values[0]],
            mode='markers',
            name='Course A',
            marker=dict(color='rgb(255, 0, 0)')
        )

        trace_B = go.Scatter(
            x=[B['lecAttendance100'].values[0],
                B['labAttendance100'].values[0]],
            y=[B['total100'].values[0]],
            mode='markers',
            name='Course B',
            marker=dict(color='rgb(0, 255, 0)')
        )

        trace_C = go.Scatter(
            x=[C['lecAttendance100'].values[0],
                C['labAttendance100'].values[0]],
            y=[C['total100'].values[0]],
            mode='markers',
            name='Course C',
            marker=dict(color='rgb(0, 0, 255)')
        )

        trace_D = go.Scatter(
            x=[D['lecAttendance100'].values[0],
                D['labAttendance100'].values[0]],
            y=[D['total100'].values[0]],
            mode='markers',
            name='Course D',
            marker=dict(color='rgb(255, 255, 0)')
        )

        trace_E = go.Scatter(
            x=[E['lecAttendance100'].values[0],
                E['labAttendance100'].values[0]],
            y=[E['total100'].values[0]],
            mode='markers',
            name='Course E',
            marker=dict(color='rgb(255, 0, 255)')
        )

        data = [trace_A, trace_B, trace_C, trace_D, trace_E]

        layout = go.Layout(
            title='Attendance vs Performance Across Courses',
            xaxis=dict(title='Attendance Percentage'),
            yaxis=dict(title='Total Score'),
            plot_bgcolor='rgb(17, 17, 17)',
            paper_bgcolor='rgb(17, 17, 17)',
            font=dict(color='rgb(255, 255, 255)')
        )

        return go.Figure(data=data, layout=layout)

# Callback function to update the pie chart
@app.callback(
    Output('pie-chart', 'figure'),
    [Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('uid-input', 'value')]
)
def update_pie_chart(n_clicks, value):
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

        # Create traces for each course
        trace = go.Pie(
            labels=['Course A', 'Course B',
                    'Course C', 'Course D', 'Course E'],
            values=[A['credit4'].values[0], B['credit4'].values[0],
                    C['credit4'].values[0], D['credit4'].values[0], E['credit4'].values[0]],
            name='Credits',
            hole=.3,
            marker=dict(colors=['rgb(255, 0, 0)', 'rgb(0, 255, 0)',
                        'rgb(0, 0, 255)', 'rgb(255, 255, 0)', 'rgb(255, 0, 255)']),
            textfont=dict(color='rgb(255, 255, 255)')
        )

        data = [trace]

        layout = go.Layout(
            title='Credit Distribution Across Courses',
            plot_bgcolor='rgb(17, 17, 17)',
            paper_bgcolor='rgb(17, 17, 17)',
            font=dict(color='rgb(255, 255, 255)')
        )
        return go.Figure(data=data, layout=layout)

# Callback function to update the box plot
@app.callback(
    Output('box-plot', 'figure'),
    [Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('uid-input', 'value')]
)
def update_box_plot(n_clicks, value):
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

        # Create traces for each teacher
        trace_A = go.Box(
            y=A['total100'],
            name=A['teacher'].values[0],
            boxpoints='all',  # show all points
            jitter=0.3,  # spread out points for visibility
            pointpos=-1.8,  # position points relative to box
            marker=dict(color='rgb(255, 0, 0)'),
            line=dict(color='rgb(255, 255, 255)')
        )

        trace_B = go.Box(
            y=B['total100'],
            name=B['teacher'].values[0],
            boxpoints='all',
            jitter=0.3,
            pointpos=-1.8,
            marker=dict(color='rgb(0, 255, 0)'),
            line=dict(color='rgb(255, 255, 255)')
        )

        trace_C = go.Box(
            y=C['total100'],
            name=C['teacher'].values[0],
            boxpoints='all',
            jitter=0.3,
            pointpos=-1.8,
            marker=dict(color='rgb(0, 0, 255)'),
            line=dict(color='rgb(255, 255, 255)')
        )

        trace_D = go.Box(
            y=D['total100'],
            name=D['teacher'].values[0],
            boxpoints='all',
            jitter=0.3,
            pointpos=-1.8,
            marker=dict(color='rgb(255, 255, 0)'),
            line=dict(color='rgb(255, 255, 255)')
        )

        trace_E = go.Box(
            y=E['total100'],
            name=E['teacher'].values[0],
            boxpoints='all',
            jitter=0.3,
            pointpos=-1.8,
            marker=dict(color='rgb(255, 0, 255)'),
            line=dict(color='rgb(255, 255, 255)')
        )

        data = [trace_A, trace_B, trace_C, trace_D, trace_E]

        layout = go.Layout(
            title='Teacher Impact on Student Performance',
            yaxis=dict(title='Total Score'),
            plot_bgcolor='rgb(17, 17, 17)',
            paper_bgcolor='rgb(17, 17, 17)',
            font=dict(color='rgb(255, 255, 255)')
        )

        return go.Figure(data=data, layout=layout)

# Callback function to update the scatter plot for lab vs theory performance
@app.callback(
    Output('scatter-plot-lab-theory', 'figure'),
    [Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('uid-input', 'value')]
)
def update_scatter_plot_lab_theory(n_clicks, value):
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

        # Create traces for each course
        trace_A = go.Scatter(
            x=[A['lab100'].values[0]],
            y=[A['theoryConverted60'].values[0]],
            mode='markers',
            name='Course A',
            marker=dict(color='rgb(255, 0, 0)')
        )

        trace_B = go.Scatter(
            x=[B['lab100'].values[0]],
            y=[B['theoryConverted60'].values[0]],
            mode='markers',
            name='Course B',
            marker=dict(color='rgb(0, 255, 0)')
        )

        trace_C = go.Scatter(
            x=[C['lab100'].values[0]],
            y=[C['theoryConverted60'].values[0]],
            mode='markers',
            name='Course C',
            marker=dict(color='rgb(0, 0, 255)')
        )

        trace_D = go.Scatter(
            x=[D['lab100'].values[0]],
            y=[D['theoryConverted60'].values[0]],
            mode='markers',
            name='Course D',
            marker=dict(color='rgb(255, 255, 0)')
        )

        trace_E = go.Scatter(
            x=[E['lab100'].values[0]],
            y=[E['theoryConverted60'].values[0]],
            mode='markers',
            name='Course E',
            marker=dict(color='rgb(255, 0, 255)')
        )

        data = [trace_A, trace_B, trace_C, trace_D, trace_E]

  
        layout = go.Layout(
            title='Lab vs Theory Performance Across Courses',
            xaxis=dict(title='Lab Score'),
            yaxis=dict(title='Theory Score'),
            plot_bgcolor='rgb(17, 17, 17)',
            paper_bgcolor='rgb(17, 17, 17)',
            font=dict(color='rgb(255, 255, 255)')
        )

        return go.Figure(data=data, layout=layout)


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


app.layout = html.Div(
    style={
        'backgroundColor': 'rgb(17, 17, 17)',
        'color': 'rgb(255, 255, 255)',
        'padding': '10px'
    },
    children=[
        dcc.Input(
            id='uid-input',
            type='number',
            placeholder='Enter UID',
           
            style={
                'backgroundColor': 'rgb(34, 34, 34)',
                'color': 'rgb(255, 255, 255)',
                'padding': '10px',
                'border': 'none',
                'borderRadius': '5px',
                'marginBottom': '10px'
            }
        ),
        html.Button(
            'Submit',
            id='submit-val',
            n_clicks=0,
            style={
                'backgroundColor': 'rgb(0, 123, 255)',
                'color': 'rgb(255, 255, 255)',
                'padding': '10px',
                'border': 'none',
                'borderRadius': '5px',
                'cursor': 'pointer'
            }
        ),
        html.Div(id='output-container'),
        dcc.Graph(
            id='line-graph',
            style={'height': '400px'}
        ),
        dcc.Graph(
            id='bar-chart',
            style={'height': '400px'}
        ),
        dcc.Graph(
            id='scatter-plot',
            style={'height': '400px'}
        ),
        dcc.Graph(
            id='pie-chart',
            style={'height': '400px'}
        ),
        dcc.Graph(
            id='box-plot',
            style={'height': '400px'}
        ),
        dcc.Graph(
            id='histogram',
            style={'height': '400px'}
        ),
        dcc.Graph(
            id='scatter-plot-lab-theory',
            style={'height': '400px'}
        )
    ]
)
if __name__ == '__main__':
    app.run_server(debug=True)
