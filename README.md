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
      # runs every 40 minutes
      prod: cron(0/40 * * * ? *)
      # runs every 1 minute(for dev purposes)
      dev: cron(0/1 * ? * * *)
      # runs every 1 minute(for dev purposes)
      test: cron(0/1 * ? * * *)
```

As this lambda is being invoked on a scheduled basis, we have configured the cron jobs for each environment. For example, on development and test, to make things move faster,
the cron job executes every minute. 

On the production profile however, we can set it to a daily run if need be to save on lambda execution costs. Right now it is set to run every 40 minutes.

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
docker build --force-rm=true -t ec2-stop-lambda:latest .
```

And then to run the tests, run the following command;
```
docker run -it ec2-stop-lambda:latest
```

