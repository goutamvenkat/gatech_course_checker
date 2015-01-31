import requests
from datetime import date
import MyHtmlParser
import re

class CourseoffParser(object):
    def __init__(self, classes, semester, year=date.today().year):
        self.classes = classes
        self.semester = semester
        self.year = year
    def parse(self):
        critique_urls = []
        for course in self.classes:
            for eachCourse in course:
                major, number = eachCourse.split()
                data = requests.get('https://soc.courseoff.com/gatech/terms/{}/majors/{}/courses/{}/sections'.format(self.findterm(), major, number))
                data = data.json()
                if data:
                    instructor_set = set()
                    for section in data:
                        instructor = section.get('instructor')
                        if instructor:
                            lname = instructor.get('lname').upper()
                            fname = instructor.get('fname').upper()
                            name = ''.join(re.split('[\s.]', (lname + ' ' + fname)))
                            if name not in instructor_set:
                                critique_url = 'http://critique.gatech.edu/prof.php?id={}'.format(name)
                                instructor_set.add(name)
		                        critique_urls.append(critique_url)
        return critique_urls

    def findterm(self):
        termdict = dict(fall='08', spring='01', summer='05')
        return str(self.year) + termdict.get(self.semester.lower())

url = 'http://catalog.gatech.edu/colleges/coc/ugrad/comsci/threads/degreq/info-internet-intel2.php'
parser = CourseoffParser(MyHtmlParser.get_classes(url), 'spring')
parser.parse()