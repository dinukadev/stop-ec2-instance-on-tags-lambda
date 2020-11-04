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
-  Run the `aws configure` and follow the instructions to setup access via the AWS CLI


