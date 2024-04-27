from flask import Flask, render_template, request, jsonify
import requests
from math import radians, sin, cos, sqrt, atan2
import logging
from google.cloud import monitoring_v3
import time
import os
import time
import boto3
from datetime import datetime, timedelta

app = Flask(__name__)

# Logging Service
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

aws_access_key = 'AWS_ACCESS_KEY'
aws_secret_key = 'AWS_SECRET_KEY'
aws_region = 'AWS_REGION'

instance_id = 'EC2_INSTANCE_ID'

CLOUD_PROVIDERS = {
    'GCP': {'url': "https://tribal-bay-407302.oa.r.appspot.com/find_best_transportation",
            'coordinates': (51.509865, -0.118092)},
    'AWS': {'url': "http://3.144.72.249/find_best_transportation", 'coordinates': (37.774929, -122.419416)}
}

end_time = datetime.utcnow()
start_time = end_time - timedelta(minutes=15)

global ordered_providers

IPSTACK_API_KEY = "IPSTACK_API_KEY"


# User Interface Service
@app.route('/')
def index():
    return render_template('index.html')


def location_service(client_ip):
    ipstack_url = f"http://api.ipstack.com/{client_ip}?access_key={IPSTACK_API_KEY}"
    response = requests.get(ipstack_url)
    data = response.json()

    logging.debug(f"IP Stack Response: {data}")

    client_coordinates = (data.get('latitude', 0.0), data.get('longitude', 0.0))
    return client_coordinates


def calculate_distance(coord1, coord2):
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    R = 6371.0

    distance = R * c
    return distance

def get_gcp_utilization(project_id):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10 ** 9)

    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": seconds, "nanos": nanos},
            "start_time": {"seconds": (seconds - 604800), "nanos": nanos},
        }
    )

    results = client.list_time_series(
        name=project_name,
        filter='metric.type = "compute.googleapis.com/instance/cpu/utilization"',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    if results.points:
        last_point = results.points[-1]
        utilization_percentage = last_point.value.double_value * 100
        return utilization_percentage
    else:
        return None

def get_aws_utilization():
    cloudwatch = boto3.client('cloudwatch', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

    metric_name = 'CPUUtilization'
    namespace = 'AWS/EC2'
    dimensions = [{'Name': 'InstanceId', 'Value': instance_id}]

    response = cloudwatch.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'm1',
                'MetricStat': {
                    'Metric': {
                        'Namespace': namespace,
                        'MetricName': metric_name,
                        'Dimensions': dimensions
                    },
                    'Period': 60,  # 60 seconds (1 minute) granularity
                    'Stat': 'Average'
                },
                'ReturnData': True
            },
        ],
        StartTime=start_time,
        EndTime=end_time
    )

    if response['MetricDataResults'][0]['Values']:
        return response['MetricDataResults'][0]['Values'][0]
    else:
        return None

def load_balance_service(client_coordinates, enable_cpu_priority=True):
    global ordered_providers
    if enable_cpu_priority:
        for provider, details in CLOUD_PROVIDERS.items():
            if details['cpu_priority']:
                if provider == 'GCP':
                    cpu_utilization = get_gcp_utilization('tribal-bay-407302')
                elif provider == 'AWS':
                    cpu_utilization = get_aws_utilization()

                details['cpu_utilization'] = cpu_utilization

        # Order the providers based on utilization
        ordered_providers = sorted(CLOUD_PROVIDERS.keys(), key=lambda provider: (CLOUD_PROVIDERS[provider]['cpu_priority'], CLOUD_PROVIDERS[provider].get('cpu_utilization', float('inf'))))
    else:
        # Order the providers based on location
        ordered_providers = sorted(CLOUD_PROVIDERS.keys(), key=lambda provider: calculate_distance(client_coordinates,
                                                                                                   CLOUD_PROVIDERS[
                                                                                                       provider][
                                                                                                       'coordinates']))
    logging.debug(f"Ordered Cloud Providers: {ordered_providers}")

    chosen_provider = ordered_providers[0]

    logging.debug(f"Chosen Cloud Provider: {chosen_provider}")

    return chosen_provider


@app.route('/find_best_transportation', methods=['GET'])
def routing_service():
    from_city = request.args.get('from_city', '')
    to_city = request.args.get('to_city', '')

    client_ip = request.remote_addr

    logging.debug(f"Client IP: {client_ip}")

    client_coordinates = location_service(client_ip)

    logging.debug(f"Client Coordinates: {client_coordinates}")

    cloud_provider = load_balance_service(client_coordinates, False)

    provider_details = CLOUD_PROVIDERS.get(cloud_provider)

    if not provider_details:
        # Log an error if no provider is available
        logging.error("No provider available")
        return jsonify({"error": "No provider available"}), 400

    api_url = provider_details['url']

    # Log the request to the cloud provider
    logging.debug(f"Request sent to {cloud_provider} provider")

    response = requests.get(api_url, params={'from_city': from_city, 'to_city': to_city})

    # Retry Mechanism
    if response.status_code != 200:
        logging.warning(f"Request to {cloud_provider} failed, retrying with another provider")
        ordered_providers.remove(cloud_provider)
        new_chosen_provider = ordered_providers[0]
        new_provider_details = CLOUD_PROVIDERS.get(new_chosen_provider)

        if not new_provider_details:
            logging.error("No provider available after retry")
            return jsonify({"error": "No provider available after retry"}), 400

        api_url = new_provider_details['url']
        response = requests.get(api_url, params={'from_city': from_city, 'to_city': to_city})

    logging.debug(f"Response from {cloud_provider} provider: {response.json()}, Status Code: {response.status_code}")
    return jsonify(response.json()), response.status_code


if __name__ == '__main__':
    app.run(debug=True)
