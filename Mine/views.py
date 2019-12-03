import json

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from Main.models import User_Note
from Main.response import APIResult, APIServerError


@csrf_exempt
def get_notes(request):
    if request.method == "POST":
        try:
            req = json.loads(request.body)
        except:
            return APIServerError("查询失败")
        uid = req["uid"]
        return APIResult(User_Note.get_all_notes(uid))


@csrf_exempt
def get_notes_by_subject(request, subject):
    if request.method == "POST":
        try:
            req = json.loads(request.body)
        except:
            return APIServerError("查询失败")
        uid = req["uid"]
        return APIResult(User_Note.get_notes_by_subject(uid, subject))

@csrf_exempt
def get_subjects(request):
    if request.method == "POST":
        try:
            req = json.loads(request.body)
        except:
            return APIServerError("查询失败")
        uid = req["uid"]
        print(User_Note.get_all_subjects(uid))
        return APIResult(User_Note.get_all_subjects(uid))
