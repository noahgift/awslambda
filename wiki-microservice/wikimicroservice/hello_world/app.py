import json
import boto3
import wikipedia

print("Loading function")


def lambda_handler(event, context):
    """Wikipedia Summarizer"""

    if "body" in event:
        event = json.loads(event["body"])
    entity = event["entity"]
    res = wikipedia.summary(entity, sentences=1)
    comprehend = boto3.client("comprehend")
    key_phrase = comprehend.detect_key_phrases(Text=res, LanguageCode='en')
    nlp_res = key_phrase['KeyPhrases'][1]['Text']
    print(f"context: {context}, event: {event}")
    print(f"Response from wikipedia API: {nlp_res}")
    response = {
        "statusCode": "200",
        "headers": {"Content-type": "application/json"},
        "body": json.dumps({"message": nlp_res}),
    }
    return response
