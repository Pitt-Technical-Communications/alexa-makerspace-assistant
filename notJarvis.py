import json

def lambda_handler(event, context):
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

def on_launch(launch_request, session):
    return get_welcome_response()
    
def get_welcome_response():
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Hello Artful Maker! I am here to help you find things. Please say, Alexa find me the insert item here, for help finding a material." 
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with the same text.
    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def on_session_ended(session_ended_request, session):
    #Called when the user ends the session. Is not called when the skill returns should_end_session=true
    print("on_session_ended requestId=" + session_ended_request['requestId'] +", sessionId=" + session['sessionId'])

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """
    print("on_intent requestId=" + intent_request['requestId'] +", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    #this is a TEMPORARY set up, I'll make it more efficient once we're sure this works
    if intent_name == "findItem":
        return findItemResponse()
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")
        
def get_help_response():
    session_attributes = {}
    card_title = "Help"
    speech_output = "Please say, Alexa find me insert item here, for help finding a material"
    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session))

def findItemResponse():
    session_attributes = {}
    card_title = "Locator"
    speech_output=""
    specificItem=intent_request["intent"]["slots"]["item"]["value"]
    
    if specificItem=="fabric":
        speech_output="the fabic is on the second protocart on whatever shelf."
    elif specificItem=="dowel rods":
        speech_output="Dowel rods are on the wall to the left of the wood station"
    else:
        speech_output="Sorry, I don't have a location for that item. Please ask a TA or Dr. Samosky."
    reprompt_text=speech_output
    should_end_session=True
    return build_response(session_attributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session))
        
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }