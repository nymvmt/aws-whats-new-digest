CATEGORY_RULES = {
    "Database": [
        "RDS", "Aurora", "DynamoDB", "ElastiCache", "Redshift", "DocumentDB",
        "Keyspaces", "Neptune", "QLDB", "Timestream", "MemoryDB"
    ],
    "AI / ML": [
        "SageMaker", "Bedrock", "Polly", "Rekognition", "Comprehend", "Lex",
        "Translate", "Textract", "Forecast", "Personalize", "Kendra", "CodeWhisperer",
        "Augmented AI", "Panorama", "Monitron", "Lookout", "DeepRacer", "Titan"
    ],
    "Security": [
        "Shield", "WAF", "IAM", "Budgets", "Organizations", "GuardDuty",
        "Inspector", "Macie", "Security Hub", "Detective", "CloudTrail",
        "KMS", "Secrets Manager", "Certificate Manager", "Artifact", "Audit Manager"
    ],
    "Compute": [
        "EC2", "Lambda", "ECS", "EKS", "Fargate", "Lightsail", "Batch",
        "Elastic Beanstalk", "Outposts", "Wavelength", "App Runner", "Serverless"
    ],
    "Storage": [
        "S3", "EFS", "EBS", "FSx", "Backup", "Storage Gateway",
        "Snow", "Snowball", "Snowcone", "Snowmobile"
    ],
    "Network": [
        "VPC", "CloudFront", "Route 53", "Direct Connect", "Global Accelerator",
        "Transit Gateway", "PrivateLink", "API Gateway", "Elastic Load Balancing",
        "ELB", "ALB", "NLB"
    ],
    "DevOps": [
        "CodePipeline", "CodeBuild", "CodeDeploy", "CodeCommit", "CodeArtifact",
        "CDK", "CloudFormation", "Systems Manager", "OpsWorks", "X-Ray",
        "CloudWatch", "Config", "Service Catalog"
    ],
    "Data & Analytics": [
        "EMR", "Glue", "Athena", "Lake Formation", "DataZone", "Kinesis",
        "MSK", "OpenSearch", "QuickSight", "Data Exchange", "Clean Rooms"
    ],
    "Messaging": [
        "MQ", "SNS", "SQS", "EventBridge", "AppSync", "Step Functions"
    ],
    "Communication": [
        "Connect", "Pinpoint", "SES", "Chime", "WorkMail"
    ],
    "IoT": [
        "IoT Core", "IoT TwinMaker", "IoT Greengrass", "IoT SiteWise",
        "IoT FleetWise", "IoT RoboRunner"
    ],
    "End User Computing": [
        "WorkSpaces", "AppStream", "WorkLink", "WorkDocs"
    ],
    "Migration": [
        "Migration Hub", "Application Migration", "Database Migration", "DMS",
        "DataSync", "Transfer Family"
    ],
}

def get_category(title: str) -> str:
    title_upper = title.upper()
    for category, keywords in CATEGORY_RULES.items():
        for keyword in keywords:
            if keyword.upper() in title_upper:
                return category
    return "기타"