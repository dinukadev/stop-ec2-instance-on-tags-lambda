import os
from datetime import datetime

import boto3
import pytz
import yaml
from moto import mock_ec2

import handler as handler


@mock_ec2
def should_stop_ec2_instances_for_24x5_Mon_Fri_tag():
    os.environ['AVAILABILITY_TAG_VALUES'] = '24x5_Mon-Fri'
    os.environ['CURR_TIME'] = '2020-11-14T00:00:00+11:00'
    # os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")
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
    os.environ['CURR_TIME'] = '2020-11-14T01:00:00+11:00'
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
    os.environ['CURR_TIME'] = '2020-11-15T01:00:00+11:00'
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
    os.environ['CURR_TIME'] = '2020-11-09T01:00:00+11:00'

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
    os.environ['CURR_TIME'] = '2020-11-10T01:00:00+11:00'

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
    os.environ['CURR_TIME'] = '2020-11-11T01:00:00+11:00'

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
    os.environ['CURR_TIME'] = '2020-11-12T01:00:00+11:00'

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
    os.environ['CURR_TIME'] = '2020-11-13T01:00:00+11:00'

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
    os.environ['CURR_TIME'] = '2020-11-16T01:00:00+11:00'

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
    os.environ['CURR_TIME'] = '2020-11-16T01:00:00+11:00'

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
    os.environ['CURR_TIME'] = '2020-11-09T00:00:00+11:00'
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
    os.environ['CURR_TIME'] = '2020-11-09T07:59:00+11:00'
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
    os.environ['CURR_TIME'] = '2020-11-09T08:01:00+11:00'

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
    os.environ['CURR_TIME'] = '2020-11-14T12:00:00+11:00'
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
    os.environ['CURR_TIME'] = '2020-11-15T12:00:00+11:00'
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
    os.environ['CURR_TIME'] = '2020-11-14T12:01:00+11:00'

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
    os.environ['CURR_TIME'] = '2020-11-15T12:01:00+11:00'

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
    os.environ['CURR_TIME'] = '2020-11-09T18:01:00+11:00'
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
    os.environ['CURR_TIME'] = '2020-11-09T08:01:00+11:00'

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
    os.environ['CURR_TIME'] = '2020-11-15T18:00:00+11:00'
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
    os.environ['CURR_TIME'] = '2020-11-15T00:00:00+11:00'
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
    os.environ['CURR_TIME'] = '2020-11-09T08:01:00+11:00'

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
    os.environ['CURR_TIME'] = '2020-11-09T09:00:00+11:00'

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
    os.environ['CURR_TIME'] = '2020-11-14T00:01:00+11:00'

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
    os.environ['CURR_TIME'] = '2020-11-15T12:01:00+11:00'

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
    os.environ['CURR_TIME'] = '2020-11-15T18:00:00+11:00'
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
    os.environ['CURR_TIME'] = '2020-11-15T18:00:00+11:00'

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
