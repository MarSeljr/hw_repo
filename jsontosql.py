import json
import psycopg2


def row_creator(device, devices_type):
    result = ()
    result += (None, devices_type + str(device["name"]))

    if "description" in device:
        result += (device["description"],)
    else:
        result += (None,)

    result += (str(device),None,None)

    if "Cisco-IOS-XE-ethernet:channel-group" in device:
        result += (device["Cisco-IOS-XE-ethernet:channel-group"]["number"],)
    else:
        result += (None,)

    if "mtu" in device:
        result += (device["mtu"],)
    else:
        result += (None,)

    return result


acceptable_types = ["Port-channel", "TenGigabitEthernet", "GigabitEthernet"]

with open("configClear_v2.json", "r") as file:
    data = json.load(file)
    conn = psycopg2.connect("dbname=jsontosql user=postgres password=Martin1234")
    cur = conn.cursor()
    for devices_type in acceptable_types:
        path = data["frinx-uniconfig-topology:configuration"]["Cisco-IOS-XE-native:native"]["interface"][devices_type]
        for device in path:
            cur.execute("""INSERT INTO jsontosql (connection, name, description, config_json,
            type, infra_type, port_channel_id, max_frame_size)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",(row_creator(device, devices_type)))
            conn.commit()

cur.close()
conn.close()