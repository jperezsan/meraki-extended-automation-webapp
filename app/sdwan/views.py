from flask.helpers import flash
from . import sdwan
from flask import render_template, Response, request
from flask_login import login_required
import json
from .. import organization_data
from .. import helpers
from ..models import Permission
from ..decorators import permission_required
import os

@sdwan.route('/', methods=['GET'])
@login_required
@permission_required(Permission.MAP_MONITORING)
def index():    
    return render_template('sdwan/index.html', title='SDWAN module')


@sdwan.route('/mapMonitoring', methods=['GET'])
@login_required
@permission_required(Permission.MAP_MONITORING)
def map_monitoring():       
    faulty_filter = request.args.get('filter')
    if faulty_filter is not None:
        if "True" in faulty_filter:
            flash("Showing only faulty networks")
            organization_data.colored_networks = helpers.get_colored_networks(organization_data.mx_devices_with_uplinks,
                                                                        organization_data.loss_tolerance,
                                                                        organization_data.latency_tolerance, True)
    else:
        organization_data.colored_networks = helpers.get_colored_networks(organization_data.mx_devices_with_uplinks,
                                                                    organization_data.loss_tolerance,
                                                                    organization_data.latency_tolerance, False) 
    return render_template('sdwan/mapMonitoring.html', title='SDWAN - Map Monitoring', here_maps_api_key = os.getenv('HERE_MAPS_API_KEY'))

@sdwan.route('/mx-devices', methods=['GET'])
@login_required
@permission_required(Permission.MAP_MONITORING)
def get_mx_devices():
    return Response(json.dumps(organization_data.colored_networks), mimetype='application/json')