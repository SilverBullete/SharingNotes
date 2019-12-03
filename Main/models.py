import uuid
import json

from datetime import datetime

from django.db import models

user_id = uuid.uuid3(uuid.NAMESPACE_DNS, 'python.org')
true = True


class User(models.Model):
    GENDER = {
        ("1", "男"),
        ("2", "女")
    }
    openId = models.CharField(default='', max_length=200, verbose_name="用户微信唯一ID", unique=True)
    avatarUrl = models.URLField(default='', max_length=500, verbose_name='用户微信头像')
    country = models.CharField(default='', max_length=100, verbose_name='用户微信国家')
    user_bh = models.CharField(default=user_id, max_length=50, unique=True, verbose_name='用户唯一ID')
    province = models.CharField(default='', max_length=100, verbose_name='用户微信城市')
    city = models.CharField(default='', max_length=100, verbose_name='用户微信区域')
    language = models.CharField(default='', max_length=100, verbose_name='用户微信语言')
    # background = models.ImageField(default='/default/default.jpg',
    #                                upload_to='UserProFilebg/%Y/%m/{imagess}'.format(imagess=user_id),
    #                                null=True, blank=True, verbose_name='背景图')
    nickName = models.CharField(max_length=20, verbose_name="微信用户名")
    name = models.CharField(max_length=20, verbose_name="用户名")
    birthday = models.DateField(default=datetime.now, verbose_name="出生日期")
    # avatar = models.ImageField(null=True, blank=True)
    # upload_to='UserProFilebg/avatar/%y/%d/{image_file}'.format(image_file=user_id),
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机号")
    gender = models.CharField(max_length=10, choices=GENDER, default="1", verbose_name="性别")
    thesignature = models.TextField(default='', max_length=200, verbose_name='用户签名')
    agreement = models.BooleanField(default=False, verbose_name='是否阅读协议')
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="注册时间")

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "id: %s name %s" % (self.user_bh, self.nickName)


class Follower(models.Model):
    follower_id = models.AutoField
    followed = models.CharField(default="", max_length=200, verbose_name="被关注者")
    follower = models.CharField(default="", max_length=200, verbose_name="关注者")
    follow_time = models.DateTimeField(default=datetime.now, verbose_name="关注时间")

    class Meta:
        verbose_name = '关注'
        verbose_name_plural = verbose_name


class Subject(models.Model):
    name = models.CharField(default="", max_length=100, verbose_name="类别名称", unique=True)
    count = models.IntegerField(verbose_name="该类别笔记数量", default=0)
    is_internal = models.BooleanField(verbose_name="是否为内置", default=False)


class Note(models.Model):
    title = models.CharField(default="", max_length=100, verbose_name="标题")
    content = models.TextField(default="")
    is_secret = models.IntegerField(default=0, verbose_name="是否开放")
    summary = models.CharField(max_length=200, default="", verbose_name="摘要")
    read_times = models.IntegerField(verbose_name="阅读数", default=0)
    star_times = models.IntegerField(verbose_name="点赞数", default=0)
    collect_times = models.IntegerField(verbose_name="收藏数", default=0)
    hot = models.IntegerField(verbose_name="热度", default=0)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="类别")
    create_time = models.DateTimeField(default=datetime.now, verbose_name="创建时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="更新时间")

    class Meta:
        verbose_name = '笔记'
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Note, self).save()
        self.hot = self.read_times * 5 + self.star_times * 15 + self.collect_times * 30
        super(Note, self).save()

    def __unicode__(self):
        return "id: %s name %s" % (self.id, self.title)

    def to_string(self):
        dic = {
            "id": self.id,
            "title": self.title,
            "author": User.objects.get(user_bh=User_Note.objects.get(note=self.id).user).nickName,
            "content": eval(self.content),
            "hot": self.hot,
            "time": self.update_time.strftime("%Y-%m-%d"),
            "subject": self.subject.name
        }
        return json.dumps(dic)

    @staticmethod
    def get_hottest_note():
        notes = Note.objects.all().order_by('-hot')[:5]
        data = [{
            "id": note.id,
            "title": note.title,
            "author": User.objects.get(user_bh=User_Note.objects.get(note__id=note.id).user).nickName,
            "hot": note.hot
        } for note in notes]
        return data

    @staticmethod
    def get_notes_by_subject(subject):
        if subject == -1:
            notes = Note.objects.select_related("subject__id").all()
        else:
            notes = Note.objects.filter(subject__id=subject)
        if len(notes) == 0:
            return {}
        data = [{
            "id": note.id,
            "title": note.title,
            "subject": note.subject.name,
            "hot": note.hot,
            "summary": note.summary,
            "update_time": note.update_time.strftime("%Y-%m-%d")
        } for note in notes]
        data.sort(key=lambda d: d['hot'], reverse=True)
        return {data}

    @staticmethod
    def get_note_by_id(note_id):
        if not note_id:
            return {
                "result": False,
                "code": 404,
                "data": {},
                "message": "请先传入id"
            }
        note = Note.objects.filter(id=note_id)
        if len(note) == 0:
            return {
                "result": False,
                "code": 404,
                "data": {},
                "message": "请传入正确的id"
            }
        note = note.first()
        data = {
            "id": note.id,
            "title": note.title,
            "subject": note.subject.name,
            "content": eval(note.content),
            "time": note.update_time.strftime("%Y-%m-%d")
        }
        return data

    def get_note_text(self):
        print(eval(self.content))
        print(eval(self.content).keys())
        return eval(self.content)['text']


class User_Note(models.Model):
    id = models.AutoField
    user = models.CharField(default="", max_length=200, verbose_name="微信ID")
    note = models.ForeignKey(Note, verbose_name="笔记id", on_delete=models.CASCADE)

    @staticmethod
    def get_all_notes(uid):
        notes = User_Note.objects.filter(user=uid)
        if len(notes) == 0:
            return {
                "message": "您还没有创建过笔记，现在开始创建一个吧！"
            }
        dic = {}
        for note in notes:
            if not note.note.subject.name in dic:
                dic[note.note.subject.name] = 1
            else:
                dic[note.note.subject.name] += 1
        data = []
        for key in dic.keys():
            data.append({"subject": key, "count": dic[key], "subject_id": Subject.objects.get(name=key).id})
        return {"subjects": data}

    @staticmethod
    def get_notes_by_subject(uid, subject):
        notes = User_Note.objects.select_related("note__subject").filter(
            user=uid, note__subject__id=subject)
        if len(notes) == 0:
            return {}
        data = []
        for n in notes:
            note = Note.objects.get(id=n.note_id)
            data.append({
                "id": note.id,
                "title": note.title
            })
        return {
            "subject": Subject.objects.get(id=subject).name,
            "notes": data
        }

    @staticmethod
    def get_all_subjects(uid):
        notes = User_Note.objects.filter(user=uid)
        data = []
        for note in notes:
            subject = Note.objects.get(id=note.note_id).subject
            js = {
                "id": subject.id,
                "name": subject.name
            }
            if js not in data:
                data.append(js)
        subjects = Subject.objects.filter(is_internal=True)
        for subject in subjects:
            if subject.name not in data:
                js = {
                    "id": subject.id,
                    "name": subject.name
                }
                if js not in data:
                    data.append(js)
        return data


class Star(models.Model):
    id = models.AutoField
    user_id = models.CharField(default="", max_length=50, verbose_name="微信ID")
    note = models.ForeignKey(Note, verbose_name="笔记id", on_delete=models.CASCADE)
    star_time = models.DateTimeField(default=datetime.now, verbose_name="点赞时间")

    class Meta:
        verbose_name = '点赞'
        verbose_name_plural = verbose_name


class Collection(models.Model):
    id = models.AutoField
    user_id = models.CharField(default="", max_length=50, verbose_name="微信ID")
    note = models.ForeignKey(Note, verbose_name="笔记id", on_delete=models.CASCADE)
    collect_time = models.DateTimeField(default=datetime.now, verbose_name="收藏时间")

    class Meta:
        verbose_name = '收藏'
        verbose_name_plural = verbose_name


class Recommend(models.Model):
    id = models.AutoField
    photo = models.CharField(null=False, max_length=500, verbose_name="图片链接")
    url = models.CharField(null=False, max_length=500, verbose_name="链接")
    create_time = models.DateTimeField(default=datetime.now, verbose_name="创建时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="更新时间")

    class Meta:
        verbose_name = "推荐"
        verbose_name_plural = verbose_name

    @staticmethod
    def get_recommends():
        recommends = Recommend.objects.all().order_by("-update_time")[:3]
        data = [{
            "photo": recommend.photo,
            "url": recommend.url
        } for recommend in recommends]
        return data
