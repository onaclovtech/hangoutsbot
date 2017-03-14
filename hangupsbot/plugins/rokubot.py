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
        admins_list = bot.get_config_suboption(event.conv_id, 'admins') or []
        if event.user_id.chat_id in admins_list:
            ip = bot.user_memory_get(event.user.id_.chat_id, 'roku')
            if ip is None:
                rokuControl = Roku.discover(timeout=10)[0]
                bot.user_memory_set(event.user.id_.chat_id, 'roku', rokuControl.host)
                ip = rokuControl.host
            
            rokuControl = Roku(ip)
            
            
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
            return
        else:
            html_text = "You can't control my roku, you so crazy"
    except:
        html_text = "Unable to control the roku right now"
        logger.exception(html_text)

    yield from bot.coro_send_message(event.conv_id, html_text)

