import os
from datetime import datetime
from functools import wraps
from apiclient import discovery
import apiclient as google
import flask
import httplib2
from flask import request, redirect, url_for, \
    render_template, flash, Blueprint, session
from oauth2client import client
from Database.Schema import db, CalenderData
from flask import jsonify

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
    return render_template("homePage.html")

@Main.route("/compare")
def compare():
    return "Yay"

@Main.route('/login', methods=['POST', 'GET'])
def login():
    """
    Retrieves the user's data from Google through gCallback, then has the user either make an account or go to the main page.
    :return:
    """
    if 'credentials' not in flask.session:  # Are they already authenticated? If not, then go to authentication.
        return flask.redirect(flask.url_for('Main.gCallback'))
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired:  # If the access token is expired, ask them to re-authenticate.
        return flask.redirect(flask.url_for('Main.gCallback'))
    else:  # If authenticated, get user info.
        http_auth = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http_auth)
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        eventsResult = service.events().list(
            calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        freeBusy = service.freebusy()
        print(freeBusy)
        events = eventsResult.get('items', [])
        print(events)
        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

        # http_auth = credentials.authorize(httplib2.Http())
        # service = google.discovery.build('oauth2', 'v2', http_auth)  # We ask for their profile information.
        # userinfo = service.userinfo().get().execute()  # Execute request.
        # print(userinfo)
        if events:
            #Bad assumption here that they use there calender TODO: FIX ME
            db.session.add(CalenderData(blob=events))
            db.session.commit()

        return redirect(flask.url_for("Main.compare"))


        # populate form with google data

        # print(flask.session)
        # return rendertemplate(create acoubt.html, form=form)
        # Account.query.filter_by(id=flask.session['Googledata']['id']).first().googleNum
        # if flask.session['Googledata']['id']==Account.query.filter_by(id=flask.session['Googledata']['id']).first().googleNum:


@Main.route('/gCallback')
def gCallback():
    """
    This handles authentication. Granted, we're not quite sure how... but it does.
    :return:
    """
    print(Main.root_path)
    secret = os.path.join(Main.root_path[:-8], 'secret/client_secret.json')  # access the secret file
    print(secret)
    # the -29 changes path to POA Website rather than the path to mainPage
    flow = client.flow_from_clientsecrets(secret, scope='https://www.googleapis.com/auth/calendar',
                                          redirect_uri=flask.url_for('Main.gCallback', _external=True))
    # ,include_granted_scopes=True)
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()  # sends request to google which redirects user to sign in
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')  # we have received a token form a user
        credentials = flow.step2_exchange(auth_code)  # authenticate that token with google
        flask.session['credentials'] = credentials.to_json()  # we have authenticated the user
        return flask.redirect(flask.url_for('Main.login'))  # once authenticated return to main page