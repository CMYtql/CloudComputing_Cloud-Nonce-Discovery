# -*- coding: utf-8 -*-
import time
from fabric.api import run, env, put, parallel, serial, execute,get
import boto3

env.user = 'ubuntu'
env.key_filename = '~/.ssh/ec2_comsm0010.pem'

@serial
def initialVMs(N):
    # use boto3 to define connections
    ec2 = boto3.client('ec2',region_name='us-east-1')
    # create and start instances
    ec2.run_instances(ImageId='ami-04b9e92b5572fa0d1',InstanceType='t2.micro',
                      KeyName='ec2_comsm0010',SecurityGroups=['launch-wizard-2'],
                      MinCount=int(N), MaxCount=int(N))
    # wait for seconds until all instances are running successfully
    time.sleep(100)
    
    currentHost = []
    # use filters to get IP addresses of all exsiting running instances
    filters = [{'Name': 'instance-state-name', 'Values': ['running']}]
    Reservations = ec2.describe_instances(Filters=filters)
    
    # add their IP addresses to the list for following tasks
    for rv in Reservations['Reservations']:
        for instance in rv['Instances']:
            currentHost.append(instance['PublicIpAddress'])
    return currentHost

@parallel
def allocateVMs(D,N,T,thisHost):
    #use fabric to put the script to each VM by super user(sudo) without authentication issues
    put('goldennonce_cw.py', 'goldennonce_cw.py',use_sudo=True)
    #run the script on each VM by looping the IPs
    for index in range(int(N)):
        if env.host == thisHost[index]:
            #get the printing console result of the run
            ls=run('python3 goldennonce_cw.py %d %d %d %d'%(int(D),int(N),int(T),int(index)))
            #get logs
            getLogs(index)
            #check that if there is an VM has found a golden nonce
            #if true, terminating all VMs ang getting the logs
            if ls.startswith('Golden nonce'):
                execute(terminateVMs)
        
def terminateVMs():
    ec2 = boto3.client('ec2',region_name='us-east-1')
    filters = [{'Name': 'instance-state-name', 'Values': ['running']}]
    Reservations = ec2.describe_instances(Filters=filters)
    # terminate all existing running instances automatically by looping their instanceid
    for rv in Reservations['Reservations']:
        for instance in rv['Instances']:
            i = instance['InstanceId']
            ec2.terminate_instances(InstanceIds=[i])   
            
def getLogs(index):
    s3 = boto3.resource('s3')
    BUCKET = 'ccwarehouse'
    # getting logs of all instacnes and download to local folder
    get('/var/log/syslog','%d.log'%index)
    # upload log files to S3 bucket
    s3.Bucket(BUCKET).upload_file('%d.log'%index, 'logs/%d.log'%index)
    
# organising the tasks in my own way
def task(D,N,T):
    # firstly get the list of IP addressed of all instances launched by the initialVMs()
    currentHost=initialVMs(int(N))
    # execute allocateVMs() based on the instances whose IP addresses are in the list currentHost
    execute(allocateVMs,D,N,T,currentHost,hosts=currentHost)
#    execute(terminateVMs)