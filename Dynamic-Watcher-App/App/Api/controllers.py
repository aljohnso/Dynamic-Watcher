from flask import  request, redirect, url_for, \
     render_template, flash, Blueprint, jsonify, session
Api = Blueprint('Api', __name__, template_folder='templates')



