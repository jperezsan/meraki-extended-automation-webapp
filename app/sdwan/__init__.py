from flask import Blueprint

from ..models import Permission

sdwan = Blueprint('sdwan', __name__)

from . import views, errors

@sdwan.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)