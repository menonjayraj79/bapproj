import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from dash_bootstrap_components._components.Container import Container

# Create the Dash application
app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)


marks = pd.read_excel('Acomplete.xlsx')

# Define dropdown options
dropdown_options = [
    {'label': 'sub 1', 'value': 'Bcomplete.xlsx'},
    {'label': 'sub 2', 'value': 'Ccomplete.xlsx'},
    {'label': 'sub 3', 'value': 'Acomplete.xlsx'}
]

# Create dropdown component
dropdown = dcc.Dropdown(
    id='file-dropdown',
    options=dropdown_options,
    value='Acomplete.xlsx'
)

# Read data from selected Excel file
marks = pd.read_excel(dropdown.value)


@ app.callback(
    dash.dependencies.Output('marks', 'children'),
    [dash.dependencies.Input('file-dropdown', 'value')]
)
def update_marks(selected_file):
    marks = pd.read_excel(selected_file)
    return html.Table([
        # html.Thead(
        #     html.Tr([html.Th(col) for col in marks.columns])
        # ),
        # html.Tbody([
        #     html.Tr([
        #         html.Td(marks.iloc[i][col]) for col in marks.columns
        #     ]) for i in range(len(marks))
        # ])
    ])


# Calculate the proportion of students who achieved different ranges of lab scores
@ app.callback(
    dash.dependencies.Output('pie', 'figure'),
    [dash.dependencies.Input('file-dropdown', 'value')]
)
def update_pie_chart(selected_file):
    marks = pd.read_excel(selected_file)
    lab_scores_ranges = pd.cut(marks['labConverted40'], bins=[
        0, 10, 20, 30, 40], labels=['0-10', '10-20', '20-30', '30-40'])
    lab_scores_proportions = lab_scores_ranges.value_counts(normalize=True)

    pie_chart = {
        'data': [
            {
                'values': lab_scores_proportions.values,
                'labels': lab_scores_proportions.index,
                'type': 'pie',
                'name': 'Lab Scores',
                'hoverinfo': 'label+percent+name',
                'hole': .3,
                'marker': {
                    'colors': ['#636EFA', '#EF553B', '#00CC96', '#AB63FA'],
                    'line': {'color': 'white', 'width': 2}

                },
                'textfont': {'color': 'white'},
                'textposition': 'inside',
                'textinfo': 'percent'
            }
        ],
        'layout': {
            'title': 'Lab Performance Analysis',
            'paper_bgcolor': '#1E1E1E',
            'plot_bgcolor': '#1E1E1E',
            'font': {'color': 'white'},
            'titlefont': {'color': 'white'},
            'legend': {'font': {'color': 'white'}}
        }
    }

    return pie_chart


# Calculate average marks for each year
yearly_average_marks = marks.groupby('year')['total100'].mean()

# Create line graph for performance over time
performance_line_graph = dcc.Graph(
    id='performance_line',
    figure={
        'data': [
            {
                'x': yearly_average_marks.index,
                'y': yearly_average_marks.values,
                'mode': 'lines',
                'name': 'Avg Marks'
            }
        ],
        'layout': {
            'title': 'Performance Over Time',
            'xaxis': {'title': 'Year'},
            'yaxis': {'title': 'Average Marks'},
            'paper_bgcolor': '#1E1E1E',
            'plot_bgcolor': '#1E1E1E',
            'font': {'color': 'white'},
            'titlefont': {'color': 'white'},
            'legend': {'font': {'color': 'white'}}
        }
    }
)

# Update the callback function to update the graph based on dropdown selection


@app.callback(
    dash.dependencies.Output('performance_line', 'figure'),
    [dash.dependencies.Input('file-dropdown', 'value')]
)
def update_performance_line(selected_file):
    marks = pd.read_excel(selected_file)
    yearly_average_marks = marks.groupby('year')['total100'].mean()

    line_graph = {
        'data': [
            {
                'x': yearly_average_marks.index,
                'y': yearly_average_marks.values,
                'mode': 'lines',
                'name': 'Avg Marks'
            }
        ],
        'layout': {
            'title': 'Performance Over Time',
            'xaxis': {'title': 'Year'},
            'yaxis': {'title': 'Average Marks'},
            'paper_bgcolor': '#1E1E1E',
            'plot_bgcolor': '#1E1E1E',
            'font': {'color': 'white'},
            'titlefont': {'color': 'white'},
            'legend': {'font': {'color': 'white'}}
        }
    }

    return line_graph


# Create histogram for Credit and Pointer Distribution
histogram = dcc.Graph(
    id='histogram',
    figure={
        'data': [
            {
                'x': marks['creditObt40'],
                'name': 'Credits Obtained',
                'type': 'histogram',
                'opacity': 0.75,
                'marker': {
                    'color': '#636EFA'
                }
            },
            {
                'x': marks['pointer10'],
                'name': 'Pointers',
                'type': 'histogram',
                'opacity': 0.75,
                'marker': {
                    'color': '#EF553B'
                }
            }
        ],
        'layout': {
            'title': 'Credit and Pointer Distribution',
            'xaxis': {'title': 'Value', 'color': 'white'},
            'yaxis': {'title': 'Number of Students', 'color': 'white'},
            'barmode': 'overlay',
            'paper_bgcolor': '#1E1E1E',
            'plot_bgcolor': '#1E1E1E',
            'font': {'color': 'white'},
            'titlefont': {'color': 'white'},
            'legend': {'font': {'color': 'white'}}
        }
    }
)

# Update the callback function to update the histogram based on dropdown selection


@app.callback(
    dash.dependencies.Output('histogram', 'figure'),
    [dash.dependencies.Input('file-dropdown', 'value')],
    allow_duplicate=True
)
def update_histogram(selected_file):
    marks = pd.read_excel(selected_file)
    histogram_figure = {
        'data': [
            {
                'x': marks['creditObt40'],
                'name': 'Credits Obtained',
                'type': 'histogram',
                'opacity': 0.75,
                'marker': {
                    'color': '#636EFA'
                }
            },
            {
                'x': marks['pointer10'],
                'name': 'Pointers',
                'type': 'histogram',
                'opacity': 0.75,
                'marker': {
                    'color': '#EF553B'
                }
            }
        ],
        'layout': {
            'title': 'Credit and Pointer Distribution',
            'xaxis': {'title': 'Value', 'color': 'white'},
            'yaxis': {'title': 'Number of Students', 'color': 'white'},
            'barmode': 'overlay',
            'paper_bgcolor': '#1E1E1E',
            'plot_bgcolor': '#1E1E1E',
            'font': {'color': 'white'},
            'titlefont': {'color': 'white'},
            'legend': {'font': {'color': 'white'}}
        }
    }
    return histogram_figure


# Group data by teacher and get marks
teacher_marks = marks.groupby('teacher')['total100']

# Create box plot
box_plot = dcc.Graph(
    id='box',
    figure={
        'data': [
            {
                'y': teacher_marks.get_group(x),
                'type': 'box',
                'name': x,
                'marker': {
                    'color': '#00CC96'
                },
                # 'boxpoints': 'all',
                # 'jitter': 0.3,
                'pointpos': -1.8
            } for x in teacher_marks.groups
        ],
        'layout': {
            'title': 'Teacher-wise Performance Comparison',
            'yaxis': {'title': 'Marks', 'color': 'white'},
            'paper_bgcolor': '#1E1E1E',
            'plot_bgcolor': '#1E1E1E',
            'font': {'color': 'white'},
            'titlefont': {'color': 'white'},
            'legend': {'font': {'color': 'white'}}
        }
    }
)

# Update the callback function to update the box plot based on dropdown selection


@app.callback(
    dash.dependencies.Output('box', 'figure'),
    [dash.dependencies.Input('file-dropdown', 'value')]
)
def update_box_plot(selected_file):
    marks = pd.read_excel(selected_file)
    teacher_marks = marks.groupby('teacher')['total100']
    box_plot_figure = {
        'data': [
            {
                'y': teacher_marks.get_group(x),
                'type': 'box',
                'name': x,
                'marker': {
                    'color': '#00CC96'
                },
                    'boxpoints': 'all',
                    # 'jitter': 0.3,
                    'pointpos': -0.1
            } for x in teacher_marks.groups
        ],
        'layout': {
            'title': 'Teacher-wise Performance Comparison',
            'yaxis': {'title': 'Marks', 'color': 'white'},
            'paper_bgcolor': '#1E1E1E',
            'plot_bgcolor': '#1E1E1E',
            'font': {'color': 'white'},
            'titlefont': {'color': 'white'},
            'legend': {'font': {'color': 'white'}}
        }
    }
    return box_plot_figure


# Calculate average grades for each attendance percentage
attendance_grades = marks.groupby('lecAttendance100')[
    'theoryConverted60'].mean()

# Create line graph
line_graph = dcc.Graph(
    id='line',
    figure={
        'data': [
            {
                'x': attendance_grades.index,
                'y': attendance_grades.values,
                'mode': 'lines',
                'name': 'Avg Grade',
                'line': {'color': '#AB63FA'}
            }
        ],
        'layout': {
            'title': 'Attendance Impact on Grades',
            'xaxis': {'title': 'Attendance Percentage', 'color': 'white'},
            'yaxis': {'title': 'Average Grade', 'color': 'white'},
            'paper_bgcolor': '#1E1E1E',
            'plot_bgcolor': '#1E1E1E',
            'font': {'color': 'white'},
            'titlefont': {'color': 'white'},
            'legend': {'font': {'color': 'white'}}
        }
    }
)

# Update the callback function to update the line graph based on dropdown selection


@app.callback(
    dash.dependencies.Output('line', 'figure'),
    [dash.dependencies.Input('file-dropdown', 'value')]
)
def update_line_graph(selected_file):
    marks = pd.read_excel(selected_file)
    attendance_grades = marks.groupby('lecAttendance100')[
        'theoryConverted60'].mean()
    line_graph_figure = {
        'data': [
            {
                'x': attendance_grades.index,
                'y': attendance_grades.values,
                'mode': 'lines',
                'name': 'Avg Grade',
                'line': {'color': '#AB63FA'}
            }
        ],
        'layout': {
            'title': 'Attendance Impact on Grades',
            'xaxis': {'title': 'Attendance Percentage', 'color': 'white'},
            'yaxis': {'title': 'Average Grade', 'color': 'white'},
            'paper_bgcolor': '#1E1E1E',
            'plot_bgcolor': '#1E1E1E',
            'font': {'color': 'white'},
            'titlefont': {'color': 'white'},
            'legend': {'font': {'color': 'white'}}
        }
    }
    return line_graph_figure


# Update the callback function to update the scatter plot based on dropdown selection


@app.callback(
    dash.dependencies.Output('scatter', 'figure'),
    [dash.dependencies.Input('file-dropdown', 'value')]
)
def update_scatter_plot(selected_file):
    marks = pd.read_excel(selected_file)
    scatter_plot_figure = {
        'data': [
            {
                'x': marks['theoryConverted60'],
                'y': marks['labConverted40'],
                'mode': 'markers',
                'name': 'Students',
                'marker': {
                    'color': '#AB63FA',
                    'size': 8,
                    'line': {'color': '#1E1E1E', 'width': 0.5}
                }
            }
        ],
        'layout': {
            'title': 'Correlation between Theory and Lab Scores',
            'xaxis': {'title': 'Theory Scores', 'color': 'white'},
            'yaxis': {'title': 'Lab Scores', 'color': 'white'},
            'paper_bgcolor': '#1E1E1E',
            'plot_bgcolor': '#1E1E1E',
            'font': {'color': 'white'},
            'titlefont': {'color': 'white'},
            'legend': {'font': {'color': 'white'}}
        }
    }
    return scatter_plot_figure


# Update the callback function to update the bar chart based on dropdown selection
@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('file-dropdown', 'value')]
)
def update_bar_chart(selected_file):
    marks = pd.read_excel(selected_file)
    average_ise = marks['iseA20'].mean()
    average_mse = marks['mse30'].mean()
    average_ese = marks['ese100'].mean()

    return {
        'data': [
            {'x': ['ISE', 'MSE', 'ESE'], 'y': [average_ise, average_mse,
                                               average_ese], 'type': 'bar', 'name': 'Avg Score',
             'marker': {'color': ['#636EFA', '#EF553B', '#00CC96']},
             'textfont': {'color': 'white'},
             'textposition': 'auto',
             'text': [f'{avg:.2f}' for avg in [average_ise, average_mse, average_ese]]
             }
        ],
        'layout': {
            'title': 'Performance Distribution by Exam Type',
            'paper_bgcolor': '#1E1E1E',
            'plot_bgcolor': '#1E1E1E',
            'font': {'color': 'white'},
            'titlefont': {'color': 'white'},
            'legend': {'font': {'color': 'white'}}
        }
    }


# Set up the layout of the app
tab1_content = html.Div([
    html.Div(id='marks'),
    html.H1(children='Performance Distribution by Exam Type',
            style={'color': 'white'}),
    dcc.Graph(
        id='graph',
        style={'paper_bgcolor': 'black  ', 'plot_bgcolor': 'black '},

    )],
    className="mt-1 mb-3",
)

tab2_content = html.Div([
    html.H1(children='Correlation between Theory and Lab Scores',
            style={'color': 'white'}),
    dcc.Graph(
        id='scatter',
        style={'paper_bgcolor': 'black  ', 'plot_bgcolor': 'black '},

    ),],
    className="mt-1 mb-3",
)
tab3_content = html.Div([
    html.H1(children='Attendance Impact on Grades',
            style={'color': 'white'}),
    line_graph,],
    className="mt-1 mb-3",
)
tab4_content = html.Div([
    html.H1(children='Teacher-wise Performance Comparison',
            style={'color': 'white'}),
    box_plot,],
    className="mt-1 mb-3",
)
tab5_content = html.Div([
    html.H1(children='Credit and Pointer Distribution',
            style={'color': 'white'}),
    histogram,],
    className="mt-1 mb-3",
)
tab6_content = html.Div([
    html.H1(children='Performance Over Time', style={'color': 'white'}),
    performance_line_graph,],
    className="mt-1 mb-3",
)
tab7_content = html.Div([
    html.H1(children='Lab Performance Analysis', style={'color': 'white'}),
    dcc.Graph(
        id='pie',
        style={'paper_bgcolor': 'black  ', 'plot_bgcolor': 'black '},

    ),],
    className="mt-1 mb-3",
)


tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Bar Chart"),
        dbc.Tab(tab2_content, label="Scatter Plot"),
        dbc.Tab(tab3_content, label="Line Graph"),
        dbc.Tab(tab4_content, label="Box Plot"),
        dbc.Tab(tab5_content, label="Histogram"),
        dbc.Tab(tab6_content, label="Line Graph"),
        dbc.Tab(tab7_content, label="Pie Chart"),
    ]
)
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

nav_contents = [
    dbc.NavItem(dbc.NavLink("Prescriptive Analysis", href="/prescriptive_analysis",
                active=True), style={'margin-right': '10px'}),
    dbc.NavItem(dbc.NavLink("Descriptive Analysis", href="/descriptive_analysis",
                active=True), style={'margin-right': '10px'}),
]

nav1 = dbc.Nav(nav_contents, pills=True, fill=True)

navs = html.Div([nav1])

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Student Marks Analysis", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                # search_bar,
                navs,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
                className="justify-content-end",  # Add right alignment
            ),
        ]
    ),
    color="black",
    dark=True,
    className=" mb-3",  # Add bottom margin
)


# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


descriptive_analysis = dbc.Container(html.Div(
    children=[
        navbar,
        dropdown,
        # accordion,
        tabs
    ],
    style={'background': 'black',
           'color': 'black', 'font-family': 'Arial'}
))


Acomplete = pd.read_excel('Acomplete.xlsx')  # Load data for Course A
Bcomplete = pd.read_excel('Bcomplete.xlsx')  # Load data for Course B
Ccomplete = pd.read_excel('Ccomplete.xlsx')  # Load data for Course C
Dcomplete = pd.read_excel('Dcomplete.xlsx')  # Load data for Course D
Ecomplete = pd.read_excel('Ecomplete.xlsx')  # Load data for Course E


value = int(2010300075)

# Callback function to update the output container


@app.callback(
    Output('output-container', 'children'),
    [Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('uid-input', 'value')],
    allow_duplicate=True
)
def update_output(n_clicks, value):

    if value is None:
        # print('Enter a UID')
        return 'Enter a UID'
    else:
        # Filter dataframes based on UID
        # print(value)
        A = Acomplete[Acomplete['uid'] == value]
        B = Bcomplete[Bcomplete['uid'] == value]
        C = Ccomplete[Ccomplete['uid'] == value]
        D = Dcomplete[Dcomplete['uid'] == value]
        E = Ecomplete[Ecomplete['uid'] == value]

        # print(A.head())
        # print(B.head())
        # print(C.head())
        # print(D.head())
        # print(E.head())
        # print(A.columns)

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
            y=[A['iseA20'].values[0], B['iseA20'].values[0],
                C['iseA20'].values[0], D['iseA20'].values[0], E['iseA20'].values[0]],
            name='ISE',
            marker=dict(color='rgb(255, 0, 0)')
        )

        trace_mse = go.Bar(
            x=['Course A', 'Course B', 'Course C', 'Course D', 'Course E'],
            y=[A['mse30'].values[0], B['mse30'].values[0],
                C['mse30'].values[0], D['mse30'].values[0], E['mse30'].values[0]],
            name='MSE',
            marker=dict(color='rgb(0, 255, 0)')
        )

        trace_ese = go.Bar(
            x=['Course A', 'Course B', 'Course C', 'Course D', 'Course E'],
            y=[A['ese100'].values[0], B['ese100'].values[0],
                C['ese100'].values[0], D['ese100'].values[0], E['ese100'].values[0]],
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
    Output('histogramS', 'figure'),
    [Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('uid-input', 'value')],
    allow_duplicate=True
)
def update_histogramS(n_clicks, value):
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


tab1B_content = html.Div([
    dcc.Graph(
        id='line-graph',
        style={'height': '400px'}
    ),],
    className="mt-1 mb-3",
)

tab2B_content = html.Div([
    dcc.Graph(
        id='bar-chart',
        style={'height': '400px'}
    ),],
    className="mt-1 mb-3",
)
tab3B_content = html.Div([
    dcc.Graph(
        id='scatter-plot',
        style={'height': '400px'}
    ),],
    className="mt-1 mb-3",
)
tab4B_content = html.Div([
    dcc.Graph(
        id='pie-chart',
        style={'height': '400px'}
    ),],
    className="mt-1 mb-3",
)
tab5B_content = html.Div([
    dcc.Graph(
        id='box-plot',
        style={'height': '400px'}
    ),],
    className="mt-1 mb-3",
)
tab6B_content = html.Div([
    dcc.Graph(
        id='histogramS',
        style={'height': '400px'}
    ),],
    className="mt-1 mb-3",
)
tab7B_content = html.Div([
    dcc.Graph(
        id='scatter-plot-lab-theory',
        style={'height': '400px'}
    )],
    className="mt-1 mb-3",
)


tabs = dbc.Tabs(
    [
        dbc.Tab(tab1B_content, label="Line Graph"),
        dbc.Tab(tab2B_content, label="Bar Chart"),
        dbc.Tab(tab3B_content, label="Scatter Plot"),
        dbc.Tab(tab4B_content, label="Pie Chart"),
        dbc.Tab(tab5B_content, label="Box Plot"),
        dbc.Tab(tab6B_content, label="Scatter Plot"),
        dbc.Tab(tab7B_content, label="Histogram"),
    ]
)
prescriptive_analysis = dbc.Container(dbc.Container(html.Div(


    children=[
        navbar,
        # accordion,
        
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
        tabs,
        
        
        ], style={
        'backgroundColor': 'rgb(17, 17, 17)',
        'color': 'rgb(255, 255, 255)',
        'padding': '10px'
    },
)))
# Run the app


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/prescriptive_analysis':
        return prescriptive_analysis
    else:
        return descriptive_analysis


# Define the layout of the application
app.layout = dbc.Container(html.Div(
    children=[
        dcc.Location(id='url', refresh=False),
        dbc.Container(html.Div(id='page-content')),
    ],
)
)


# app.layout =


# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)
# # Define the layout of the scatter plot page
# scatter_layout = html.Div([
#     html.H1('Scatter Plot'),
#     scatter_plot,
#     html.P('Go to the '),
#     dcc.Link('Bar Chart', href='/bar'),
# ])
