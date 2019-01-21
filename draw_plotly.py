import plotly.graph_objs as go
from settlement import spline as spline


def draw(x, y):
    hover_text = ['Angular distortion: ' + '{:.2e}'.format(text_x) +
                  '<br>Horizontal strain: ' + '{:.2e}'.format(text_y)
                  for text_x, text_y in zip(list(x), list(y))]

    trace0 = go.Scatter(
        x=x,
        y=y,
        mode='markers',
        name='Points',
        marker=dict(
            size=5,
            color='grey',
            symbol='triangle-up'
        ),
        text=hover_text,
        hoverinfo='text',
        hoverlabel=dict(
            bordercolor='gray',
            bgcolor='lightgray',
            font=dict(
                size=12,
                family='consolas'
            )
        )
    )

    trace1 = go.Scatter(
        x=spline(([0.001, 0], [0, 0.0005]))[0],
        y=spline(([0.001, 0], [0, 0.0005]))[1],
        mode='lines',
        name='Negligible damage',
        line=dict(
            color='turquoise'
            ),
        hoverinfo='none'
    )

    trace2 = go.Scatter(
        x=spline(([0.0016, 0], [0, 0.00075]))[0],
        y=spline(([0.0016, 0], [0, 0.00075]))[1],
        mode='lines',
        name='Very slight damage',
        line=dict(
            color='gold'
            ),
        hoverinfo='none'
    )

    trace3 = go.Scatter(
        x=spline(([0.0032, 0], [0, 0.0015]))[0],
        y=spline(([0.0032, 0], [0, 0.0015]))[1],
        mode='lines',
        name='Slight damage',
        line=dict(
            color='red'
            ),
        hoverinfo='none'
    )

    trace4 = go.Scatter(
        x=spline(([0.0068, 0], [0, 0.003]))[0],
        y=spline(([0.0068, 0], [0, 0.003]))[1],
        mode='lines',
        name='Moderate to severe damage',
        line=dict(
            color='brown'
            ),
        hoverinfo='none'
    )

    layout = go.Layout(
        title='Relationship of Damage acc. Boscardin-Cording',
        hovermode='closest',
        autosize=False,
        width=1200,
        height=500,
        xaxis=dict(
            rangemode='nonnegative',
            tickformat='.1e',
            title='Angular distortion [m/m]',
            titlefont=dict(
                size=12)
            ),
        yaxis=dict(
            rangemode='nonnegative',
            tickformat='.1e',
            title='Horizontal extension strain [m/m]',
            titlefont=dict(
                size=12)
            ),
        legend=dict(
            x=0.8,
            y=1,
            traceorder='normal',
            font=dict(
                family='sans-serif',
                size=12,
                color='#000'
            ),
            bgcolor='#E2E2E2',
            bordercolor='#FFFFFF',
            borderwidth=2
        )
    )

    data = [trace4, trace3, trace2, trace1, trace0]

    return go.Figure(
        data=data,
        layout=layout
    )
