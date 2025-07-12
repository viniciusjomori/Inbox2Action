import * as cdk from 'aws-cdk-lib'
import { Inbox2ActionStack } from '../lib/inbox2action-stack'
import * as fs from 'fs';
import * as path from 'path';

const app = new cdk.App();

let envName = app.node.tryGetContext('env')
const config = getConfig(envName)

new Inbox2ActionStack(app, `Inbox2Action[${envName.toUpperCase()}]`, {
  stackName: `inbox2action-${envName}-stack`,
  envName: envName,
  ...config
});

function getConfig(envName: string) {
  const configPath = path.resolve(__dirname, `../env/${envName}.json`);
  
  if (!fs.existsSync(configPath)) throw new Error(`env not found: ${configPath}`);

  const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
  return config
}