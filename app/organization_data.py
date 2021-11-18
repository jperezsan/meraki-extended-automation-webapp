import os
import meraki
from app import helpers


def init():
    global dashboard, organization_id, organization_name, networks, networks_dict, devices, mx_devices_with_uplinks, loss_tolerance, latency_tolerance, colored_networks
    
    dashboard = meraki.DashboardAPI(
        api_key=os.getenv("MERAKI_DASHBOARD_API_KEY"),
        base_url='https://api.meraki.com/api/v1/',
        output_log=False,
        log_file_prefix=os.path.basename(__file__)[:-3],
        log_path='',
        print_console=False
    )
    
    print("-- Initializing Meraki organization data --")
    org_id = os.getenv("MERAKI_ORG_ID")
    
    ## General Data
    organization_name  = dashboard.organizations.getOrganization(org_id).get('name')
    networks = dashboard.organizations.getOrganizationNetworks(org_id)
    networks_dict = helpers.get_networks_dict(networks)
    devices = dashboard.organizations.getOrganizationDevices(org_id)    
    
    ## SDWAN Module Data
    mx_devices_with_uplinks = helpers.get_mx_devices_with_uplinks(org_id, devices, networks_dict)    
    loss_tolerance = 50
    latency_tolerance = 120      
    colored_networks = helpers.get_colored_networks(mx_devices_with_uplinks,
                                                    loss_tolerance,
                                                    latency_tolerance,
                                                    only_critical=False)            
    
    print("-- Done --")