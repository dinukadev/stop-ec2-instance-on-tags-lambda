# Introduction

This project contains a lambda that lets you stop AWS EC-2 instances running on any region of your account based on configurable tags.

# Pre-requisites
This lambda created using the serverless framework. We need a few things setup before we can deploy this lambda.
- [Install Node](https://nodejs.org/en/download/)
- Run the following to install the serverless framework

```
npm install -g serverless
```
- To verify that the serverless framwork was installed correctly, run the following
```
serverless --version
```

- [Install the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- Create an AWS user who has full admin access with programmatic access and obtain the access key ID and the secret access key 
- Run the `aws configure` and follow the instructions to setup access via the AWS CLI

# Configuration and Profiles
This lambda is broken down into three main profiles;
 - dev
 - test
 - prod

You can see this within the serverless.yml;
```
custom:
  env:
    cron:
       prod: rate(15 minutes)
       dev: rate(15 minutes)
       test: rate(15 minutes)
```

The valid tag values are also configured as properties within the same yaml file as follows;
```
environment:
    AVAILABILITY_TAG_VALUES: 24x5_Mon-Fri,08-24_Mon-Fri,08-18_Mon-Sun,08-18_Mon-Fri,18_Shutdown,24x7_Mon-Sun,Maintenance
```

The email configuration is broken down based on profiles so you can switch it as needed with differnt emails if need be;

```
    EMAIL_ALERTS_FLAG: true
    REGION: ${self:provider.region}
    EMAIL_FROM: ${self:custom.env.email.${self:custom.stage}.EMAIL_FROM}
    EMAIL_TO: ${self:custom.env.email.${self:custom.stage}.EMAIL_TO}
    EMAIL_SUBJECT: AWS Availability Scheduler Report - Development Environment
    EMAIL_CHARSET: UTF-8

  env:
    email:
      prod:
        EMAIL_FROM: dl-aws-ops-master@metricon.com.au
        EMAIL_TO: dl-aws-ops-master@metricon.com.au
      test:
        EMAIL_FROM: dl-aws-ops-master@metricon.com.au
        EMAIL_TO: dl-aws-ops-master@metricon.com.au
      dev:
        EMAIL_FROM: dl-aws-ops-master@metricon.com.au
        EMAIL_TO: dl-aws-ops-master@metricon.com.au
```

You can turn off all email configuration by setting the value to `false` on the following property;
```
EMAIL_ALERTS_FLAG: false
```

# Deployment
Once the pre-requisites mentioned above are completed, you can deploy the lambda by invoking the following command;

```
sls deploy --stage prod --region ap-southeast-2
```

If you do not specify the `--region`, the default specified in the serverless.yml will be used.
If you do not specify the `--stage`, the default of `dev` will be injected.

For more best practices on deploying with the serverless framework, do check [this link](https://www.serverless.com/framework/docs/providers/aws/guide/deploying/).

# Tear down
On the test and development environments, you would want to clean up the lambda once testing is done in order to save on cost of executing the lambda.

As the serverless framework deploys the lambda using CloudFormation, cleaning up all your resources is quite easy. All you have to do is to execute the following command.

```
sls remove
```

# Running tests
Integration tests are done using the [moto](https://github.com/spulec/moto) library which runs a virtual AWS environment so you can test the code similar to an actual AWS environment.

A Dockerfile is provided so that you do not need to install all the required libraries on your local environment to run  tests.

Make sure you have docker installed and then run the following command to build the docker image;

```
docker build --force-rm=true -t ec2-stop-start-lambda:latest .
```

And then to run the tests, run the following command;
```
docker run -it ec2-stop-start-lambda:latest
```

