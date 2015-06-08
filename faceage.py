import requests
import json

if __name__ == '__main__':
    keyFile = open('AZUREKEY.txt', 'r')
    PROJECT_OXFORD_KEY = keyFile.readline()

    # https://is.azure-api.net/face/v0/detections[?analyzesAge][&analyzesGender][&analyzesFaceLandmarks][&analyzesHeadPose]&subscription-key=<Your subscription key>
    url = 'https://api.projectoxford.ai/face/v0/detections?analyzesAge=true&analyzesGender=true&subscription-key=' + PROJECT_OXFORD_KEY

    data = open('./people.jpg', 'rb').read()

    print 'Processing image...'
    response = requests.post(url, data=data, headers={'Content-Type': 'application/octet-stream'})

    result = json.loads(response.text)

    print 'Found:'
    for face in result:
        print 'A ' + str(face['attributes']['age']) + ' years old ' + face['attributes']['gender'] + '.'