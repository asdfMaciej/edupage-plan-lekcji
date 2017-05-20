import json, sqlite3
from models import *
from pprint import pprint


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

class SqliteExport:
    def __init__(self, fname: str):
        self.con = sqlite3.connect(fname)
        self.cur = self.con.cursor()

    def delete(self):
        self.con.execute('DELETE FROM jednostki_lekcyjne;')
        self.con.commit()

    def close(self):
        self.con.commit()
        self.con.close()

    def export(self, d: dict):
        dict_model = {
            'id': '', 'teacher_id': '', 'teacher': '', 'period': '', 'period_start': '', 'period_end': '',
            'classroom': '', 'subject': '', 'subject_id': '', 'subject_color': '',
            'class': '', 'class_teacher': '', 'd_monday': 0, 'd_tuesday': 0, 'd_thursday': 0, 'd_wednesday': 0,
            'd_friday': 0, 'week_a': 0, 'week_b': 1, 'lesson_id': '', 'group_name': '', 'entire_class': ''
        }

        #cur.execute(
        #    "CREATE TABLE jednostki_lekcyjne ("+', '.join(sorted(list(dict_model.keys())))+");")  # use your column names here
        query = "INSERT INTO jednostki_lekcyjne ("+', '.join(sorted(list(dict_model.keys())))+") VALUES ("+', '.join(['?']*len(list(dict_model.keys())))+");"
        self.cur.executemany(
            query, [tuple(value for (key, value) in sorted(d.items()))])

def open_file(filename: str) -> str:
    with open(filename, 'r') as f:
        t = f.read()
    return t

def search_by_id(search_list: List, id: str, attr = "id") -> object:
    for i in search_list:
        if i.__getattribute__(attr) == id:
            r = i
            break
    else:  # happens after you break out of the for loop
        r = None
    return r

def parse_card(ex_card):
    ex_lesson = search_by_id(lessons, ex_card.lessonid)
    return_list = []
    for x in range(len(ex_lesson.groupids)):
        if not ex_card.days and not ex_card.weeks:
            return []
        dict_model = {
            'id': '', 'teacher_id': '', 'teacher': '', 'period': '', 'period_start': '', 'period_end': '',
            'classroom': '', 'subject': '', 'subject_id': '', 'subject_color': '',
            'class': '', 'class_teacher': '', 'd_monday': 0, 'd_tuesday': 0, 'd_thursday': 0, 'd_wednesday': 0,
            'd_friday': 0, 'week_a': 0, 'week_b': 1, 'lesson_id': '', 'group_name': '', 'entire_class': ''
        }
        if (len(ex_lesson.teacherids)-1 >= x):
            teacher = search_by_id(teachers, ex_lesson.teacherids[x])
        else:
            teacher = search_by_id(teachers, ex_lesson.teacherids[-1])
        if (len(ex_lesson.classids)-1 >= x):
            _class = search_by_id(classes, ex_lesson.classids[x])
        else:
            _class = search_by_id(classes, ex_lesson.classids[-1])
        period = search_by_id(periods, str(ex_card.period))
        classroom = search_by_id(classrooms, str(ex_card.classroomids[0]))
        subject = search_by_id(subjects, ex_lesson.subjectid)
        group = search_by_id(groups, ex_lesson.groupids[x])
        try:
            class_teacher = search_by_id(teachers, _class.teacherid).lastname
        except:
            class_teacher = ""
        _dlist = [
            'd_monday', 'd_tuesday', 'd_thursday', 'd_wednesday', 'd_friday']
        for n in range(len(ex_card.days)):
            dict_model[_dlist[n]] = int(ex_card.days[n])
        dict_model['week_a'] = int(ex_card.weeks[0])
        dict_model['week_b'] = int(ex_card.weeks[1])
        dict_model['teacher'] = teacher.lastname
        dict_model['teacher_id'] = teacher.id
        dict_model['lesson_id'] = ex_lesson.id
        dict_model['id'] = ex_card.id
        dict_model['period'] = period.period
        dict_model['period_start'] = period.starttime
        dict_model['period_end'] = period.endtime
        dict_model['classroom'] = classroom.name
        dict_model['class'] = _class.name
        dict_model['class_teacher'] = class_teacher
        dict_model['group_name'] = group.name
        dict_model['entire_class'] = group.entireclass
        dict_model['subject'] = subject.name
        dict_model['subject_color'] = subject.color
        dict_model['subject_id'] = subject.id
        return_list.append(dict_model)
    return return_list


src = SourceParser(open_file('plan.html'))
jsn = JsonParser(src.json)
periods = jsn.return_periods()
days = jsn.return_days()
weeks = jsn.return_weeks()
terms = jsn.return_terms()
subjects = jsn.return_subjects()
teachers = jsn.return_teachers()
classes = jsn.return_classes()
classrooms = jsn.return_classrooms()
groups = jsn.return_groups()
lessons = jsn.return_lessons()
cards = jsn.return_cards()

f = True
sq = SqliteExport('baza.db')
sq.delete()
for card in cards:
    for x in parse_card(card):
        sq.export(x)
    pprint(parse_card(card))
sq.close()



