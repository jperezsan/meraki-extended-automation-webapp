from flask import Blueprint, current_app

from ..models import Permission

auth = Blueprint('auth', __name__)

from . import views
from ..models import User

@auth.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)

