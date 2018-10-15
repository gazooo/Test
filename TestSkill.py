import json


def lambda_handler(event, context):
    if event["request"]["type"] == "LaunchRequest":
        print("test")
        return on_launch(event, context)

    if event["request"]["type"] == "IntentRequest":
        return intent_router(event, context)

    return {
        "statusCode": 200,
        "body": json.dumps('Hello from Lambda!')
    }


def on_launch(event, context):
    return statement("Greetings", "Welcome to the math quiz", False)


def intent_router(event, context):
    intent = event["request"]["intent"]["name"]
    if intent == "StartNewGameIntent":
        return startNewGame(event, context)

    # required Intents
    if intent == "AMAZON.CancelIntent":
        return cancel_intent()
    if intent == "AMAZON.HelpIntent":
        return help_intent()
    if intent == "AMAZON.StopIntent":
        return stop_intent()
    if intent == "AMAZON.FallbackIntent":
        return fallback_intent()


def startNewGame(event, context):
    return statement("New Game", "Okay, we start a new round. Get ready.", False)


def cancel_intent():
    return statement("CancelIntent", "You want to cancel", False)


def help_intent():
    return statement("HelplIntent", "You want help", False)


def stop_intent():
    return statement("StopIntent", "You want to stop", True)


def fallback_intent():
    return statement("FallbackIntent", "You want to fall back", True)


def statement(title, body, endit):
    speechlet = {}
    speechlet["outputSpeech"] = build_PlainSpeech(body)
    speechlet["card"] = build_SimpleCard(title, body)
    speechlet["shouldEndSession"] = endit
    return build_response(speechlet)


def build_PlainSpeech(body):
    speech = {}
    speech["type"] = "PlainText"
    speech["text"] = body
    return speech


def build_SimpleCard(title, body):
    card = {}
    card["type"] = "Simple"
    card["title"] = title
    card["content"] = body
    return card


def build_response(message, session_attributes={}):
    response = {}
    response["version"] = "1.0"
    response["sessionAttributes"] = session_attributes
    response["response"] = message
    return response