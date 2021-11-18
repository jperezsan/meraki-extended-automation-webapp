from app import organization_data


def get_networks_dict(networks):    
    networks_dict = {}
    for network in networks:        
        networks_dict[network.get("id")] = network
    
    return networks_dict


def get_devices_dict(devices):    
    devices_dict = {}
    for device in devices:        
        devices_dict[device.get("serial")] = device
    
    return devices_dict


# Determine the loss average of each uplink
def get_loss_average(uplink):
    _sum = 0
    count = 0

    for item in uplink["timeSeries"]:        
        loss_percent = item["lossPercent"]
        if loss_percent is not None:
            _sum = _sum + loss_percent
            count += 1

    if count > 0:
        return _sum / count

    return 0


# Determine the latency average of each uplink
def get_latency_average(uplink):
    _sum = 0
    count = 0
    for item in uplink["timeSeries"]:
        latency = item["latencyMs"]        
        if latency is not None:
            _sum = _sum + latency
            count += 1

    if count > 0:
        return int(_sum / count)

    return 0

# Organization MX devices with uplinks and uplink status
def get_mx_devices_with_uplinks(organization_id, devices, networks_dict): 
                  
    uplinks = organization_data.dashboard.organizations.getOrganizationDevicesUplinksLossAndLatency(organization_id)    
    devices_dict = get_devices_dict(devices)
        
    # MX devices with uplinks information
    filtered_devices = {}
    
    for uplink in uplinks:
        if uplink["serial"] in devices_dict:
            if uplink["serial"] in filtered_devices:
                filtered_devices[uplink["serial"]]["uplinks"].append(
                    {
                        "uplink": uplink["uplink"],                            
                        "loss_average": get_loss_average(uplink),
                        "latency_average": get_latency_average(uplink),
                        "ip": uplink["ip"]
                    })
            else:
                device = devices_dict[uplink["serial"]]
                device["uplinks"] = []
                device["uplinks"].append({
                    "uplink": uplink["uplink"],                        
                    "loss_average": get_loss_average(uplink),
                    "latency_average": get_latency_average(uplink),
                    "ip": uplink["ip"]
                })
                if device["networkId"] in networks_dict:
                    device["networkName"] = networks_dict[device["networkId"]]
                    
                filtered_devices[device["serial"]] = device
        
    return filtered_devices


def get_hubs(org_id):
    hubs = []
    appliance_vpn_statuses = organization_data.dashboard.appliance.getOrganizationApplianceVpnStatuses(
        org_id, total_pages="all")

    try:
        for item in appliance_vpn_statuses:
            if str(item['vpnMode']) == "hub":
                temp = {"hubName": item["networkName"],
                        "hubId": item["networkId"], "hubSerial": item["deviceSerial"]}
                hubs.append(temp)

        return hubs

    except:
        print("Error!")
        print("Site-to-site VPN needs to be enabled for this organization")
        print("Map Monitoring and DC Switchover modules will not work")
        return None
    

# Assign color to network depending on latency, loss and active wans
def get_colored_networks(clean_networks, loss_tolerance, latency_tolerance, only_critical=False):
    if only_critical:
        critical_networks = clean_networks.copy()

    for key, network in clean_networks.items():                
        uplinks = network["uplinks"]                
        network["color"] = "Green"
        dead_uplinks = 0
        packet_loss_uplinks = 0
        high_latency_uplinks = 0

        for uplink in uplinks:
            # Restrict ip testing to 8.8.8.8 (Google) and Cisco Umbrella dns
            # TODO: Add testing IPs in the configuration
            if '8.8.8.8' not in uplink["ip"] and '208.67.222.222' not in uplink["ip"] and '208.67.220.220' not in uplink["ip"]:
                continue

            loss_value = uplink["loss_average"]            
            if loss_value is not None:
                if loss_value < loss_tolerance:
                    uplink["loss_status"] = "Good"
                    uplink["color"] = "Green"

                elif loss_value == 100:
                    uplink["loss_status"] = "Dead"
                    uplink["color"] = "Red"
                    dead_uplinks += 1
                    continue

                else:
                    uplink["loss_status"] = "Bad"
                    uplink["color"] = "Orange"
                    packet_loss_uplinks += 1
                    continue

            latency_value = uplink["latency_average"]
            if latency_value is not None:
                if latency_value > latency_tolerance:
                    uplink["latency_status"] = "Bad"
                    uplink["color"] = "Yellow"
                    high_latency_uplinks += 1
                else:
                    uplink["latency_status"] = "Good"
                    uplink["color"] = "Green"

        if dead_uplinks == len(uplinks):
            network["color"] = "Red"
            continue
        elif dead_uplinks > 0:
            network["color"] = "Blue"
            continue

        if packet_loss_uplinks == 0 and high_latency_uplinks == 0:
            if only_critical:
                del critical_networks[key]
                continue

        if packet_loss_uplinks > high_latency_uplinks:
            network["color"] = "Orange"
        elif high_latency_uplinks > 0:
            network["color"] = "Yellow"                

    if only_critical:
        return critical_networks

    return clean_networks
