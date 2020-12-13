import os
from datetime import datetime, timedelta

import boto3
import pytz
from botocore.exceptions import ClientError
from dateutil.parser import parse


def ec2_stop_start(event, context):
    os.environ['TZ'] = 'UTC'
    region = os.environ['REGION']
    print('Starting the ec2 stop lambda functionality')

    tags = os.environ['AVAILABILITY_TAG_VALUES']
    stop_tags_filter_arr = get_eligible_stop_filters(tags.split(","))
    print('stop eligible tags {}', stop_tags_filter_arr)
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
    print('start eligible tags {}', start_tags_filter_arr)
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

    handle_email_alerts_for_non_compliant_instances()
    print('Successfully executed the ec2 stop lambda functionality')


def handle_email_alerts_for_non_compliant_instances():
    email_from = os.environ['EMAIL_FROM']
    email_to = os.environ['EMAIL_TO']
    email_subject = os.environ['EMAIL_SUBJECT']
    email_charset = os.environ['EMAIL_CHARSET']

    email_alert_flag = True if "true" in os.environ["EMAIL_ALERTS_FLAG"] else False
    ec2_client = boto3.client('ec2', os.environ['REGION'])
    reservations = ec2_client.describe_instances().get('Reservations', [])
    email_content_for_invalid_instances = build_email_body_content_for_invalid_tags_or_maintenance_instances_and_stop_invalid_value_intances(
        reservations)

    if email_alert_flag and len(email_content_for_invalid_instances) > 0:
        ses_client = boto3.client('ses', region_name='us-west-2')
        try:
            email_body = " ".join(email_content_for_invalid_instances)
            print('email body : {}'.format(email_body))
            response = ses_client.send_email(
                Destination={'ToAddresses': [email_to, ], },
                Message={'Body': {
                    'Text': {
                        'Charset': email_charset,
                        'Data': email_body, }, },
                    'Subject': {
                        'Charset': email_charset,
                        'Data': email_subject, }, },
                Source=email_from)
            print("Email sent! Message ID: {}".format(response['MessageId']))
        except ClientError as e:
            print(e.response['Error']['Message'])


def build_email_body_content_for_invalid_tags_or_maintenance_instances_and_stop_invalid_value_intances(reservations):
    email_body_text = []
    ec2_client = boto3.client('ec2', os.environ['REGION'])
    for reservation in reservations:
        for instance in reservation['Instances']:
            instance_state = instance['State']['Name']
            tags = {}
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    tags[tag['Key']] = tag['Value']
                if os.environ['TAG_NAME'] in tags:
                    availability_tag = tags[os.environ['TAG_NAME']]
                    availability_tag_lower = availability_tag.lower()
                    if 'maint' in availability_tag_lower:
                        email_body_text.append(
                            'WARNING: Instance {} is tagged for Maintenance! \n'.format(str(instance['InstanceId'])))
                    else:
                        if availability_tag not in os.environ['AVAILABILITY_TAG_VALUES']:
                            email_body_text.append(
                                'ERROR: Instance {} has a non-compliant value! \n'.format(str(instance['InstanceId'])))
                            if instance_state == "running":
                                ec2_client.stop_instances(InstanceIds=[str(instance['InstanceId'])])
                                print('Stopped instance id : {} as it has an invalid value : {}'.format(str(instance['InstanceId']), availability_tag))
    return email_body_text


def get_eligible_stop_filters(tags):
    now = parse(os.environ['CURR_TIME']) if "CURR_TIME" in os.environ is not None else datetime.now()
    local_tz = pytz.timezone('Australia/Sydney')
    local_time = now.astimezone(local_tz)
    print('local time : {}'.format(local_time))
    tags_arr = []
    for tag in tags:
        tag_start_end_date = get_valid_tags(tag)
        print('tag : {}', tag)
        print('start and end date params : {}'.format(tag_start_end_date))
        if tag_start_end_date is not None and tag_start_end_date['stop_from_date'] is not None and \
                tag_start_end_date['stop_to_date'] is not None and tag_start_end_date['stop_from_date'] <= local_time <= \
                tag_start_end_date[
                    'stop_to_date']:
            tags_arr.append({'Name': 'tag:{}'.format(os.environ['TAG_NAME']),
                             'Values': [tag]})
        else:
            print(tag_start_end_date)
            print(local_time)
            if tag_start_end_date is not None and tag_start_end_date['stop_from_date'] is not None and \
                    tag_start_end_date['stop_to_date'] is None and \
                    tag_start_end_date[
                        'stop_from_date'] <= local_time:
                tags_arr.append({'Name': 'tag:{}'.format(os.environ['TAG_NAME']),
                                 'Values': [tag]})
    return tags_arr


def get_eligible_start_filters(tags):
    local_tz = pytz.timezone('Australia/Sydney')
    now = parse(os.environ['CURR_TIME']) if "CURR_TIME" in os.environ is not None else datetime.now()
    local_time = now.astimezone(local_tz)
    tags_arr = []
    print('local time : {}'.format(local_time))
    for tag in tags:
        tag_start_end_date = get_valid_tags(tag)
        print('tag : {}', tag)
        print('start and end date params : {}'.format(tag_start_end_date))
        if tag_start_end_date is not None and tag_start_end_date['start_from_date'] is not None \
                and tag_start_end_date['start_end_date'] is not None and local_time > \
                tag_start_end_date['start_from_date'] and \
                local_time < tag_start_end_date['start_end_date']:
            tags_arr.append({'Name': 'tag:{}'.format(os.environ['TAG_NAME']),
                             'Values': [tag]})
        else:
            if tag_start_end_date is not None and tag_start_end_date['start_end_date'] is None \
                    and tag_start_end_date['start_from_date'] is not None \
                    and local_time > \
                    tag_start_end_date['start_from_date']:
                tags_arr.append({'Name': 'tag:{}'.format(os.environ['TAG_NAME']),
                                 'Values': [tag]})

    return tags_arr


def get_valid_tags(pattern):
    now = parse(os.environ['CURR_TIME']) if "CURR_TIME" in os.environ is not None else datetime.now()
    local_tz = pytz.timezone('Australia/Sydney')
    local_time = now.astimezone(local_tz)
    local_time = local_time.replace(hour=0, second=0, microsecond=0, minute=0)
    day_int = local_time.weekday()
    stop_from_date = None
    stop_to_date = None
    start_from_date = None
    start_end_date = None
    if pattern == "24x5_Mon-Fri":
        if 0 <= day_int <= 4:
            start_from_date = local_time
            start_end_date = None
        else:
            start_from_date = None
            start_end_date = None
            stop_from_date = local_time
            stop_to_date = local_time + timedelta(days=1)
    if pattern == "08-24_Mon-Fri":
        if 0 <= day_int <= 4:
            stop_from_date = local_time
            stop_to_date = local_time + timedelta(hours=8)
            start_from_date = local_time + timedelta(hours=8)
            start_end_date = local_time + timedelta(hours=24)
        else:
            stop_from_date = local_time
            stop_to_date = local_time + timedelta(days=1)
            start_from_date = None
            start_end_date = None
    if pattern == "08-18_Mon-Sun":
        stop_from_date = local_time + timedelta(hours=18)
        stop_to_date = local_time + timedelta(hours=32)
        start_from_date = local_time + timedelta(hours=8)
        start_end_date = local_time + timedelta(hours=18)
    if pattern == "08-18_Mon-Fri":
        if 0 <= day_int <= 4:
            stop_from_date = local_time + + timedelta(hours=18)
            stop_to_date = local_time + timedelta(hours=32)
            start_from_date = local_time + timedelta(hours=8)
            start_end_date = local_time + timedelta(hours=18)
        else:
            stop_from_date = local_time
            stop_to_date = local_time + timedelta(days=1)
            start_from_date = None
            start_end_date = None
    if pattern == "18_Shutdown":
        stop_from_date = local_time + timedelta(hours=18)
        stop_to_date = None
        start_from_date = None
        start_end_date = None
    if pattern == "24x7_Mon-Sun":
        stop_from_date = None
        stop_to_date = None
        start_from_date = local_time
        start_end_date = None

    return {'stop_from_date': stop_from_date, 'stop_to_date': stop_to_date, 'start_from_date': start_from_date,
            'start_end_date': start_end_date}
