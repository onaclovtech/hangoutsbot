import logging
import plugins
import requests

logger = logging.getLogger(__name__)

def _initialise(bot):
    plugins.register_user_command(["stock"])

def stock(bot, event, *args):
    try:
        r = requests.get("http://www.google.com/finance/info?q=NSE:" + args[0].upper())
        html_text = '$' + r.text.split('\n')[6].split(':')[1].strip(' ').strip('\"')
    except:
        html_text = "Unable to get stocks right now"
        logger.exception(html_text)

    yield from bot.coro_send_message(event.conv_id, html_text)
