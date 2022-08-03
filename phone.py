import re
from cgitb import html
import dash_bootstrap_components as dbc
from dash import html, get_asset_url
from dash_iconify import DashIconify

from send_sms import send_sms_to


class PhoneColorPalette:
    def __init__(self, color):
        self.colors = {
            'blue': ["#BBDEFB", "#EEFFFF", "#8AACC8", "#293137"],
            'green': ["#C8E6C9", "#FBFFFC", "#97B498", "#353D35"],
            'pink': ["#F8BBD0", "#FFFFFF", "#C9B2BA", "#423238"],
            'white': ["#FAFAFA", "#FFFFFF", "#C7C7C7", "#1A1A1A"], }

        self.top = self.colors[color][0]
        self.bg = self.colors[color][1]
        self.buttons = self.colors[color][2]
        self.high_contrast = self.colors[color][3]


class Phone(html.Div):
    def __init__(self, color, id, number="None", height="auto", width="auto", **kwargs):
        self.phone_id = id
        self.number = number
        self.recipient = "TDK"
        self.messages_list = ["Yes this is a test", "and another test"]
        if self.number == "None":
            self.number = "No number set"
            self.recipient = ""
            self.messages_list = []

        self.messages = html.Div([html.Div(
            f"{message}",
            style={"color": "black", "background-color": "white", "border-radius": "10px", "padding": "5px",
                   "border": "1px solid gray", "font-size": "0.8rem", "margin": "0.5rem"}) for message in
            self.messages_list],
            id={'label': 'phone-text', 'index': self.phone_id})

        if height != "auto" and width == "auto":
            value = float(re.sub("[^0-9]", "", height))
            measure = re.sub('[^a-zA-Z]+', '', height)
            width = str(value / 2) + measure
        elif height == "auto" and width != "auto":
            value = float(re.sub("[^0-9]", "", width))
            measure = re.sub('[^a-zA-Z]+', '', width)
            height = str(value * 2) + measure

        self.palette = PhoneColorPalette(color)

        super().__init__(
            # All the components/screens of the phone in order to load the ids.
            # However, only one is visible at a time.
            children=[
                self.messaging_screen("block"),
                self.main_screen("none")
            ],
            style={'color': 'white', 'backgroundColor': f"{self.palette.bg}",
                   "width": width, "height": height, "border": "7px gray ridge",
                   "borderRadius": "20px", "margin": "10px", "position": "relative"},
            className="phone",
            id={'label': 'phone-container', 'index': self.phone_id},
        )

    def messaging_screen(self, display):
        self.footer = html.Div([
            html.Div([
                dbc.Input(placeholder="Your text message", id={'label': 'phone-text-area', 'index': self.phone_id}),
                html.Div(DashIconify(icon="material-symbols:send-rounded", width=30, color=f"{self.palette.buttons}",
                                     ), id={'label': 'send-message-phone', 'index': self.phone_id},
                         className="send-button")
            ], className="d-flex flex-row justify-content-center align-items-center p-2 gap-2")
        ],
            style={"width": "100%", "position": "absolute", "bottom": "0%", "background-color": f"{self.palette.bg}",
                   "borderRadius": "0px 0px 10px 10px"})

        self.header = html.Div(
            [
                html.Div(
                    [html.Div(
                        DashIconify(icon="material-symbols:contact-page", width=30,
                                    color=f"{self.palette.high_contrast}"),
                        className="send-button", id={'label': 'phone-go-contact', 'index': self.phone_id}),
                        html.H6(self.recipient, style={"color": "black"})],
                    className="d-flex flex-row justify-content-center align-items-center p-2 gap-2"),
            ],

            id={'label': 'phone-top', 'index': self.phone_id},
            style={"width": "100%",
                   "min-height": "10%",
                   "position": "relative",
                   "height": "10%", "background-color": f"{self.palette.top}",
                   "borderRadius": "10px 10px 0px 0px",
                   "border-bottom": f"3px ridge {self.palette.buttons}"},
            className="d-flex flex-row justify-content-center align-items-center p-2")

        screen = html.Div([html.Div([  # Equivalent to `html.Div([...])`
            # Header
            self.header,

            # Messages
            self.messages,

            # Footer
        ], style={"position": "absolute", "top": "0px", "left": "0px", "bottom": "0px", "right": "0px",
                  "overflow": "auto"}),
            self.footer,

        ], id={"type": "messaging-screen", "index": self.phone_id}, style={"display": display})

        return screen

    def main_screen(self, display):
        screen = [html.Div([  # Equivalent to `html.Div([...])`
            # Messages
            # Div containing an icon for contact and another icon for messages
            html.Div(
                [
                    html.Title("Les iñages font chier"),
                    html.Img(src=get_asset_url("imgs/4278162.jpg"),
                             style={"width": "100%", "height": "100%", "position": "absolute", "top": "0px",
                                    "left": "0px",
                                    "border-radius": "10px", "z-index": "0"},
                             className="d-flex flex-row justify-content-center align-items-center"
                             ),
                    html.Div(DashIconify(icon="bxs:contact", width=60,
                                         color=f"{self.palette.high_contrast}"),
                             style={"z-index": "0"},
                             id={'label': 'phone-go-to-contact-list', 'index': self.phone_id}),
                    html.Div(DashIconify(icon="material-symbols:mail-outline", width=60,
                                         color=f"{self.palette.high_contrast}"),
                             style={"z-index": "0"},
                             id={'label': 'phone-go-to-mail', 'index': self.phone_id}),
                ],
                className="d-flex flex-row p-4 gap-3"
            ),

            # Footer
        ], style={"position": "absolute", "top": "0px", "left": "0px", "bottom": "0px", "right": "0px",
                  "overflow": "auto"}),

        ]
        return html.Div(screen, {"type": "main-screen", "index": self.phone_id}, style={"display": display})

    def send_sms(self, content, recipient):
        send_sms_to(content, recipient, self.number)


"""{'color': 'white', 'backgroundColor': f"{palette.bg}",
                       "width": width, "height": height, "border": "7px gray ridge",
                       "borderRadius": "20px", "margin": "10px"}"""
