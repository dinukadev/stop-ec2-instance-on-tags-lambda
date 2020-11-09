import os
from datetime import datetime, timedelta

import boto3
import pytz
import yaml
from moto import mock_ec2

import handler as handler


@mock_ec2
def should_stop_ec2_instances_for_24x5_Mon_Fri_tag():
    os.environ['AVAILABILITY_TAG_VALUES'] = '24x5_Mon-Fri'
    local_tz = pytz.timezone('Australia/Sydney')
    datetime_object = datetime.strptime('Nov 14 2020 12:00AM', '%b %d %Y %I:%M%p')
    datetime_object = datetime_object.replace(tzinfo=local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")
    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop_start(None, None)

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
    instance_id_list = list(map(lambda x: x.id, instances))
    filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
    assert instance_id in filtered_instance_ids


@mock_ec2
def should_stop_ec2_instances_for_24x5_Mon_Fri_tag_if_date_has_passed():
    os.environ['AVAILABILITY_TAG_VALUES'] = '24x5_Mon-Fri'
    local_tz = pytz.timezone('Australia/Sydney')
    datetime_object = datetime.strptime('Nov 14 2020 1:00AM', '%b %d %Y %I:%M%p')
    datetime_object = datetime_object.replace(tzinfo=local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")
    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop_start(None, None)

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
    instance_id_list = list(map(lambda x: x.id, instances))
    filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
    assert instance_id in filtered_instance_ids

@mock_ec2
def should_stop_ec2_instances_for_24x5_Mon_Fri_tag_if_date_on_sunday():
    os.environ['AVAILABILITY_TAG_VALUES'] = '24x5_Mon-Fri'
    local_tz = pytz.timezone('Australia/Sydney')
    datetime_object = datetime.strptime('Nov 15 2020 1:00AM', '%b %d %Y %I:%M%p')
    datetime_object = datetime_object.replace(tzinfo=local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")
    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop_start(None, None)

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
    instance_id_list = list(map(lambda x: x.id, instances))
    filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
    assert instance_id in filtered_instance_ids




@mock_ec2
def should_start_ec2_instances_for_24x5_Mon_Fri_tag():
    os.environ['AVAILABILITY_TAG_VALUES'] = '24x5_Mon-Fri'
    local_tz = pytz.timezone('Australia/Sydney')
    datetime_object = datetime.strptime('Nov 9 2020 1:00AM', '%b %d %Y %I:%M%p')
    datetime_object = datetime_object.replace(tzinfo=local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")

    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']
    client.stop_instances(InstanceIds=[instance_id])

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop_start(None, None)

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    instance_id_list = list(map(lambda x: x.id, instances))
    filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
    assert instance_id in filtered_instance_ids


@mock_ec2
def should_start_ec2_instances_for_24x5_Mon_Fri_tag_if_on_tuesday():
    os.environ['AVAILABILITY_TAG_VALUES'] = '24x5_Mon-Fri'
    local_tz = pytz.timezone('Australia/Sydney')
    datetime_object = datetime.strptime('Nov 10 2020 1:00AM', '%b %d %Y %I:%M%p')
    datetime_object = datetime_object.replace(tzinfo=local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")

    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']
    client.stop_instances(InstanceIds=[instance_id])

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop_start(None, None)

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    instance_id_list = list(map(lambda x: x.id, instances))
    filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
    assert instance_id in filtered_instance_ids


@mock_ec2
def should_start_ec2_instances_for_24x5_Mon_Fri_tag_if_on_wednesday():
    os.environ['AVAILABILITY_TAG_VALUES'] = '24x5_Mon-Fri'
    local_tz = pytz.timezone('Australia/Sydney')
    datetime_object = datetime.strptime('Nov 11 2020 1:00AM', '%b %d %Y %I:%M%p')
    datetime_object = datetime_object.replace(tzinfo=local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")

    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']
    client.stop_instances(InstanceIds=[instance_id])

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop_start(None, None)

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    instance_id_list = list(map(lambda x: x.id, instances))
    filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
    assert instance_id in filtered_instance_ids

@mock_ec2
def should_start_ec2_instances_for_24x5_Mon_Fri_tag_if_on_thursday():
    os.environ['AVAILABILITY_TAG_VALUES'] = '24x5_Mon-Fri'
    local_tz = pytz.timezone('Australia/Sydney')
    datetime_object = datetime.strptime('Nov 12 2020 1:00AM', '%b %d %Y %I:%M%p')
    datetime_object = datetime_object.replace(tzinfo=local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")

    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']
    client.stop_instances(InstanceIds=[instance_id])

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop_start(None, None)

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    instance_id_list = list(map(lambda x: x.id, instances))
    filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
    assert instance_id in filtered_instance_ids



@mock_ec2
def should_start_ec2_instances_for_24x5_Mon_Fri_tag_if_on_friday():
    os.environ['AVAILABILITY_TAG_VALUES'] = '24x5_Mon-Fri'
    local_tz = pytz.timezone('Australia/Sydney')
    datetime_object = datetime.strptime('Nov 13 2020 1:00AM', '%b %d %Y %I:%M%p')
    datetime_object = datetime_object.replace(tzinfo=local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")

    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']
    client.stop_instances(InstanceIds=[instance_id])

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop_start(None, None)

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    instance_id_list = list(map(lambda x: x.id, instances))
    filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
    assert instance_id in filtered_instance_ids


@mock_ec2
def should_start_ec2_instances_for_24x5_Mon_Fri_tag_if_date_on_monday():
    os.environ['AVAILABILITY_TAG_VALUES'] = '24x5_Mon-Fri'
    local_tz = pytz.timezone('Australia/Sydney')
    datetime_object = datetime.strptime('Nov 16 2020 1:00AM', '%b %d %Y %I:%M%p')
    datetime_object = datetime_object.replace(tzinfo=local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")

    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']
    client.stop_instances(InstanceIds=[instance_id])

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop_start(None, None)

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    instance_id_list = list(map(lambda x: x.id, instances))
    filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
    assert instance_id in filtered_instance_ids


@mock_ec2
def should_start_ec2_instances_for_24x5_Mon_Fri_tag_if_date_passed():
    os.environ['AVAILABILITY_TAG_VALUES'] = '24x5_Mon-Fri'
    local_tz = pytz.timezone('Australia/Sydney')
    datetime_object = datetime.strptime('Nov 16 2020 1:00AM', '%b %d %Y %I:%M%p')
    datetime_object = datetime_object.replace(tzinfo=local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")

    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']
    client.stop_instances(InstanceIds=[instance_id])

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop_start(None, None)

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    instance_id_list = list(map(lambda x: x.id, instances))
    filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
    assert instance_id in filtered_instance_ids


@mock_ec2
def should_stop_ec2_instances_for_08_24_Mon_Fri_tag():
    os.environ['AVAILABILITY_TAG_VALUES'] = '08-24_Mon-Fri'
    local_tz = pytz.timezone('Australia/Sydney')
    datetime_object = datetime.strptime('Nov 9 2020 12:00AM', '%b %d %Y %I:%M%p')
    datetime_object = datetime_object.replace(tzinfo=local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")
    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop_start(None, None)

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
    instance_id_list = list(map(lambda x: x.id, instances))
    filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
    assert instance_id in filtered_instance_ids


@mock_ec2
def should_stop_ec2_instances_for_08_24_Mon_Fri_tag_if_still_before_8am():
    os.environ['AVAILABILITY_TAG_VALUES'] = '08-24_Mon-Fri'
    local_tz = pytz.timezone('Australia/Sydney')
    datetime_object = datetime.strptime('Nov 9 2020 7:59AM', '%b %d %Y %I:%M%p')
    datetime_object = datetime_object.replace(tzinfo=local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")
    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop_start(None, None)

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
    instance_id_list = list(map(lambda x: x.id, instances))
    filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
    assert instance_id in filtered_instance_ids

@mock_ec2
def should_start_ec2_instances_for_24x5_Mon_Fri_tag_if_after_8am():
    os.environ['AVAILABILITY_TAG_VALUES'] = '08-24_Mon-Fri'
    local_tz = pytz.timezone('Australia/Sydney')
    datetime_object = datetime.strptime('Nov 9 2020 8:01AM', '%b %d %Y %I:%M%p')
    datetime_object = datetime_object.replace(tzinfo=local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")

    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']
    client.stop_instances(InstanceIds=[instance_id])

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop_start(None, None)

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    instance_id_list = list(map(lambda x: x.id, instances))
    filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
    assert instance_id in filtered_instance_ids


@mock_ec2
def should_stop_ec2_instances_for_08_24_Mon_Fri_tag_if_saturday():
    os.environ['AVAILABILITY_TAG_VALUES'] = '08-24_Mon-Fri'
    local_tz = pytz.timezone('Australia/Sydney')
    datetime_object = datetime.strptime('Nov 14 2020 12:00AM', '%b %d %Y %I:%M%p')
    datetime_object = datetime_object.replace(tzinfo=local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")
    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop_start(None, None)

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
    instance_id_list = list(map(lambda x: x.id, instances))
    filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
    assert instance_id in filtered_instance_ids



@mock_ec2
def should_stop_ec2_instances_for_08_24_Mon_Fri_tag_if_sunday():
    os.environ['AVAILABILITY_TAG_VALUES'] = '08-24_Mon-Fri'
    local_tz = pytz.timezone('Australia/Sydney')
    datetime_object = datetime.strptime('Nov 15 2020 12:00AM', '%b %d %Y %I:%M%p')
    datetime_object = datetime_object.replace(tzinfo=local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")
    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop_start(None, None)

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
    instance_id_list = list(map(lambda x: x.id, instances))
    filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
    assert instance_id in filtered_instance_ids


@mock_ec2
def should_not_start_ec2_instances_for_24x5_Mon_Fri_tag_if_saturday():
    os.environ['AVAILABILITY_TAG_VALUES'] = '08-24_Mon-Fri'
    local_tz = pytz.timezone('Australia/Sydney')
    datetime_object = datetime.strptime('Nov 14 2020 12:01AM', '%b %d %Y %I:%M%p')
    datetime_object = datetime_object.replace(tzinfo=local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")

    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']
    client.stop_instances(InstanceIds=[instance_id])

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop_start(None, None)

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
    instance_id_list = list(map(lambda x: x.id, instances))
    filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
    assert instance_id in filtered_instance_ids



@mock_ec2
def should_not_start_ec2_instances_for_24x5_Mon_Fri_tag_if_sunday():
    os.environ['AVAILABILITY_TAG_VALUES'] = '08-24_Mon-Fri'
    local_tz = pytz.timezone('Australia/Sydney')
    datetime_object = datetime.strptime('Nov 15 2020 12:01AM', '%b %d %Y %I:%M%p')
    datetime_object = datetime_object.replace(tzinfo=local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")

    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']
    client.stop_instances(InstanceIds=[instance_id])

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop_start(None, None)

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
    instance_id_list = list(map(lambda x: x.id, instances))
    filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
    assert instance_id in filtered_instance_ids


@mock_ec2
def should_stop_ec2_instances_for_08_18_Mon_Sun_tag_if_after_6pm():
    os.environ['AVAILABILITY_TAG_VALUES'] = '08-18_Mon-Sun'
    local_tz = pytz.timezone('Australia/Sydney')
    datetime_object = datetime.strptime('Nov 9 2020 6:01PM', '%b %d %Y %I:%M%p')
    datetime_object = datetime_object.replace(tzinfo=local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")
    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop_start(None, None)

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
    instance_id_list = list(map(lambda x: x.id, instances))
    filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
    assert instance_id in filtered_instance_ids


@mock_ec2
def should_start_ec2_instances_for_08_18_Mon_Sun_tag_if_after_8am():
    os.environ['AVAILABILITY_TAG_VALUES'] = '08-18_Mon-Sun'
    local_tz = pytz.timezone('Australia/Sydney')
    datetime_object = datetime.strptime('Nov 9 2020 8:01AM', '%b %d %Y %I:%M%p')
    datetime_object = datetime_object.replace(tzinfo=local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")

    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']
    client.stop_instances(InstanceIds=[instance_id])

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop_start(None, None)

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    instance_id_list = list(map(lambda x: x.id, instances))
    filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
    assert instance_id in filtered_instance_ids

@mock_ec2
def should_stop_ec2_instances_for_08_18_Mon_Fri_tag_if_after_6pm():
    os.environ['AVAILABILITY_TAG_VALUES'] = '08-18_Mon-Fri'
    local_tz = pytz.timezone('Australia/Sydney')
    datetime_object = datetime.strptime('Nov 15 2020 6:00PM', '%b %d %Y %I:%M%p')
    datetime_object = datetime_object.replace(tzinfo=local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")
    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop_start(None, None)

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
    instance_id_list = list(map(lambda x: x.id, instances))
    filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
    assert instance_id in filtered_instance_ids


@mock_ec2
def should_stop_ec2_instances_for_08_18_Mon_Fri_tag_if_after_12am():
    os.environ['AVAILABILITY_TAG_VALUES'] = '08-18_Mon-Fri'
    local_tz = pytz.timezone('Australia/Sydney')
    datetime_object = datetime.strptime('Nov 15 2020 12:00AM', '%b %d %Y %I:%M%p')
    datetime_object = datetime_object.replace(tzinfo=local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")
    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop_start(None, None)

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
    instance_id_list = list(map(lambda x: x.id, instances))
    filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
    assert instance_id in filtered_instance_ids



@mock_ec2
def should_start_ec2_instances_for_08_18_Mon_Fri_tag_if_after_8am():
    os.environ['AVAILABILITY_TAG_VALUES'] = '08-18_Mon-Fri'
    local_tz = pytz.timezone('Australia/Sydney')
    datetime_object = datetime.strptime('Nov 9 2020 8:01AM', '%b %d %Y %I:%M%p')
    datetime_object = datetime_object.replace(tzinfo=local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")

    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']
    client.stop_instances(InstanceIds=[instance_id])

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop_start(None, None)

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    instance_id_list = list(map(lambda x: x.id, instances))
    filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
    assert instance_id in filtered_instance_ids


@mock_ec2
def should_start_ec2_instances_for_08_18_Mon_Fri_tag_if_after_9am():
    os.environ['AVAILABILITY_TAG_VALUES'] = '08-18_Mon-Fri'
    local_tz = pytz.timezone('Australia/Sydney')
    datetime_object = datetime.strptime('Nov 9 2020 9:00AM', '%b %d %Y %I:%M%p')
    datetime_object = datetime_object.replace(tzinfo=local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")

    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']
    client.stop_instances(InstanceIds=[instance_id])

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop_start(None, None)

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    instance_id_list = list(map(lambda x: x.id, instances))
    filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
    assert instance_id in filtered_instance_ids


@mock_ec2
def should_not_start_ec2_instances_for_8_18_Mon_Fri_tag_if_saturday():
    os.environ['AVAILABILITY_TAG_VALUES'] = '08-18_Mon-Fri'
    local_tz = pytz.timezone('Australia/Sydney')
    datetime_object = datetime.strptime('Nov 14 2020 12:01AM', '%b %d %Y %I:%M%p')
    datetime_object = datetime_object.replace(tzinfo=local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")

    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']
    client.stop_instances(InstanceIds=[instance_id])

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop_start(None, None)

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
    instance_id_list = list(map(lambda x: x.id, instances))
    filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
    assert instance_id in filtered_instance_ids



@mock_ec2
def should_not_start_ec2_instances_for_8_18_Mon_Fri_tag_if_sunday():
    os.environ['AVAILABILITY_TAG_VALUES'] = '08-18_Mon-Fri'
    local_tz = pytz.timezone('Australia/Sydney')
    datetime_object = datetime.strptime('Nov 15 2020 12:01AM', '%b %d %Y %I:%M%p')
    datetime_object = datetime_object.replace(tzinfo=local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")

    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']
    client.stop_instances(InstanceIds=[instance_id])

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop_start(None, None)

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
    instance_id_list = list(map(lambda x: x.id, instances))
    filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
    assert instance_id in filtered_instance_ids

@mock_ec2
def should_stop_ec2_instances_for_18_Shutdown_tag_if_after_6pm():
    os.environ['AVAILABILITY_TAG_VALUES'] = '18_Shutdown'
    local_tz = pytz.timezone('Australia/Sydney')
    datetime_object = datetime.strptime('Nov 15 2020 6:00PM', '%b %d %Y %I:%M%p')
    datetime_object = datetime_object.replace(tzinfo=local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")
    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop_start(None, None)

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
    instance_id_list = list(map(lambda x: x.id, instances))
    filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
    assert instance_id in filtered_instance_ids

@mock_ec2
def should_not_start_ec2_instances_for_18_Shutdown_tag_if_already_stopped():
    os.environ['AVAILABILITY_TAG_VALUES'] = '18_Shutdown'
    local_tz = pytz.timezone('Australia/Sydney')
    datetime_object = datetime.strptime('Nov 15 2020 6:00PM', '%b %d %Y %I:%M%p')
    datetime_object = datetime_object.replace(tzinfo=local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")

    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']
    client.stop_instances(InstanceIds=[instance_id])

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop_start(None, None)

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
    instance_id_list = list(map(lambda x: x.id, instances))
    filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
    assert instance_id in filtered_instance_ids


#
# @mock_ec2
# def test_should_not_stop_ec2_instances_without_matching_tag():
#     serverless_yaml = readYaml()
#     tags_from_serverless_yaml = serverless_yaml['provider']['environment']['TAGS']
#     os.environ['TAGS'] = tags_from_serverless_yaml
#     region = 'ap-southeast-2'
#     client = boto3.client('ec2', region_name=region)
#     reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=2, MaxCount=2)
#     instance_id = reservation['Instances'][0]['InstanceId']
#
#     tags = list(map(lambda x: create_tag_obj(x), tags_from_serverless_yaml.split(",")))
#
#     client.create_tags(Resources=[instance_id], Tags=tags)
#
#     handler.ec2_stop(None, None)
#
#     ec2 = boto3.resource('ec2', region_name=region)
#     instances = ec2.instances.filter(
#         Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
#     instance_id_list = list(map(lambda x: x.id, instances))
#     filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
#     assert instance_id in filtered_instance_ids
#
#     running_instances = ec2.instances.filter(
#         Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
#     running_instance_id_list = list(map(lambda x: x.id, running_instances))
#     assert len(running_instance_id_list) == 1
#
#
# @mock_ec2
# def test_should_match_multiple_tags():
#     os.environ['TAGS'] = 'Auto=On,Stop=true'
#     region = 'ap-southeast-2'
#     client = boto3.client('ec2', region_name=region)
#     reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
#     instance_id = reservation['Instances'][0]['InstanceId']
#
#     tags = list(map(lambda x: create_tag_obj(x), os.environ['TAGS'].split(',')))
#
#     client.create_tags(Resources=[instance_id], Tags=tags)
#
#     handler.ec2_stop(None, None)
#
#     ec2 = boto3.resource('ec2', region_name=region)
#     instances = ec2.instances.filter(
#         Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
#     instance_id_list = list(map(lambda x: x.id, instances))
#     filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
#     assert instance_id in filtered_instance_ids
#
#
# @mock_ec2
# def test_stop_multiple_instances_with_different_tags():
#     os.environ['TAGS'] = 'Auto=On,Stop=true'
#     region = 'ap-southeast-2'
#     client = boto3.client('ec2', region_name=region)
#     reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=2, MaxCount=2)
#     instance_id = reservation['Instances'][0]['InstanceId']
#     instance_id_two = reservation['Instances'][1]['InstanceId']
#
#     tags = list(map(lambda x: create_tag_obj(x), 'Auto=On'.split(',')))
#
#     client.create_tags(Resources=[instance_id], Tags=tags)
#
#     tags = list(map(lambda x: create_tag_obj(x), 'Stop=true'.split(',')))
#
#     client.create_tags(Resources=[instance_id_two], Tags=tags)
#
#     handler.ec2_stop(None, None)
#
#     ec2 = boto3.resource('ec2', region_name=region)
#     instances = ec2.instances.filter(
#         Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
#     instance_id_list = list(map(lambda x: x.id, instances))
#     filtered_instance_ids = list(filter(lambda x: x == instance_id or x == instance_id_two, instance_id_list))
#     assert instance_id in filtered_instance_ids
#     assert instance_id_two in filtered_instance_ids


def create_tag_obj(tag):
    return {'Key': 'Availability',
            'Value': tag}


def readYaml():
    with open("serverless.yml", "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exec:
            print(exec)
            sys.exit(1)


if __name__ == '__main__':
    should_stop_ec2_instances_for_24x5_Mon_Fri_tag()
    should_stop_ec2_instances_for_24x5_Mon_Fri_tag_if_date_has_passed()
    should_stop_ec2_instances_for_24x5_Mon_Fri_tag_if_date_on_sunday()
    should_start_ec2_instances_for_24x5_Mon_Fri_tag()
    should_start_ec2_instances_for_24x5_Mon_Fri_tag_if_date_passed()
    should_start_ec2_instances_for_24x5_Mon_Fri_tag_if_date_on_monday()
    should_start_ec2_instances_for_24x5_Mon_Fri_tag_if_on_tuesday()
    should_start_ec2_instances_for_24x5_Mon_Fri_tag_if_on_wednesday()
    should_start_ec2_instances_for_24x5_Mon_Fri_tag_if_on_thursday()
    should_start_ec2_instances_for_24x5_Mon_Fri_tag_if_on_friday()
    should_stop_ec2_instances_for_08_24_Mon_Fri_tag()
    should_stop_ec2_instances_for_08_24_Mon_Fri_tag_if_still_before_8am()
    should_start_ec2_instances_for_24x5_Mon_Fri_tag_if_after_8am()
    should_stop_ec2_instances_for_08_24_Mon_Fri_tag_if_saturday()
    should_stop_ec2_instances_for_08_24_Mon_Fri_tag_if_sunday()
    should_not_start_ec2_instances_for_24x5_Mon_Fri_tag_if_saturday()
    should_not_start_ec2_instances_for_24x5_Mon_Fri_tag_if_sunday()
    should_stop_ec2_instances_for_08_18_Mon_Sun_tag_if_after_6pm()
    should_start_ec2_instances_for_08_18_Mon_Sun_tag_if_after_8am()
    should_stop_ec2_instances_for_08_18_Mon_Fri_tag_if_after_6pm()
    should_stop_ec2_instances_for_08_18_Mon_Fri_tag_if_after_12am()
    should_start_ec2_instances_for_08_18_Mon_Fri_tag_if_after_8am()
    should_start_ec2_instances_for_08_18_Mon_Fri_tag_if_after_9am()
    should_not_start_ec2_instances_for_8_18_Mon_Fri_tag_if_saturday()
    should_not_start_ec2_instances_for_8_18_Mon_Fri_tag_if_sunday()
    should_stop_ec2_instances_for_18_Shutdown_tag_if_after_6pm()
    should_not_start_ec2_instances_for_18_Shutdown_tag_if_already_stopped()

