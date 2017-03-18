import logging
import plugins
import requests
import urllib.request, urllib.parse, base64, os, aiohttp, io
from time import sleep
logger = logging.getLogger(__name__)

def _initialise(bot):
    plugins.register_user_command(["snap"])
    
   
def snap(bot, event, *args):
    # Source http://krqe.com/traffic/albuqerque-traffic-cams/
    cams = {
            'i40@unser'          : "http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-40@Unser",
            'i40@paseodelvolcan' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-40W@PaseoDelVolcan',
            'i40@98th'           : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-40@98thSt',
            'coors@atrisco'      : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=Coors@Atrisco',
            'coors@nofi40'       : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=Coors@NofI-40',
            'coors@i40'          : "http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=Coors@I-40SGore",
            'i40@riogranderiver' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-40@RioGrandeRiver',
            'i40@riogrande'      : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-40@RioGrande',
            'i40@12th'           : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-40@12thSt',
            'i40@4th'            : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-40@4thSt',
            'i40eb/i25'          : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-40EB/I-25Gore',
            'i40wb/i25'          : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-40WestToI-25',
            'i40@university'     : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-40@University',
            'i40@carlisle'       : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-40@Carlisle',
            'i40@sanmateo' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-40@SanMateo',
            'i40@washington' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-40@Washington',
            'i40@12th' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-40@12thSt',
            'i40@eubank' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-40@Eubank',
            'i40eb@juantabo' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-40EB@JuanTabo',
            'i40wb@juantabo' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-40WB@JuanTabo',
            'i40@tramway' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-40@Tramway',
            'i25@riobravo' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-25@RioBravo',
            'i25@sunport' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-25@Sunport',
            'i25@gibson' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-25@Gibson',
            'i25@cesarchavez' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-25@CesarChavez',
            'i25@mlk' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-25@MLK',
            'i25@coal' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-25@Coal',
            'i25@lead' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-25@Lead',
            'i25nb/Gore' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-25NB/Gore',
            'i25@Lomas' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-25@Lomas',
            'i25@Mongomery' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-25@Mongomery',
            'i25@SofBigI' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-25@SofBigI',
            'i25@SanAntonio' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-25@SanAntonio',
            'i25@Jefferson' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-25@Jefferson',
            'i25NB@Tramway' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-25NB@Tramway',
            'i25@SanMateo' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-25@SanMateo',
            'i25NB@US-550' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-25NB@US-550',
            '550@i25' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=US550@I-25',
            'i25@bernalillo' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-25@Bernalillo',
            'pdn@coors' : "http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=PaseoDelNorteAtCoors",
            'pdn@riogrande' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=PDN@RioGrande',
            'pdn@4th' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=PaseoDelNorteAt4th',
            'jefferson@pdn' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=Jefferson@PDN',
            'i25@pdn' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=I-25@PaseoDelNorte',
            '84-285@502' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=US84-285@NM502',
            '550@528' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=US550@SR528',
            '550@313' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=US550@NM313',
            'tramway@lomas' : 'http://servicev3.nmroads.com/RealMapWAR/GetCameraImage?cameraName=Tramway@Lomas'}

            
    try:
        if args[0].lower() in ['help']:
           html_text = "Here are available options: "
           for k in cams.keys():
              html_text += k + ','
           html_text = html_text[:-1]
           yield from bot.coro_send_message(event.conv_id, html_text)
           return
           
        if args[0].lower() in cams.keys():
            request = urllib.request.Request(cams[args[0].lower()])
            result = urllib.request.urlopen(request)
            with open('test.jpg','wb') as output:
               output.write(result.read())
            with open('test.jpg', "rb") as f:
               image_data = io.BytesIO(f.read())
            image_id = yield from bot._client.upload_image(image_data, filename='test.jpg')
            yield from bot.coro_send_message(event.conv_id, None, image_id=image_id)
            return
    except:
        html_text = "Unable to access the camera right now"
        logger.exception(html_text)

        yield from bot.coro_send_message(event.conv_id, html_text)

#@asyncio.coroutine
#def mkgif(bot, event):
#    with open('test.jpg', "rb") as f:
#        image_data = io.BytesIO(f.read())
#    image_id = yield from bot._client.upload_image(image_data, filename='test.jpg')
#    yield from bot.coro_send_message(event.conv_id, None, image_id=image_id)
    
#def getImg():
#   request = urllib.request.Request("http://192.168.0.29/image.jpg?cidx=307805807")
#   base64string = base64.b64encode(b"admin:").decode("ascii")
#   request.add_header("Authorization", "Basic %s" % base64string)
#   result = urllib.request.urlopen(request)
