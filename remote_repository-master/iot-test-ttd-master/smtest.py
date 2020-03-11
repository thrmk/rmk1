import os
import pathlib
import requests
import flask
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask import Flask, request,render_template
from flask_restful import Api
from flask_restful import Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objs as go
import dash_daq as daq
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask_restplus import reqparse#, Api, Resource, fields
#import log
from flask import Flask, render_template, request, jsonify, Response


#import werkzeug
#werkzeug.cached_property = werkzeug.utils.cached_property
#log=log.get_logger()

from datetime import datetime



import pandas as pd
FA = "https://use.fontawesome.com/releases/v5.8.1/css/all.css"
LOGO = "https://www.tirumala.org/NewImages/TTD-Logo.png"
LOGO1= "https://www.tirumala.org/NewImages/HD-TXT.png"

#app = Flask(__name__, static_url_path="/static/")
#app.config["CORS_HEADERS"] = "Content-Type"
#cors = CORS(app)



#apii = Api(app)
#model_400 = apii.model('ErrorResponse400', {
#                      'message': fields.String,
#'errors' :fields.Raw
#})

#model_500 = apii.model('ErrorResponse400', {
#'status': fields.Integer,
#'message':fields.String
#})

                                
devId1=0

server = flask.Flask(__name__)

server.config['DEBUG'] = True

server.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
server.secret_key = 'smarttrak'
api = Api(server)
db = SQLAlchemy()

db.init_app(server)

@server.before_first_request
def create_tables():
    db.create_all()

class DeviceModel(db.Model):
    __tablename__ = 'devices'

    count = db.Column(db.String(20),primary_key=True)
    devname = db.Column(db.String(15))
  
    tStamp= db.Column(db.String(25))
    rphvol = db.Column(db.Float(precision=2))
    yphvol = db.Column(db.Float(precision=2))
    bphvol = db.Column(db.Float(precision=2))
    
    
    
    def __init__(self, count,devname,tStamp,rphvol,yphvol,bphvol):
        self.tStamp= tStamp
        self.devname= devname
        self.count = count
        self.rphvol = rphvol
        self.yphvol = yphvol
        self.bphvol = bphvol
        


    def json(self):
        return {'devname':self.devname,'count': self.count,'tStamp':self.tStamp,'rphvol': self.rphvol,'yphvol': self.yphvol,'bphvol': self.bphvol}

    @classmethod
    def find_by_name(cls, count):
        return cls.query.filter_by(count=count).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class Device(Resource):
    parser = reqparse.RequestParser()
    print("parser=",parser) 
    parser.add_argument('devname',
        type=str
    )

    parser.add_argument('tStamp',
        type=str
    )
    parser.add_argument('rphvol',
        type=float
    )
    parser.add_argument('yphvol',
        type=float
    )
    parser.add_argument('bphvol',
        type=float
    )
    
    
    def get(self, count):
        device = DeviceModel.find_by_name(count)
        if device:
            return device.json()
        return {'message': 'Device not found'}, 404

    def post(self, count):
        global devId1
        devId1 =devId1 +1
        count =str(devId1)
        print("Reading No.=",count)
        data = Device.parser.parse_args()
        print("data=",data)
        device = DeviceModel.find_by_name(count)

        if device is None:
            device = DeviceModel(count,data['devname'],data['tStamp'],data['rphvol'],data['yphvol'],data['bphvol'])
            print("device=",device)

        else:
            device.devname= data['devname']
            device.tStamp = data['tStamp']
            device.rphvol = data['rphvol']
            device.yphvol = data['yphvol']
            device.bphvol = data['bphvol']
           
          
            
        try:
            device.save_to_db()
        except:
            return {"message": "An error occurred inserting the device data."}, 500

        return device.json(), 201


    """def put(self, devId):
        data = Device.parser.parse_args()

        device = DeviceModel.find_by_name(devId)

        if device is True:
            
            device = DeviceModel(devId, data['rphvol'],data['yphvol'],data['bphvol'])

        else:
            device.rphvol = data['rphvol']
            device.yphvol = data['yphvol']
            device.bphvol = data['bphvol']
            
            
            
        device.save_to_db()

        return device.json()"""



class DeviceList(Resource):
    def get(self):
        x= {'devices': [x.json() for x in DeviceModel.query.all()]}
        return x



#@server.route('/')
#def index():
    #devices = DeviceModel.query.all()
    #return render_template('index.html',devices=devices)

api.add_resource(Device, '/device/<string:count>')
api.add_resource(DeviceList, '/devices')

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

params = [
    'count','Devname','rphvol','yphvol','bphvol']

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "15rem",
    "padding": "2rem 2rem",
    "fontSize":"30rem"
}
collapse = html.Div(
    [
        dbc.Button("Menu",id="collapse-button",className="mb-4",color="primary"),
        dbc.Container(dbc.Collapse(
            children=[dbc.DropdownMenu(nav=True,in_navbar=True,label="Substations",
            children=[
                dbc.DropdownMenu(nav=True,in_navbar=True,label="SUB 1",
                    children=[
                        dbc.DropdownMenuItem(dbc.NavLink("Dev 1",href="/Dev-1",id="dev-1")),dbc.DropdownMenuItem(divider=True),dbc.DropdownMenuItem(dbc.NavLink("Dev 2",href="/Dev-2",id="dev-2")),dbc.DropdownMenuItem(divider=True),
                            dbc.DropdownMenuItem(dbc.NavLink("Dev 3",href="/Dev-3",id="dev-3"))]),
                           dbc.DropdownMenu(nav=True,in_navbar=True,label="SUB 2",
                               children=[
                                   dbc.DropdownMenuItem(dbc.NavLink("SVM 1",href="/SVM-1",id="svm-1")),dbc.DropdownMenuItem(divider=True),dbc.DropdownMenuItem(dbc.NavLink("SVM 2",href="/SVM 2",id="svm-2")),dbc.DropdownMenuItem(divider=True),
                            dbc.DropdownMenuItem(dbc.NavLink("SVM 3",href="/SVM-3",id="svm-3"))])]),
                    dbc.DropdownMenu(nav=True,in_navbar=True,label="Streetlights",
                        children=[
                dbc.DropdownMenu(nav=True,in_navbar=True,label="SL 1",
                    children=[
                        dbc.DropdownMenuItem(dbc.NavLink("JEO 1",href="/jeo-1")),dbc.DropdownMenuItem(divider=True),dbc.DropdownMenuItem(dbc.NavLink("JEO 2",href="/jeo 2")),dbc.DropdownMenuItem(divider=True),
                            dbc.DropdownMenuItem(dbc.NavLink("JEO 3",href="/jeo 3"))]),
                           dbc.DropdownMenu(nav=True,in_navbar=True,label="SL 2",
                               children=[
                                   dbc.DropdownMenuItem(dbc.NavLink("SVSD 1",href="/SVSD-1")),dbc.DropdownMenuItem(divider=True),dbc.DropdownMenuItem(dbc.NavLink("SVSD 2",href="/SVSD 2")),dbc.DropdownMenuItem(divider=True)])])],                                                                  
                                
    id="collapse"),style={"backgroundColor":"grey","width":"auto"})])     

sidebar = html.Div(
        [
       dbc.Row(
            html.Img(src=LOGO,height="100px",width="auto"),style={"padding-left":0}),
                
            dbc.Nav(collapse, vertical=True)
  ] ,
style={
    "position": "absolute",
    "top": 0,
    "left":"2rem",
    "bottom": 0,
    "width": "12rem",
    "padding": "1rem 0rem",
    "backgroundColor":"light"},
     id="sidebar",
)
button =html.Div(
           dbc.Row(
              [
                  dbc.Col(dbc.Button("Login",color="primary",className="mb-3",href="#"),style={"padding-left":"20rem","width":"15rem"})]))
navbar = dbc.Navbar(
           html.Div(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.NavbarBrand(
                                html.H2((html.Img(src=LOGO1,height="90px",width="auto"))),style={"fontSize":"50px","padding-left":"20rem"})),
                        dbc.NavbarToggler(id="navbar-toggler"),
                         dbc.Collapse(sidebar,id="sidebar-collapse",navbar=True),
                         dbc.Collapse(button,id="button-collapse",navbar=True)
                        ],

                    align="center",
                    no_gutters=True,
                ),
             ),
          )
content = html.Div(id="page-content", style=CONTENT_STYLE)

data1= html.Div([
        html.H4('Substation Data Live Feed'),
        html.Table(id="live-update-text"),],style={"overflowX":"scroll"}) 

app = dash.Dash(__name__,server=server,external_stylesheets=[dbc.themes.BOOTSTRAP, FA])

app.config['suppress_callback_exceptions']=True

def table(devices):
    table_header=[
        html.Thead(html.Tr([html.Th('Reading No.'),html.Th('dev name') ,html.Th('tstamp'), html.Th('rphV') ,
            html.Th('yphV') , html.Th('bphV')]))]
    table_body=[
        html.Tbody(html.Tr([html.Td(dev.count),html.Td(dev.devname),html.Td(dev.tStamp), html.Td(dev.rphvol) ,
            html.Td(dev.yphvol) , html.Td(dev.bphvol)]))for dev in devices]
    table=dbc.Table(table_header+table_body,bordered=True,striped=True,hover=True,style={"backgroundColor":"white"})
    return table



app.layout = html.Div([navbar,content,data1,dcc.Location(id="url",refresh=False)])

@app.callback(Output("live-update-text", "children"),
              [Input("live-update-text", "className")])


def update_output_div(input_value):
    devices = DeviceModel.query.all()

    return [html.Table(table(devices)
        )]
                      


@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
for i in range(1,4):
    @app.callback(
         Output("dev-{%d}"%i, "active"),
         [Input("url", "pathname")],
         )
    def toggle_active_links(pathname):
        if pathname == "/":
        # Treat page 1 as the homepage / index
            return True, False, False
        return [pathname == "/Dev-{%d}"%i]

@app.callback([Output("page-content", "children")],
        [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/Dev-1"]:

        return [
                html.H4("Displays Device 1 Graph")]
    elif pathname in ["/", "/Dev-2"]:

        return [
                html.H4("Displays Device 2 Graph")]
    elif pathname in ["/", "/Dev-3"]:

        return [
                html.H4("Displays Device 3 Graph")]
    
   # If the user tries to reach a different page, return a 404 message
    return [404]





if __name__ == '__main__':
    app.run_server(debug=True)
