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
	sem = ''
	sem += year
	if semester.lower() == 'fall':
	    sem += '08'
	elif semester.lower() == 'spring':
	    sem += '01'
	else:
	    sem += '05'
	return sem

def courseoff_parser(courses, semester, year, color):
    sem = get_semester(semester, year)
    classes_in_sem = []
    for course in courses:
        if len(course) < 2:
            course = course[0]
        else:
            course = course[1]
        major, course_num = course.split()
        course_num = int(course_num)
        sem = get_semester(semester, year)
    	url = 'https://soc.courseoff.com/gatech/terms/{}/majors/{}/courses/{}/sections'.format(sem, major, course_num)
        data = requests.get(url)
        data = data.json()
        if data:
            for section in data:
                instructor = section.get('instructor')
                if instructor:
                    lname = instructor.get('lname').upper()
                    fname = instructor.get('fname').upper()
                    name  = name = ''.join((fname + lname).split())
                    critique_url = 'http://critique.gatech.edu/prof.php?id={}#{}'.format(name, major.upper()+str(course))
                    critique = requests.get(critique_url)
                    print critique.content

        	
	                   
pp(php_parser('e'))
