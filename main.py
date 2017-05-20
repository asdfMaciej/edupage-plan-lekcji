import json
from typing import Dict, List


class Period:
    def __init__(self, period: int, name: str, short: str, starttime: str, endtime: str, id: str):
        self.period = period
        self.name = name
        self.short = short
        self.starttime = starttime
        self.endtime = endtime
        self.id = id

    def __str__(self):
        return str(self.period)+" -> "+self.starttime+" - "+self.endtime

class Day:
    def __init__(self, name: str, short: str, vals: List, val: int, id: str):
        self.name = name
        self.short = short
        self.vals = vals
        self.val = val
        self.id = id

    def __str__(self):
        return self.name+" ("+self.short+") - "+self.id

class Week:
    def __init__(self, name: str, short: str, vals: List, val: int, id: str):
        self.name = name
        self.short = short
        self.vals = vals
        self.val = val
        self.id = id

    def __str__(self):
        return self.name + " (" + self.short + ") - " + self.id

class Term:
    def __init__(self, name: str, short: str, vals: List, val: int, id: str):
        self.name = name
        self.short = short
        self.vals = vals
        self.val = val
        self.id = id

    def __str__(self):
        return self.name + " (" + self.short + ") - " + self.id

class Subject:
    def __init__(self, name: str, short: str, color: str, id: str):
        self.name = name
        self.short = short
        self.color = color
        self.id = id

    def __str__(self):
        return self.id + " - " + self.name + " (" + self.short + ")"

class Teacher:
    def __init__(self, lastname: str, short: str, color: str, id: str):
        self.lastname = lastname
        self.short = short
        self.color = color
        self.id = id

    def __str__(self):
        return self.id + " - " + self.lastname

class Class:
    def __init__(self, name: str, teacherid: str, id: str):
        self.name = name
        self.teacherid = teacherid
        self.id = id

    def __str__(self):
        return self.id + " - " + self.name + " ("+self.teacherid+")"

class Classroom:
    def __init__(self, name: str, id: str):
        self.name = name
        self.id = id

    def __str__(self):
        return self.id + " - " + self.name

class Group:
    def __init__(self, name: str, entireclass: str, classid: str, id: str):
        self.name = name
        self.entireclass = entireclass
        self.classid = classid
        self.id = id

    def __str__(self):
        return self.id + " - " + self.classid + " - " + self.name

class Lesson:
    def __init__(self, subjectid: str, teacherids: Dict, groupids: Dict, classids: Dict, count: str,
            classroomids: Dict, id: str):
        self.subjectid = subjectid
        self.teacherids = teacherids
        self.groupids = groupids
        self.classids = classids
        self.count = count
        self.classroomids = classroomids
        self.id = id

    def __str__(self):
        return self.id + " - lesson"

class Card:
    def __init__(self, lessonid: str, period: int, days: str, weeks: str, classroomids: Dict, id: str):
        self.lessonid = lessonid
        self.period = period
        self.days = days
        self.weeks = weeks
        self.classroomids = classroomids
        self.id = id

    def __str__(self):
        return self.id + " - Period " + str(self.period) + ", days " + self.days

class JsonParser:
    """
    I made a mistake - this code could be reduced by 90%
    The model objects should be provided the rows and parse them on init
    Therefore, you could do one template function and just reference to it with other names
    like return_generic(self, n, object) and provide object as in Card or Period or whatever
    """
    def __init__(self, json: Dict):
        self.json = json

    def _int(self, val) -> int:
        return int(val) if val else None

    def return_periods(self) -> List:
        periods = []
        rows = self.json['changes'][4]['rows']
        for row in rows:
            periods.append(Period(
                row["period"], row["name"], row["short"], row["starttime"], row["endtime"], row["id"]
            ))
        return periods

    def return_days(self) -> List:
        days = []
        rows = self.json['changes'][3]['rows']
        for row in rows:
            days.append(Day(
                row["name"], row["short"], row["vals"], row["val"], row["id"]
            ))
        return days

    def return_weeks(self) -> List:
        weeks = []
        rows = self.json['changes'][2]['rows']
        for row in rows:
            weeks.append(Week(
                row["name"], row["short"], row["vals"], self._int(row["val"]), row["id"]
            ))
        return weeks

    def return_terms(self) -> List:
        terms = []
        rows = self.json['changes'][1]['rows']
        for row in rows:
            terms.append(Term(
                row["name"], row["short"], row["vals"], self._int(row["val"]), row["id"]
            ))
        return terms

    def return_subjects(self) -> List:
        subjects = []
        rows = self.json['changes'][6]['rows']
        for row in rows:
            subjects.append(Subject(
                row["name"], row["short"], row["color"], row["id"]
            ))
        return subjects

    def return_teachers(self) -> List:
        teachers = []
        rows = self.json['changes'][7]['rows']
        for row in rows:
            teachers.append(Teacher(
                row["lastname"], row["short"], row["color"], row["id"]
            ))
        return teachers

    def return_classes(self) -> List:
        classes = []
        rows = self.json['changes'][8]['rows']
        for row in rows:
            classes.append(Class(
                row["name"], row["teacherid"], row["id"]
            ))
        return classes

    def return_classrooms(self) -> List:
        classrooms = []
        rows = self.json['changes'][9]['rows']
        for row in rows:
            classrooms.append(Classroom(
                row["name"], row["id"]
            ))
        return classrooms

    def return_groups(self) -> List:
        groups = []
        rows = self.json['changes'][10]['rows']
        for row in rows:
            groups.append(Group(
                row["name"], row["entireclass"], row["classid"], row["id"]
            ))
        return groups

    def return_lessons(self) -> List:
        lessons = []
        rows = self.json['changes'][11]['rows']
        for row in rows:
            lessons.append(Lesson(
                row["subjectid"], row["teacherids"], row["groupids"], row["classids"], row["count"],
                row["classroomidss"], row["id"]
            ))
        return lessons

    def return_cards(self) -> List:
        cards = []
        rows = self.json['changes'][12]['rows']
        for row in rows:
            cards.append(Card(
                row["lessonid"], row["period"], row["days"], row["weeks"], row["classroomids"], row["id"]
            ))
        return cards

class SourceParser:
    def __init__(self, html: str):
        self.html = self.extract_html(html)
        self.json = self.extract_json(self.html)

    def extract_html(self, html:str) -> str:
        return html.split('.app.Sync(')[1].split(');')[0]
    def extract_json(self, html:str) -> Dict:
        return json.loads(html)


def open_file(filename: str) -> str:
    with open(filename, 'r') as f:
        t = f.read()
    return t

src = SourceParser(open_file('plan.html'))
jsn = JsonParser(src.json)
combinated = jsn.return_periods()
combinated += jsn.return_days()
combinated += jsn.return_weeks()
combinated += jsn.return_terms()
combinated += jsn.return_subjects()
combinated += jsn.return_teachers()
combinated += jsn.return_classes()
combinated += jsn.return_classrooms()
combinated += jsn.return_groups()
combinated += jsn.return_lessons()
combinated += jsn.return_cards()
for p in combinated:
    print(p)

