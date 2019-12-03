import json
import requests
import redis
import uuid

from django.views.decorators.http import require_GET

from Main.models import Note, Recommend, User
from Main.response import APIResult, APIServerError
from SharingNotes.local_settings import APP_ID, SECRET, POOL


@require_GET
def get_hottest(request):
    notes = Note.get_hottest_note()
    conn = redis.Redis(connection_pool=POOL)
    conn.delete(40)
    for note in notes:
        id = note['id']
        conn.set(name=id, value=Note.objects.get(id=id).to_string())
    return APIResult(notes)


@require_GET
def get_recommend(request):
    return APIResult(Recommend.get_recommends())


@require_GET
def get_user_info(request):
    js_code = request.GET["code"]
    info = eval(request.GET["userInfo"])
    nickName = info['nickName']
    # avatarUrl = info['avatarUrl']
    response = requests.get("https://api.weixin.qq.com/sns/jscode2session?"
                            "appid={APPID}&secret={SECRET}&js_code={JSCODE}"
                            "&grant_type=authorization_code"
                            .format(APPID=APP_ID, SECRET=SECRET,
                                    JSCODE=js_code), verify=False)
    response = json.loads(response.text)
    print(response)
    try:
        user = User.objects.get_or_create(openId=response['openid'],
                                          user_bh=uuid.uuid3(uuid.NAMESPACE_DNS, response['openid']),
                                          nickName=nickName)[0]
        print(user.user_bh)
        return APIResult({"uid": user.user_bh})
    except KeyError:
        return APIServerError(response["errmsg"])
