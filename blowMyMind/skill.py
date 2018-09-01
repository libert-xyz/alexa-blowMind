import logging
import os
import random
from flask import Flask, render_template
from flask_ask import Ask, request, session, question, statement
from facts import blow

app = Flask(__name__)
ask = Ask(app, "/")

log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

logo = 'https://s3.amazonaws.com/itron-skill/visuals/BrainWithFusePNG-300x184.png'


@ask.launch
def launch():
    #Return a list
    #LIST
    session.attributes['facts'] = blow

    random_quote = random.randint(0,len(session.attributes['facts'])-1)
    fact = render_template('quote',q=session.attributes['facts'][random_quote])
    fact_tts = render_template('quote_tts',q=session.attributes['facts'][random_quote])

    #Remove the item
    session.attributes['facts'].remove(session.attributes['facts'][random_quote])


    #Repeat
    session.attributes['repeat']  = fact
    session.attributes['repeat_tts'] = fact_tts

    return question(fact) \
    .standard_card(title='Blow my mind',
    text=fact_tts,
    small_image_url=logo)


@ask.intent('YesIntent')
def yes_intent():
    #Return a list

    if len(session.attributes['facts']) == 0:
        #Restart Quesions
        session.attributes['facts'] = blow

    lenght = len(session.attributes['facts']) - 1

    random_quote = random.randint(0,lenght)
    fact = render_template('quote',q=session.attributes['facts'][random_quote])
    fact_tts = render_template('quote_tts',q=session.attributes['facts'][random_quote])
    #Remove the item
    session.attributes['facts'].remove(session.attributes['facts'][random_quote])

    #Repeat
    session.attributes['repeat']  = fact
    session.attributes['repeat_tts'] = fact_tts

    return question(fact) \
    .standard_card(title='Blow my mind',
    text=fact_tts,
    small_image_url=logo)

@ask.intent('NoIntent')
def no_intent():
    return statement('Ok. have a great day') \
        .standard_card(title='Blow my mind',
        text="Ok. have a great day",
        small_image_url=logo)


@ask.intent('StopIntent')
def stop_intent():
    return statement('')

@ask.intent('AMAZON.RepeatIntent')
def repeat():

    return question(session.attributes.get('repeat')) \
            .standard_card(title='Blow my mind',
            text=session.attributes.get('repeat_tts'),
            small_image_url=logo)


@ask.intent('HelpIntent')
def help_intent():

    help_t = render_template('help')
    return question(help_t) \
        .standard_card(title='Blow my mind',
        text=help_t,
        small_image_url=logo)


if __name__ == '__main__':
    app.run(debug=True)
