
from config.lib import *


def get_maxpages_pdf(base64_pdf):
    try:
        countpages = 0
        message = "nonnoti"
        base64_bytes = base64_pdf.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        images = convert_from_bytes(message_bytes)
        for i, image in enumerate(images):
            countpages = countpages + 1
        # if countpages >= 20:
        #     message = "noti"
        if countpages >= 21 and countpages <= 50:
            message = "noti2trans"
        elif countpages >= 51:
            message = "notiadmin"
        return [200,countpages,message]
    except Exception as e:
        return [400,str(e)]