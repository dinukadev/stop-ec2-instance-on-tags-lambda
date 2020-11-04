import os

import boto3
import yaml
from moto import mock_ec2

import handler as handler


@mock_ec2
def test_ec2_stop():
    # handler.ec2_stop(None,None)
    serverless_yaml = readYaml()
    tags_from_serverless_yaml = serverless_yaml['provider']['environment']['TAGS']
    os.environ['TAGS'] = tags_from_serverless_yaml
    region = 'us-west-1'
    client = boto3.client('ec2', region_name=region)
    reservation = client.run_instances(ImageId='ami-1234abcd', MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']

    tags = list(map(lambda x: create_tag_obj(x), tags_from_serverless_yaml.split(",")))

    client.create_tags(Resources=[instance_id], Tags=tags)

    handler.ec2_stop(None, None)

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
    instance_id_list = list(map(lambda x: x.id, instances))
    filtered_instance_ids = list(filter(lambda x: x == instance_id, instance_id_list))
    assert instance_id in filtered_instance_ids


def create_tag_obj(tag):
    tag_split = tag.split("=")
    tag_key = tag_split[0]
    tag_value = tag_split[1]
    return {'Key': tag_key,
            'Value': tag_value}


def readYaml():
    with open("serverless.yml", "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exec:
            print(exec)
            sys.exit(1)


if __name__ == '__main__':
    test_ec2_stop()
