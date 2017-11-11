from flask import request, redirect, url_for, \
    render_template, flash, Blueprint, jsonify, session

Main = Blueprint('Main', __name__, template_folder='templates')


@Main.route('/')
def index():
    # print(os.getcwd())
    # with open(os.getcwd() + '/tests/inventoryGC.json') as data_file:
    #     data = json.load(data_file)
    # for item in data['data'].values():
    #     temp = Inventory(item)
    #     db.session.add(temp)
    #     db.session.commit()
    return "Hello World"
