#!/bin/bash
cd /root/lekcje/

phpsessid=$(curl --silent --output /dev/null -c - https://zs1wronki.edupage.org/timetable/ | grep PHPSESSID | awk '{print $NF}')
gsh=$(curl --silent -H "Cookie: PHPSESSID=$phpsessid" https://zs1wronki.edupage.org/timetable/ | grep gsechash= | cut -d \" -f2)
echo "$phpsessid"
echo "$gsh"
curl --request POST \
-d "{\"__args\":[null,\"38\"],\"__gsh\":\"$gsh\"}" \
-H 'Content-Type: application/json; charset=UTF-8' \
-H "Cookie: PHPSESSID=$phpsessid" \
https://zs1wronki.edupage.org/timetable/server/regulartt.js?__func=regularttGetData > plan.json

# curl "https://zs1wronki.edupage.org/timetable/" > plan.html

python3 main.py
cp baza.db /var/www/html/plan/
