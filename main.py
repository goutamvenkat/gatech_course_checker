import requests
from HTMLParser import HTMLParser
from pprint import pprint as pp
import re

classes = []
course = []
course_regex = re.compile(r'\s*[A-Z]{3,4}\s*[0-9]{4}\s*')
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global course
        if tag == 'li':
	        for attr in attrs:
	            course.append(attr)
    def handle_endtag(self, tag):
    	global course
    	global classes
    	if tag == 'li' and course:
    		classes.append(course)
    		course = []
    def handle_data(self, data):
    	global course
    	global course_regex
        if course_regex.match(data):
        	course.append(data)
        else:
        	course = []


parser = MyHTMLParser()

def php_parser(core, color='WHITE'):
	catalog_url = 'http://www.catalog.gatech.edu/students/ugrad/core/core{}.php'.format(core)
	courses = requests.get(catalog_url)
	courses = courses.content
	parser.feed(courses)
	global classes
	c = classes 
    courseoff_info = courseoff_parser(c, 'Spring', '2015', color)

def get_semester(semester, year):
    sem += year
    if semester.lowercase() == 'fall':
        sem += '08'
    elif semester.lowercase() == 'spring':
        sem += '01'
    else:
        sem += '05'
    return sem

def courseoff_parser(courses, semester, year, color):
    sem = get_semester(semester, year)
    classes_in_sem = []
    majors_and_courses = dict()
    for course in courses:
        if len(course) < 2:
            course = course[0]
        else:
            course = course[1]
        major, course_num = course.split()
        course_num = int(course_num)
        if majors_and_courses.get(major):
            majors_and_courses[major].add(course_num)
        else:
            majors_and_courses[major] = set(course_num)

    for major in majors_and_courses.keys():    
        url = 'https://soc.courseoff.com/gatech/terms/{}/majors/{}/courses'.format(sem, major)
        data = requests.get(url)
        data = data.json()
        



#pp(php_parser('e'))
