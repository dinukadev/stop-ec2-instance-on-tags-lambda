import os

import boto3


def ec2_stop(event, context):
    print('Starting the ec2 stop lambda functionality')
    ec2_client = boto3.client('ec2')
    # Get list of regions
    regions = [region['RegionName']
               for region in ec2_client.describe_regions()['Regions']]
    tags = os.environ['TAGS']
    tags_filter_arr = list(map(lambda x: create_filter_obj(x), tags.split(",")))

    # Iterate over each region
    for region in regions:
        ec2 = boto3.resource('ec2', region_name=region)
        print("Region:", region)
        # Get only running instances
        instances = ec2.instances.filter(
            Filters=tags_filter_arr)
        # Stop the instances
        for instance in instances:
            instance.stop()
            print('Stopped instance: ', instance.id)
    print('Successfully executed the ec2 stop lambda functionality')


def create_filter_obj(tag):
    tag_split = tag.split("=")
    tag_key = tag_split[0]
    tag_value = tag_split[1]
    return {'Name': 'tag:{}'.format(tag_key),
            'Values': [tag_value]}


if __name__ == '__main__':
    ec2_stop(None, None)
