import boto3
# Get the service resource.
import key_config as keys
from botocore.config import Config

dynamodb = boto3.resource('dynamodb',
                    aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key=keys.ACCESS_SECRET_KEY)





                    

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')

print(table.creation_date_time)

# table.put_item(
#    Item={
        

#         'name': 'Neha',
#         'pan-number': 'MCLPS8412F',
#         'ph-number': 76767466243,
#         'aadhar-number': '632245155881',
#         'password':'neha100@'
#     }
# )

# Instantiate a table resource object without actually
# creating a DynamoDB table. Note that the attributes of this table
# are lazy-loaded: a request is not made nor are the attribute
# values populated until the attributes
# on the table resource are accessed or its load() method is called.


# Print out some data about the table.
# This will cause a request to be made to DynamoDB and its attribute
# values will be set based on the response.
print(table.creation_date_time)

# Create the DynamoDB table.
# table = dynamodb.create_table(
#     TableName='users',
#     KeySchema=[
#         {
#             'AttributeName': 'email',
#             'KeyType': 'HASH'
#         }
         
#     ],
#     AttributeDefinitions=[
#              {
#             'AttributeName': 'email',
#             'AttributeType': 'S'
#         } 
#     ],
#     ProvisionedThroughput={
#         'ReadCapacityUnits': 5,
#         'WriteCapacityUnits': 5
#     }
# )

# # Wait until the table exists.
# table.meta.client.get_waiter('table_exists').wait(TableName='users')

# # Print out some data about the table.
# print(table.item_count)
