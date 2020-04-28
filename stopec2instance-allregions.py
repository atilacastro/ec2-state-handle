import boto3
import logging

#Autor: Átila Castro
#setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#define the connection
ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
    # Use the filter() method of the instances collection to retrieve
    # all running EC2 instances.
    filters = [{
            'Name': 'tag:turn-off',
            'Values': ['true']
        },
        {
            'Name': 'instance-state-name', 
            'Values': ['running']
        }
    ]
    
    #locate all regions
    client = boto3.client('ec2')
    ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    
    for region in ec2_regions:
        
        ec2 = boto3.resource('ec2',region_name=region)
        
        #filter the instances
        instances = ec2.instances.filter(Filters=filters)
    
        #locate all running instances
        RunningInstances = [instance.id for instance in instances]
        
        #print the instances for logging purposes
        #print RunningInstances 
        
        #make sure there are actually instances to stop. 
        for i in RunningInstances:
            #perform the stopup
            shuttingDown = ec2.instances.filter(InstanceIds=RunningInstances).stop()
            print (shuttingDown)