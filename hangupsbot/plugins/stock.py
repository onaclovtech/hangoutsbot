import logging
import plugins
import requests

logger = logging.getLogger(__name__)

def _initialise(bot):
    plugins.register_user_command(["stock"])

def stock(bot, event, *args):
    try:
        r = requests.get("http://www.google.com/finance/info?q=NSE:" + args[0].upper())

        symbol = args[0].upper()
        price = r.text.split('\n')[6].split(':')[1].strip(' ').strip('\"')
        change_dollar = r.text.split('\n')[13].split(':')[1].strip(' ').strip('\"')
        change_percent = r.text.split('\n')[15].split(':')[1].strip(' ').strip('\"')

        html_text = '%s: $%s / %s (%s%%)' % (symbol, price, change_dollar, change_percent)
    except:
        html_text = "Unable to get stocks right now"
        logger.exception(html_text)

    yield from bot.coro_send_message(event.conv_id, html_text)

