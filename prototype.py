import json
import re
import urllib.request as urllib2
from collections import defaultdict

from bs4 import BeautifulSoup

base = "https://cesd3.oit.umass.edu/undergradguide/2017-2018/"
info = "Page12331.html"
courseinfo = urllib2.urlopen(base + info).read()

soup = BeautifulSoup(courseinfo, "lxml")

majors = []
for li in soup.find_all('li'):
    c = li.get('class')
    if c is not None:
        if c[0] == "catalognavigationmenu-chapter":
            majors.append((li.a.contents[0], li.a.get('href')))

ml = []
for m, u in majors:
    major = urllib2.urlopen(base + u).read()
    ml.append((m, BeautifulSoup(major, "lxml")))

courses = []
for m, s in ml:
    for li in s.find_all('li'):
        if li.get('class') is not None:
            if li.get('class')[0] == "catalognavigationmenu-topicgroup":
                if li.a.contents[0] == "The Courses":
                    courses.append((m, li.a.get('href')))
mc = []
for m, u in courses:
    courses = urllib2.urlopen(base + u).read()
    mc.append((m, BeautifulSoup(courses, "lxml")))

classes = defaultdict(lambda: [])
for m, s in mc:
    temp = []
    for strong in s.find_all('strong'):
        n = re.findall(r'((^|\s)[0-9][0-9][0-9]\s)|([0-9][0-9][0-9][A-Z|a-z]+(\s|$))|([0-9][0-9][0-9][A-Z|a-z]+[0-9])',
                       strong.text)
        for c in n:
            for j in c:
                if j != '\n' and j != '':
                    temp.append(j.rstrip('\n').rstrip(' ').rstrip('\xa0'))
    for t in temp:
        if len(t) > 1:
            classes[m].append(t.strip())

r = json.dumps(classes)
js = json.loads(r)
with open('fetched.json', 'w') as outfile:
    json.dump(js, outfile)
