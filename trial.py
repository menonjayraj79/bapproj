import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

app = dash.Dash()

marks = pd.read_excel('Acomplete.xlsx')

# Calculate the proportion of students who achieved different ranges of lab scores
lab_scores_ranges = pd.cut(marks['labConverted40'], bins=[
                           0, 10, 20, 30, 40], labels=['0-10', '10-20', '20-30', '30-40'])
lab_scores_proportions = lab_scores_ranges.value_counts(normalize=True)

# Create pie chart
pie_chart = dcc.Graph(
    id='pie',
    figure={
        'data': [
            {
                'values': lab_scores_proportions.values,
                'labels': lab_scores_proportions.index,
                'type': 'pie',
                'name': 'Lab Scores',
                'hoverinfo': 'label+percent+name',
                'hole': .3,
            }
        ],
        'layout': {
            'title': 'Lab Performance Analysis',
        }
    }
)


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
            # Modify the range to include years after 2016
            'xaxis': {'title': 'Year', 'range': [2010, 2016]},
            'yaxis': {'title': 'Average Marks'},
        }
    }
)


# Histogram for Credit and Pointer Distribution
histogram = dcc.Graph(
    id='histogram',
    figure={
        'data': [
            {
                'x': marks['creditObt40'],
                'name': 'CreditsObtained',
                'type': 'histogram',
                'opacity': 0.75
            },
            {
                'x': marks['pointer10'],
                'name': 'Pointers',
                'type': 'histogram',
                'opacity': 0.75
            }
        ],
        'layout': {
            'title': 'Credit and Pointer Distribution',
            'xaxis': {'title': 'Value'},
            'yaxis': {'title': 'Number of Students'},
            'barmode': 'overlay'
        }
    }
)

# Add histogram to the layout

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
                'name': x
            } for x in teacher_marks.groups
        ],
        'layout': {
            'title': 'Teacher-wise Performance Comparison',
            'yaxis': {'title': 'Marks'},
        }
    }
)


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
                'name': 'Avg Grade'
            }
        ],
        'layout': {
            'title': 'Attendance Impact on Grades',
            'xaxis': {'title': 'Attendance Percentage'},
            'yaxis': {'title': 'Average Grade'},
        }
    }
)

# Add line graph to the layout


# Scatter plot for correlation between Theory and Lab Scores
scatter_plot = dcc.Graph(
    id='scatter',
    figure={
        'data': [
            {
                'x': marks['theoryConverted60'],
                'y': marks['labConverted40'],
                'mode': 'markers',
                'name': 'Students'
            }
        ],
        'layout': {
            'title': 'Correlation between Theory and Lab Scores',
            'xaxis': {'title': 'Theory Scores'},
            'yaxis': {'title': 'Lab Scores'},
        }
    }
)

# Add scatter plot to the layout


# Calculate average scores for each exam type
average_ise = marks['iseA20'].mean()
average_mse = marks['mse30'].mean()
average_ese = marks['ese100'].mean()

# Create bar chart
bar_chart = dcc.Graph(
    id='graph',
    figure={
        'data': [
            {'x': ['ISE', 'MSE', 'ESE'], 'y': [average_ise, average_mse,
                                               average_ese], 'type': 'bar', 'name': 'Avg Score'},
        ],
        'layout': {
            'title': 'Performance Distribution by Exam Type'
        }
    }
)

app.layout = html.Div(children=[
    html.H1(children='Performance Distribution by Exam Type'),
    bar_chart,
    html.H2(children='Correlation between Theory and Lab Scores'),
    scatter_plot,
    html.H3(children='Attendance Impact on Grades'),
    line_graph,
    html.H4(children='Teacher-wise Performance Comparison'),
    box_plot,
    html.H5(children='Credit and Pointer Distribution'),
    histogram,
    html.H6(children='Performance Over Time'),
    performance_line_graph,
    html.H1(children='Lab Performance Analysis'),
    pie_chart
])    


if __name__ == '__main__':
    app.run_server(debug=True)
