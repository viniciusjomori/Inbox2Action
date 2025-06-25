import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import * as lambda from "aws-cdk-lib/aws-lambda";

export interface Inbox2ActionProps extends cdk.StackProps {
  envName: string;
  username: string;
  openai: { apiKey: string };
  aws: {
    bucketName: string;
  }
  clickUp: {
    apiKey: string,
    teamId: string,
    spaceId: string
  }
  email: {
    address: string;
    name: string;
    bcc: string
  }
}

export class Inbox2ActionStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: Inbox2ActionProps) {
    super(scope, id, props);

    const dockerFunc = new lambda.DockerImageFunction(this, "DockerFunc", {
      functionName: `inbox2action-lambda-${props.envName}`,
      code: lambda.DockerImageCode.fromImageAsset("./image"),
      memorySize: 1024,
      timeout: cdk.Duration.seconds(60),
      architecture: lambda.Architecture.X86_64,
      environment: {
        'USERNAME': props.username,
        'OPENAI_API_KEY': props.openai.apiKey,
        'AWS_BUCKET_NAME': props.aws.bucketName,
        'CLICKUP_API_KEY': props.clickUp.apiKey,
        'CLICKUP_TEAM_ID': props.clickUp.teamId,
        'CLICKUP_SPACE_ID': props.clickUp.spaceId,
        'EMAIL_NAME': props.email.name,
        'EMAIL_ADDRESS': props.email.address,
        'EMAIL_ADDRESS_BCC': props.email.bcc,
      }
    });
  }
}