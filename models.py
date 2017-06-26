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
    def __init__(self, subjectid: str, teacherids: List, groupids: List, classids: List, count: str,
            classroomids: Dict, id: str, durationperiods: str):
        self.subjectid = subjectid
        self.teacherids = teacherids
        self.groupids = groupids
        self.classids = classids
        self.count = count
        self.classroomids = classroomids
        self.durationperiods = durationperiods
        self.id = id

    def __str__(self):
        return self.id + " - lesson"

class Card:
    def __init__(self, lessonid: str, period: int, days: str, weeks: str, classroomids: List, id: str):
        self.lessonid = lessonid
        self.period = period
        self.days = days
        self.weeks = weeks
        self.classroomids = classroomids
        self.id = id

    def __str__(self):
        return self.id + " - Period " + str(self.period) + ", days " + self.days