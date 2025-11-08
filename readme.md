Features:
Show items in the house.

Swagger ui: https://nno3q5ecp6.execute-api.us-west-2.amazonaws.com/Stage/api/swagger

Running locally:
1. Install dependencies
pip install -r requirements.txt
2. Run the application
> python run main.py

3. Run lambda function locally
Run handler /lambda_api/sessions.py
In working directory of Pycharm config, set to /badminton_recharging (not badminton_recharging/lambda_api)


Problem:
1. Create python layer:
pip install -r .\requirement_aws_standard.txt -t layer/python_standard
Note: libs must be compatible with linux os, aws layer requires folder /python in zip file. Use following command to install dependencies for aws lambda layer:
pip install --platform manylinux2014_x86_64 --target=layer/python_standard/python --implementation cp --python-version 3.11 --only-binary=:all: --upgrade -r .\requirement_aws_standard.txt

2. CORS error for aws lambda application

Enable CORS in API Gateway, using AWS Console or AWS cloudformation template:
Example:
  ApiBadmintonRechargingDeployment:
    Type: AWS::Serverless::Api
    Properties:
      StageName: dev
      Cors:
        AllowMethods: "'OPTIONS,POST,GET,PUT,DELETE'"
        AllowHeaders: "'Content-Type,X-Amz-Date,Authorization,X-Api-Key'"
        AllowOrigin: "'*'"

3. EFS
- IAM User Group: FileSystemFullAccess, VPCFullAccess
- Create VPC, Subnet, Security Group (VPC, Subnet create by AWS console)
- Create EFS, mount target, AccessPoint (AWS Cloudformation template)
- Create lambda function in VPC

4. Unit test
- pip install pytest pytest-mock pytest-cov
- > pytest
- > pytest --cov=api_logic --cov-report=html
  
5. Init DB locally
- Set source as Root folder of project
- Run efs_lambda with task_type='init_db'


6. U2net
- link repo: git clone https://github.com/xuebinqin/U-2-Net.git
- link model: https://huggingface.co/FireCRT/VideoStudio/blob/main/u2net.pth