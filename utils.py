import requests


GRAPH_URL = "https://graph.facebook.com/v2.6"
ACCESS_TOKEN = "EAAEwfCH38u0BAKZBQ8TkdZAS6AsuFvynZAMwVLqk15sxgtfGZBCBUi5QmkFEf51a0ry1xzBtZCpyBl29sfOWTFMuqN3YZCfXTVUHzoFGvLaNCabdGmS6csldPRNZA3ZA0wPyoRKhez91buqLW1apubqmA0bzhhgUgX5o6SNZBdfNZBupjuD6p0dGja"


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
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    #"is_reusable": true,
                    "url": img_url
                }
            }
        }
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response


def send_button_message(id, text, buttons):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message":{
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":text,
                    "buttons":[
                    {
                        "type":"web_url",
                        "url":"https://www.messenger.com/",
                        "title":"更多資訊",
                        "webview_height_ratio": "full"
                    }
                    ]
                }
            }
        }
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response

