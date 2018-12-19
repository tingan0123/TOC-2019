import requests


GRAPH_URL = "https://graph.facebook.com/v2.6"
ACCESS_TOKEN = "EAAbjM4ZBlyt4BAOLwBysEEmykdK9q3XFlvKZBq1BTwoWxwY28S4CEZA2LuYuBgdMggDOMrXUR8eo7OfrhknU9LG6qXXl2VHiUqwoBauprDVMCRdhfGAzWF8tkiKzXv1023wjYOwLE8INoZC6f0ki7CLtIAZCJ66ZBSM6gmojBqY6ZBqZAlhjBdZCQ"


def send_text_message(id, text):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message": {"text": text}
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response



def send_image_url(id, img_url):
    url = "{0}/me/messages?access_token = {1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient" : {"id" : id},
        "message" : {
            "attachment" : {
                "type" : "image",
                "payload" : {
                    "url" : img_url
                }
            }
        }
    }    
    
    response = requests.post(url, json = payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response

def send_button_message(id, text, buttons):
    pass

