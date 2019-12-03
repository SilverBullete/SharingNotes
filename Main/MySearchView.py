import json

from haystack.views import SearchView
from .response import APIResult
from .models import User, User_Note

true = True


class MySearchView(SearchView):
    def create_response(self):
        content = super(MySearchView, self).get_context()
        data = [{
            'id': result.object.id,
            'title': result.object.title,
            'content': eval(result.object.content),
            'hot': result.object.hot,
            'subject': result.object.subject.name,
            'author': User.objects.get(
                user_bh=User_Note.objects.get(note_id=result.object.id).user).nickName,
            'time': result.object.update_time.strftime("%Y-%m-%d")
        } for result in content['page'].object_list]
        sorted(data, key=lambda d: d["hot"], reverse=True)
        subject_list = ['全部']
        for data_info in data:
            if data_info['subject'] not in subject_list:
                subject_list.append(data_info['subject'])
        return APIResult({
            'notes': data,
            'subject_list': subject_list
        })
