import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as ses from 'aws-cdk-lib/aws-ses';
import * as actions from 'aws-cdk-lib/aws-ses-actions';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as sns from 'aws-cdk-lib/aws-sns';
import * as subscriptions from 'aws-cdk-lib/aws-sns-subscriptions';
import * as crypto from 'crypto';

export interface Inbox2ActionProps extends cdk.StackProps {
  envName: string;
  username: string;
  openai: { apiKey: string };
  clickUp: {
    apiKey: string,
    teamId: string,
    spaceId: string
  }
  email: {
    address: string;
    name: string;
    bcc: string;
    receiptRuleSet: string
  },
  log: { level: string }
}

export class Inbox2ActionStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: Inbox2ActionProps) {
    super(scope, id, props);

    const account_id = cdk.Stack.of(this).account
    const hash = crypto.createHash('md5').update(account_id).digest('hex').slice(0, 8);
    
    const dockerLambda = new lambda.DockerImageFunction(this, "DockerLambda", {
      functionName: `inbox2action-${props.envName}-lambda`,
      code: lambda.DockerImageCode.fromImageAsset("./image"),
      memorySize: 1024,
      timeout: cdk.Duration.seconds(60),
      architecture: lambda.Architecture.X86_64,
      loggingFormat: lambda.LoggingFormat.JSON,
      environment: {
        'USERNAME': props.username,
        'OPENAI_API_KEY': props.openai.apiKey,
        'CLICKUP_API_KEY': props.clickUp.apiKey,
        'CLICKUP_TEAM_ID': props.clickUp.teamId,
        'CLICKUP_SPACE_ID': props.clickUp.spaceId,
        'EMAIL_NAME': props.email.name,
        'EMAIL_ADDRESS': props.email.address,
        'EMAIL_ADDRESS_BCC': props.email.bcc,
        'LOG_LEVEL': props.log.level
      }
    });
    
    dockerLambda.addToRolePolicy(new iam.PolicyStatement({
      actions: ['ses:SendEmail', 'ses:SendRawEmail'],
      resources: ['*'],
      conditions: {
        StringEquals: {
          'ses:FromAddress': props.email.address
        }
      }
    }));

    const snsTopic = new sns.Topic(this, 'SnsTopic', {
      topicName: `inbox2action-${props.envName}-sns-topic`,
      displayName: `inbox2action-${props.envName}-sns-topic`
    })

    snsTopic.addSubscription(new subscriptions.LambdaSubscription(dockerLambda));
    
    const bucket = new s3.Bucket(this, 'S3Bucket', {
      bucketName: `inbox2action-${props.envName}-bucket-${hash}`,
      versioned: false,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true
    });
    
    bucket.grantRead(dockerLambda, 'emails/*');
    
    bucket.addToResourcePolicy(new iam.PolicyStatement({
      sid: 'AllowSESPutObject',
      effect: iam.Effect.ALLOW,
      principals: [new iam.ServicePrincipal('ses.amazonaws.com')],
      actions: ['s3:PutObject'],
      resources: [bucket.arnForObjects('*')],
      conditions: {
        StringEquals: { 'aws:Referer': account_id},
      },
    }));

    dockerLambda.addPermission('AllowS3Invoke', {
      principal: new iam.ServicePrincipal('s3.amazonaws.com'),
      sourceArn: bucket.bucketArn,
    });
    
    const ruleSet = ses.ReceiptRuleSet.fromReceiptRuleSetName(
      this,
      'ImportedRuleSet',
      props.email.receiptRuleSet
    );
    
    ruleSet.addRule(`inbox2action-${props.envName}-rule`, {
      receiptRuleName: `inbox2action-${props.envName}-rule`,
      recipients: [props.email.address],
      actions: [
        new actions.S3({
          bucket: bucket,
          objectKeyPrefix: 'emails/',
          topic: snsTopic
        })
      ],
      enabled: true,
      scanEnabled: true,
    });

  }
}