import os
from datetime import datetime, timedelta

import boto3
import pytz


def ec2_stop(event, context):
    region = 'ap-southeast-2'
    print('Starting the ec2 stop lambda functionality')
    ec2_client = boto3.client('ec2')
    # Get list of regions
    regions = [region['RegionName']
               for region in ec2_client.describe_regions()['Regions']]
    # tags = os.environ['TAGS']
    tags = os.environ['AVAILABILITY_TAG_VALUES']
    # stop_tags_filter_arr = list(map(lambda x: create_filter_obj(x), tags.split(",")))
    stop_tags_filter_arr = get_eligible_stop_filters(tags.split(","))
    print('stop tags {}',stop_tags_filter_arr)
    ec2 = boto3.resource('ec2', region_name=region)
    # Get only running instances
    all_found_running_instances = []
    for created_tag_filter in stop_tags_filter_arr:
        instances = ec2.instances.filter(
            Filters=[created_tag_filter, {'Name': 'instance-state-name', 'Values': ['running']}])
        for instance in instances:
            all_found_running_instances.append(instance)
    # Stop the instances
    for instance in all_found_running_instances:
        instance.stop()
        print('Stopped instance: ', instance.id)

    start_tags_filter_arr = get_eligible_start_filters(tags.split(","))
    print('start tags {}',start_tags_filter_arr)
    all_found_stopped_instances = []
    for created_tag_filter in start_tags_filter_arr:
        instances = ec2.instances.filter(
            Filters=[created_tag_filter, {'Name': 'instance-state-name', 'Values': ['stopped']}])
        for instance in instances:
            all_found_stopped_instances.append(instance)
    # Stop the instances
    for instance in all_found_stopped_instances:
        instance.start()
        print('Started instance: ', instance.id)


print('Successfully executed the ec2 stop lambda functionality')


# def get_start_end_time_array():
#     start_stop_arr = []
#     now = datetime.now()
#
#     day_int = now.weekday()
#     if day_int <= 5:
#         start_date = now + timedelta(days=5 - day_int)
#     else:
#         start_date = now + timedelta(6)
#     local_tz = pytz.timezone('Australia/Sydney')
#     local_time = add.astimezone(local_tz)
#     print(local_time)


def get_eligible_stop_filters(tags):
    now = datetime.strptime(os.environ['CURR_TIME'],
                            "%m/%d/%Y, %H:%M:%S") if "CURR_TIME" in os.environ is not None else datetime.now()
    local_tz = pytz.timezone('Australia/Sydney')
    local_time = now.astimezone(local_tz)
    tags_arr = []
    for tag in tags:
        tag_start_end_date = get_valid_tags(tag)
        print(tag_start_end_date)
        if tag_start_end_date is not None and tag_start_end_date['stop_from_date'] <= local_time <= tag_start_end_date[
            'stop_to_date']:
            tags_arr.append({'Name': 'tag:{}'.format('Availability'),
                             'Values': [tag]})
    return tags_arr


def get_eligible_start_filters(tags):
    now = datetime.strptime(os.environ['CURR_TIME'],
                            "%m/%d/%Y, %H:%M:%S") if "CURR_TIME" in os.environ is not None else datetime.now()
    local_tz = pytz.timezone('Australia/Sydney')
    local_time = now.astimezone(local_tz)
    tags_arr = []

    for tag in tags:
        tag_start_end_date = get_valid_tags(tag)
        print(tag_start_end_date)
        if tag_start_end_date is not None and local_time > tag_start_end_date['start_from_date']:
            tags_arr.append({'Name': 'tag:{}'.format('Availability'),
                             'Values': [tag]})
    return tags_arr


def get_valid_tags(pattern):
    now = datetime.strptime(os.environ['CURR_TIME'],
                            "%m/%d/%Y, %H:%M:%S") if "CURR_TIME" in os.environ is not None else datetime.now()
    now = now.replace(hour=0, second=0, microsecond=0, minute=0)
    local_tz = pytz.timezone('Australia/Sydney')
    local_time = now.astimezone(local_tz)
    day_int = now.weekday()
    print('day int : {}'.format(day_int))
    if pattern == "24x5_Mon-Fri":
        start_from_date = local_time + timedelta(days=day_int)
        print('start from data : {}'.format(start_from_date))
        if day_int <= 5:
            stop_from_date = local_time + timedelta(days=5 - day_int)
            stop_to_date = local_time + timedelta(days=(5 - day_int) + 2)
        else:
            stop_from_date = local_time + timedelta(days=day_int + 6)
            stop_to_date = local_time + timedelta(days=day_int + 1)
        return {'stop_from_date': stop_from_date, 'stop_to_date': stop_to_date, 'start_from_date': start_from_date}


def create_filter_obj(tag):
    tag_split = tag.split("=")
    tag_key = tag_split[0]
    tag_value = tag_split[1]
    return {'Name': 'tag:{}'.format(tag_key),
            'Values': [tag_value]}
