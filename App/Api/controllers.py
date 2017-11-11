from flask import  request, redirect, url_for, \
     render_template, flash, Blueprint, jsonify, session
from Database.Schema import CalenderData
Api = Blueprint('Api', __name__, template_folder='templates')


@Api.route("/getUsers")
def getUsers():
     users = CalenderData.query.all()
     return jsonify(data= [i.serializeTable for i in users])
