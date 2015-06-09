import requests
import json
import sys
import os


class BadResponseException(Exception):
    def __init__ (self, value):
        self.value = value

    def __str__(self):
        return self.value


def get_faces(headers, data):
    keyFile = open('AZUREKEY.txt', 'r')
    AZURE_KEY = keyFile.readline()
    # [?analyzesAge][&analyzesGender][&analyzesFaceLandmarks][&analyzesHeadPose]&subscription-key=<Your subscription key>
    url = 'https://api.projectoxford.ai/face/v0/detections?analyzesAge=true&analyzesGender=true&subscription-key=' + AZURE_KEY
    response = requests.post(url, data=data, headers=headers)
    if response.status_code != 200:
        raise BadResponseException(json.loads(response.content)['message'])
    return json.loads(response.text)


def get_faces_from_url(url):
    data = json.dumps({'url': url})
    headers = {'Content-Type': 'application/json'}
    return get_faces(headers, data)


class FileTooBigException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


def get_faces_from_file(path):
    if os.path.getsize(path) > 2*1024*1024:
        raise FileTooBigException('File must be under 2MB')

    data = open(path, 'rb').read()
    headers = {'Content-Type': 'application/octet-stream'}
    return get_faces(headers, data)


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
            try:
                faces = get_faces_from_url(resource)
            except BadResponseException as e:
                print 'Error contacting the server'
                print e
                exit(-1)
        else:
            try:
                faces = get_faces_from_file(resource)
            except IOError:
                print 'Could not process the file:', resource
                exit(-1)
            except FileTooBigException as e:
                print e.value
                exit(-1)
    else:
        print USAGE
        exit()

    print 'Found:'
    for face in faces:
        print 'A ' + str(face['attributes']['age']) + ' years old ' + face['attributes']['gender'] + '.'
