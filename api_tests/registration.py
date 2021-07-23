import requests

base_url = 'http://127.0.0.1:8000/restapi/api/'


class ApiTest:

    def __init__(self):
        self.url = 'http://127.0.0.1:8000/restapi/api/'
        self.username = ''
        self.password = ''

    def retrieve(self):
        """ Retrieve all Lesson objects"""
        request = requests.get(f'{self.url} lessons/')
        print(request)
        #lessons = request.json()

        """available_lessons = ', '.join([lesson['title'] for lesson in lessons])
        print(f'Available courses: {available_lessons}')

        for lesson in lessons:
            id = lesson['id']
            title = lesson['title']

            request = requests.post(f'{self.url} lessons/{id}/register/', auth=(self.username, self.password))

            if request.status_code == 200:
                print('Enrolled in' + title)"""


if __name__:
    test = ApiTest()
    test.retrieve()
