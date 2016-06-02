import logging
import plugins
import requests
import json

logger = logging.getLogger(__name__)

def _initialise(bot):
    plugins.register_user_command(["wiki"])

def wiki(bot, event, *args):
    try:
    
        #r = requests.get("https://en.wikipedia.org/wiki/" + args[0])
        r = requests.get("https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles=" + args[0])
        x = json.loads(r.text)
#        r: {"batchcomplete":"","query":{"normalized":[{"from":"pedagogy","to":"Pedagogy"}],"pages":{"419686":{"pageid":419686,"ns":0,"title":"Pedagogy","extract":"Pedagogy (etymology and pronunciation) is the discipline that deals with the theory and practice of education; it thus concerns the study and practice of how best to teach. Its aims range from the general (full development of the human being via liberal education) to the narrower specifics of vocational education (the imparting and acquisition of specific skills).\nFor example, Paulo Freire referred to his method of teaching people as \"critical pedagogy\". In correlation with those instructive strategies, the instructor's own philosophical beliefs of instruction are harbored and governed by the pupil's background knowledge and experience, situation, and environment, as well as learning goals set by the student and teacher. One example would be the Socratic schools of thought. The teaching of adults, however, may be referred to as andragogy."}}}}
        #
        print ("r: " + str(x['query']['pages'][x['query']['pages'].keys()[0]]))
        html_text = "https://en.wikipedia.org/wiki/" + args[0]
#        html_text = '%s: $%s / %s (%s%%)' % (symbol, price, change_dollar, change_percent)
    except:
        html_text = "Unable to get definition right now"
        logger.exception(html_text)

    yield from bot.coro_send_message(event.conv_id, html_text)
