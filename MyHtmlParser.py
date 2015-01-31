import requests
from HTMLParser import HTMLParser
import re
from pprint import pprint as pp

classes = []
course = []
course_regex = re.compile(r'[A-Z]{2,4}\s*[0-9]{4}')
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global course
        # if tag == 'td':
        # 	print attrs
        # 	for attr in attrs: course.append(attr)
    def handle_endtag(self, tag):
        global course
        global classes
        if tag == 'td' and course:
            classes.append(course)
            course = []
    def handle_data(self, data):
        global course
        global course_regex
        if course_regex.match(data):
            if 'or' in data:
                course = [d for d in course_regex.findall(data)]
            else:
                course.append(data)
        else:
            course = []

def get_classes(url):
    request_data = requests.get(url)
    parser = MyHTMLParser()
    parser.feed(request_data.content)
    # pp(classes)
    return classes

