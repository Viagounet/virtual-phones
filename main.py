import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, State, html, ALL, MATCH

from phone import PhoneColorPalette, Phone

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

phones = [Phone("blue", height="80vh", number="+1 719 212 2797", id=0),
          Phone("green", height="80vh", id=1),
          Phone("pink", height="80vh", id=2),
          Phone("white", height="80vh", id=3)]

app.layout = dbc.Container(
    html.Div([html.Div([phone, html.P(phone.number)]) for phone in phones],
             className="d-flex flex-row"),
    className="p-5 d-flex flex-column")


@app.callback(
    Output({'label': 'phone-text', 'index': MATCH}, "children"),
    [Input({'label': 'send-message-phone', 'index': MATCH}, "n_clicks")],
    State({'label': 'phone-text-area', 'index': MATCH}, "value"),
    prevent_initial_call=True
)
def send_input(n_clicks, value):
    if n_clicks is None:
        return "Please enter a number"
    else:
        phones[0].send_sms(value, "+33637890663")
        return "The number you entered is {}".format(value)


if __name__ == "__main__":
    app.run_server(debug=True)
