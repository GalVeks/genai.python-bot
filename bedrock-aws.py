from langchain.llms import Bedrock
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import boto3

#BEDROCK_CLIENT = boto3.client(service_name='bedrock',region_name='us-east-1',endpoint_url='https://bedrock.us-east-1.amazonaws.com')

llm = Bedrock(
    credentials_profile_name="default",
    model_id="amazon.titan-tg1-large"
    #client=BEDROCK_CLIENT
)

conversation = ConversationChain(
    llm=llm, verbose=True, memory=ConversationBufferMemory()
)

conversation.predict(input="Hi there!")