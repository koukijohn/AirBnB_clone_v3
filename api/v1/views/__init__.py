#!/usr/bin/python3
from flask import Blueprint
app_views = Blueprint('app_views', __name__)
from api.v1.views.index import *
# import api.v1.views.states as states
from api.v1.views import states
from api.v1.views import cities
from api.v1.views import amenities
from api.v1.views import users
from api.v1.views import places
