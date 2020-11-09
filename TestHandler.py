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
    datetime_object = datetime_object.astimezone(local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")
    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop(None, None)

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
    datetime_object = datetime_object.astimezone(local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")
    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop(None, None)

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
    datetime_object = datetime_object.astimezone(local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")

    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']
    client.stop_instances(InstanceIds=[instance_id])

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop(None, None)

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
    datetime_object = datetime_object.astimezone(local_tz)
    os.environ['CURR_TIME'] = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")

    region = 'ap-southeast-2'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']
    client.stop_instances(InstanceIds=[instance_id])

    tags = list(map(lambda x: create_tag_obj(x), os.environ['AVAILABILITY_TAG_VALUES'].split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop(None, None)

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
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
    should_start_ec2_instances_for_24x5_Mon_Fri_tag()
    should_start_ec2_instances_for_24x5_Mon_Fri_tag_if_date_passed()
    should_stop_ec2_instances_for_24x5_Mon_Fri_tag_if_date_has_passed()

