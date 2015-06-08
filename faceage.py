import requests
import json

if __name__ == '__main__':
    keyFile = open('AZUREKEY.txt', 'r')
    PROJECT_OXFORD_KEY = keyFile.readline()
    print PROJECT_OXFORD_KEY

    # https://is.azure-api.net/face/v0/detections[?analyzesAge][&analyzesGender][&analyzesFaceLandmarks][&analyzesHeadPose]&subscription-key=<Your subscription key>
    url = 'https://api.projectoxford.ai/face/v0/detections?analyzesAge=true&analyzesGender=true&subscription-key=' + PROJECT_OXFORD_KEY
    files = {'file': open('toni0.jpg', 'rb')}

    payload = { 'url': 'https://binarymaxsum.github.io/img/tonipenya.png' }
    r = requests.post(url, data=json.dumps(payload))
    print json.loads(r.text)[0]['attributes']


