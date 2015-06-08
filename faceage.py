import requests
import json
import sys

def getFaces(headers, data):
    keyFile = open('AZUREKEY.txt', 'r')
    AZURE_KEY = keyFile.readline()
    # https://is.azure-api.net/face/v0/detections[?analyzesAge][&analyzesGender][&analyzesFaceLandmarks][&analyzesHeadPose]&subscription-key=<Your subscription key>
    url = 'https://api.projectoxford.ai/face/v0/detections?analyzesAge=true&analyzesGender=true&subscription-key=' + AZURE_KEY
    response = requests.post(url, data=data, headers=headers)
    return json.loads(response.text)


def getFacesFromUrl(url):
    data = json.dumps({'url': url})
    headers = {'Content-Type': 'application/json'}
    return getFaces(headers, data)


def getFacesFromFile(path):
    data = open(path, 'rb').read()
    headers = {'Content-Type': 'application/octet-stream'}
    return getFaces(headers, data)


if __name__ == '__main__':
    USAGE = ("faceage.py <resource>\n"
             "  If the resource starts with 'http' it will treat it as an internet URL. "
             "Otherwise, it will look for a file in the local file system.\n"
             "\n"
             "EXAMPLES:\n"
             "  faceage.py ./people.jpg\n"
             "  faceage.py https://binarymaxsum.github.io/img/tonipenya.png")

    print 'Processing image...'

    if len(sys.argv) == 2:
        resource = sys.argv[1]
        if resource[0:4] == 'http':
            faces = getFacesFromUrl(resource)
        else:
            try:
                faces = getFacesFromFile(resource)
            except IOError:
                print 'Could not process the file:', resource
                exit(-1)
    else:
        print USAGE
        exit()

    print 'Found:'
    for face in faces:
        print 'A ' + str(face['attributes']['age']) + ' years old ' + face['attributes']['gender'] + '.'
