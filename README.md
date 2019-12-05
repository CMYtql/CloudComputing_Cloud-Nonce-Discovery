# CloudComputing_Cloud-Nonce-Discovery
comsm0010_CW

To run the script:

e.g. fab -f CNDtask.py task: D=3,N=6,T=2000


Users are able to specify difficulty-level D and N number of virtual machines to do CND task on AWS within the maximum runtime T.

In detail, CND automatically start up N VMs(Virtual Machines) in the cloud, distribute the brute-force search for a golden nonce over the N VMs, and then when one of the VMs does find the golden nonce, CND should cleanly close down all VMs and report the nonce value back to the user. It also returns log files that show what happened in the run up until the shutdown and upload them to Amazon S3 bucket.



To run the scripts you need to:

1. Install Python3, Pip3, Boto3, Fabric3


2. Configure AWS:

The user's AWS access and secret keys:

[default]

region = your_aws_region_here

aws_access_key_id=your_aws_access_id_here

aws_secret_access_key=your_aws_access_key_here

aws_session_token=your_aws_access_token_here


3. Create a key pair named 'ec2_comsm0010.pem', download it and move it to ~\.ssh file. 

   Create a security group named 'launch-wizard-2' and a S3 bucket named 'ccwarehouse'.
