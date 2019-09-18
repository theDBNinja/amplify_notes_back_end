# React and AWS Amplify Back End

This application was inspired by the tutorial on https://serverless-stack.com/

The lambda functions from the tutorial have been re-written using Python from Node.js.

The code in this project is only the backend infrastructure of the application. The front end is in the [amplify_notes_front_end](https://github.com/theDbNinja/amplify_notes_front_end) repo.

This backend code will need to be created in order to provide the configuration details in the front end's config.js file.

Create an `S3 bucket` where our Lambda functions will be packaged as ZIP before we deploy anything - If you don't have a S3 bucket to store code artifacts then this is a good time to create one.

```bash
aws s3 mb s3://DEPLOY_BUCKET_NAME
```

Create another S3 bucket for storing the swagger definition file (if you don't already have one).

```bash
aws s3 mb s3://SWAGGER_BUCKET_NAME
```

Upload `notes-default-swagger-api-gateway.yaml` to the S3 bucket.

```bash
aws s3 cp /path/to/file/notes-swagger-api-gateway.yaml S3://SWAGGER_BUCKET_NAME/notes-swagger-api-gateway.yaml
```

Next, run the following command to package our Lambda function to S3:

```bash
sam package \
--template-file /path/to/file/template.yaml \
--output-template-file /path/to/file/packaged.yaml \
--s3-bucket DEPLOY_BUCKET_NAME
```

After packaging and getting the lambda functions ready to go. Replace the `--parameter-overrides` values as necessary, then deploy the template:

```bash
aws cloudformation deploy \
--template-file /path/to/file/packaged.yaml \
--stack-name amplifyNotes \
--capabilities CAPABILITY_NAMED_IAM \
--parameter-overrides \
AmplifyNotesSiteBucketName=PUBLIC_SITE_BUCKET_NAME \
SwaggerBucketName=SWAGGER_BUCKET_NAME \
AmplifyNotesNoteBucketName=BUCKET_TO_STORE_ATTACHMENTS \
ApiHostName=api.myexample.com \
SwaggerFileName=SWAGGER_FILE_NAME \ # Default: notes-swagger-api-gateway.yaml
StageName=default \ # Default: default
NotesTableName=notes  # Default: notes
```

To get the CloudFormation Output values*
```bash
aws cloudformation describe-stacks --stack-name amplifyNotes
```

Additionally the OutputValue for ApiKey is an aws cli command to get the API key. It looks something like:
```bash
aws apigateway get-api-key --include-value --api-key XXXXXXXXXX
```

*Keep these values safe.

### Final steps: 
Create a CloudFront distribution pointing to the Public Site S3 Bucket, creating an SSL cert if needed. Create a record set that points your site to the CloudFront Distribution. Create a custom url in API Gateway for the API host name used, with a base path to the API and stage that was deployed.
