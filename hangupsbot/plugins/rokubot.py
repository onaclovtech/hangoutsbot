import logging
import plugins
import requests
from roku import Roku
logger = logging.getLogger(__name__)
def _initialise(bot):
    plugins.register_user_command(["roku"])
    
    #roku = Roku('192.168.0.5')

def roku(bot, event, *args):
    try:
        # https://pypi.python.org/pypi/roku/1.0

        rokuControl = Roku.discover(timeout=10)[0]
        print (rokuControl)
        command = {'up' : rokuControl.up,
                   'down' : rokuControl.down,
                   'left' : rokuControl.left,
                   'right' : rokuControl.right,
                   'select' : rokuControl.select,
                   'home' : rokuControl.home,
                   'back' : rokuControl.back,
                   'play' : rokuControl.play
                   
                   }
        arg = args[0]
        if arg in command:
            command[args[0].lower()]()
        else:
            rokuControl[arg].launch()
        
        html_text = "Successful?"
    except:
        html_text = "Unable to get stocks right now"
        logger.exception(html_text)

    yield from bot.coro_send_message(event.conv_id, html_text)

