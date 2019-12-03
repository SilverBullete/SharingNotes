import json
import logging
import redis

from json import JSONDecodeError
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET

from Main.models import User, Follower, Note, Star, Collection, Subject, User_Note
from Main.response import APIResult, APIServerError
from SharingNotes.local_settings import POOL

log = logging.getLogger('app')
true = True


@require_GET
def get_notes_by_subject(request, subject):
    return APIResult(Note.get_notes_by_subject(subject))


@require_POST
def create_note(request):
    try:
        req = json.loads(request.body)
    except JSONDecodeError as e:
        return JsonResponse(e)
    uid = req.get('uid')
    subject_id = req.get('subject_id')
    if subject_id == 0:
        subject = create_subject(req.get('subject_name'))
    else:
        subject = Subject.objects.get(id=subject_id)
    title = req.get('title')
    content = req.get('content')
    note = Note.objects.create(title=title, content=content, subject=subject)
    User_Note.objects.create(user=uid, note=Note.objects.get(id=note.id))
    return APIResult({}, "创建成功")


@require_POST
def update_note(request):
    try:
        req = json.loads(request.body)
    except JSONDecodeError as e:
        return JsonResponse(e)
    note_id = req.get('note_id')
    uid = req.get('uid')
    subject_id = req.get('subject_id')
    title = req.get('title')
    content = req.get('content')
    conn = redis.Redis(connection_pool=POOL)
    if is_owner(uid, note_id):
        if subject_id == 0:
            subject = create_subject(req.get("subject_name"))
        else:
            subject = Subject.objects.get(id=subject_id)
        note = Note.objects.get(id=note_id)
        note.content = content
        note.subject = subject
        note.title = title
        note.save()
        if conn.exists(note_id):
            conn.set(name=note_id, value=note.to_string())
        return APIResult({}, "更新成功")
    return APIServerError("更新失败")


def create_subject(subject_name):
    subject, _ = Subject.objects.get_or_create(name=subject_name)
    return subject


@require_POST
def get_note_by_id(request):
    try:
        req = json.loads(request.body)
    except JSONDecodeError as e:
        return JsonResponse(e)
    uid = req.get("uid")
    note_id = req.get("note_id")
    conn = redis.Redis(connection_pool=POOL)
    if not is_owner(uid, note_id):
        note = Note.objects.filter(id=note_id).first()
        note.read_times += 1
        note.save()
        conn.set(name=note_id, value=note.to_string())
    if conn.exists(note_id):
        note = eval(conn.get(note_id).decode('utf-8'))
    else:
        note = Note.get_note_by_id(note_id)
    return APIResult({
        "is_owner": is_owner(uid, note_id),
        "has_stared": has_stared(uid, note_id),
        "note": note
    })


def is_owner(user_id, note_id):
    note = User_Note.objects.filter(user=user_id, note_id=note_id)
    if len(note) == 0:
        return False
    return True


def has_stared(user_id, note_id):
    star = Star.objects.filter(user_id=user_id, note_id=note_id)
    if len(star) == 0:
        return False
    return True


@require_POST
def star(request):
    try:
        req = json.loads(request.body)
    except JSONDecodeError as e:
        return JsonResponse(e)
    user_id = req['uid']
    note_id = req['note_id']
    try:
        s, has = Star.objects.get_or_create(user_id=user_id, note_id=note_id)
        if has:
            note = Note.objects.get(id=note_id)
            note.star_times += 1
            note.save()
        else:
            Star.objects.filter(user_id=user_id, note_id=note_id).delete()
            note = Note.objects.get(id=note_id)
            note.star_times -= 1
            note.save()
        return APIResult({}, "点赞成功")
    except:
        return APIServerError("点赞失败")


def collect(request):
    req = json.load(request.body)
    user_id = req['user_bh']
    note_id = req['note_id']
    if user_id != '' or note_id != '':
        return json.dumps({})
    else:
        try:
            Collection.objects.create(user_id=user_id, note_id=note_id)
        except:
            pass


def follow(request):
    req = json.load(request.body)
    follower = req['follower']
    followed = req['followed']
    if follower != '' or followed != '':
        return json.dumps({})
    else:
        try:
            Follower.objects.create(followed=followed, follower=follower)
        except:
            pass
