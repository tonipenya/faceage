import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json

if __name__ == '__main__':
    keyFile = open('AZUREKEY.txt', 'r')
    PROJECT_OXFORD_KEY = keyFile.readline()
    print PROJECT_OXFORD_KEY

    # https://is.azure-api.net/face/v0/detections[?analyzesAge][&analyzesGender][&analyzesFaceLandmarks][&analyzesHeadPose]&subscription-key=<Your subscription key>
    url = 'https://api.projectoxford.ai/face/v0/detections?analyzesAge=true&analyzesGender=true&subscription-key=' + PROJECT_OXFORD_KEY


    # files = {'file': open('people.jpg', 'rb')}
    data = open('./people.jpg', 'rb').read()

    # payload = { 'url': 'https://binarymaxsum.github.io/img/tonipenya.png' }
    # r = requests.post(url, data=json.dumps(payload))
    r = requests.post(url, data=data, headers={'Content-Type': 'application/octet-stream'})
    print r
    print json.loads(r.text)[0]['attributes']


