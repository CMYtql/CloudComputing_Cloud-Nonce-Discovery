# Cloud-Nonce-Discovery
 comsm0010_CW

## Introduction

Users are able to specify difficulty-level D and N number of virtual machines to do CND task on AWS within the maximum runtime T.

In detail, CND automatically start up N VMs(Virtual Machines) in the cloud, distribute the brute-force search for a golden nonce over the N VMs, and then when one of the VMs does find the golden nonce, CND should cleanly close down all VMs and report the nonce value back to the user. It also returns log files that show what happened in the run up until the shutdown and upload them to Amazon S3 bucket.

## Installation and Configuration

To run the scripts you need to:

1. Install Python3

2. Install pip3

3. Install awscli through pip3

4. Install Boto3

5. Install Fabric3

6. AWS Configure:
```

[default]

region = your_aws_region_here

aws_access_key_id=your_aws_access_id_here

aws_secret_access_key=your_aws_access_key_here

aws_session_token=your_aws_access_token_here

```

6. Create a key pair named 'ec2_comsm0010.pem', download it and move it to ~\.ssh file. 


7. Create a security group named 'launch-wizard-2'.


8. Create a S3 bucket named 'ccwarehouse'.


## How to run the script

1. Enter to the Fabric folder:

cd ...

2. Use Fabric run command:

e.g. fab -f CNDtask.py task: D=3,N=6,T=2000
