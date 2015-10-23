from flask import Blueprint, session, redirect, current_app, request, url_for
import functools

main = Blueprint('main', __name__)

from . import views, errors
