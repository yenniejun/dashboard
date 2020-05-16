import dash
import dash_core_components as dcc
import dash_html_components as html
import graphs

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'dash.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(children=[
    html.H1(
        className="app-title",
        children='NYC Dashboard'),

    html.H2(
        className="app-subtitle",
        children='Noise'
    ),

    html.Hr(),

    # html.Div(
    #     className="app-header",
    #     children='''
    #     Dash: A web application framework for Python.
    # '''),

    dcc.Graph(
        animate=True,
        figure=graphs.noise_graph("overall")
                                    
    ),

    dcc.Graph(
        animate=True,
        figure=graphs.noise_graph_borough()
    ),

    # dcc.Graph(
    #     animate=True,
    #     figure=graphs.noise_graph_zip()
    # )
])

if __name__ == '__main__':
    app.run_server(debug=True)


