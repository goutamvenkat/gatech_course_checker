import requests
from datetime import date
import re
from pprint import pprint as pp
from bs4 import BeautifulSoup
from collections import defaultdict

class OscarParser(object):
	def __init__(self, semester, year=date.today().year):
		self.semester = semester
		self.year = year

	def findterm(self):
	    termdict = dict(fall='08', spring='01', summer='05')
	    return str(self.year) + termdict.get(self.semester.lower())

	def run(self):
		term = self.findterm()
		url = 'https://oscar.gatech.edu/pls/bprod/bwckschd.p_get_crse_unsec?term_in=' + term +'&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj=CS&sel_crse=&sel_title=&sel_schd=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&sel_ptrm=%25&sel_instr=%25&sel_attr=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a'
		req = requests.get(url)
		content = req.text
		soup = BeautifulSoup(repr(content), 'lxml')
		courses = []
		instructors = []
		Map = defaultdict(list)
		for link in soup.find_all('a'):
			url = link.get('href')
			if url is not None and len(url.split('?')) > 1:
				url = url.split('?')
				config = url[1].split('&')
				configDict = {}
				for keyValue in config:
					keyValue = keyValue.split('=')
					configDict[keyValue[0]] = keyValue[1]
				if configDict.get('one_subj') is not None and configDict.get('sel_crse_strt') is not None:
					courses.append(configDict.get('one_subj') + configDict.get('sel_crse_strt'))
			elif link.get('target') and link['target'] != '_blank':
				instructors.append(link['target'])
		# return {course: instructor for (course, instructor) in zip(courses, instructors)}
		for course, instructor in zip(courses, instructors):
			if Map.get(course) == [] or instructor not in set(Map[course]):
				splitStr = re.split('[\s.]', instructor)
				if len(splitStr) > 2:
					temp = splitStr[len(splitStr) - 1].upper() + splitStr[0].upper()
					for i in xrange(1, len(splitStr) - 1):
						temp += splitStr[i]
					Map[course].append(temp)
				else:
					newStr = ''.join([splitStr[i].upper() for i in xrange(len(splitStr) - 1, -1, -1)])
					Map[course].append(newStr)

		return dict(Map)

if __name__ == '__main__':
	pp(OscarParser('fall').run())