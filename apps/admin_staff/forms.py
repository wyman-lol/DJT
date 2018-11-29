from django import forms
from apps.forms import FormMixin
from apps.doc.models import Doc


class CoursePubForm(forms.Form, FormMixin):
    category_id = forms.IntegerField(error_messages={"required": "课程id错误"})
    teacher_id = forms.IntegerField(error_messages={"required": "讲师id错误"})
    title = forms.CharField(error_messages={"required": "新闻标题错误"})
    cover_url = forms.URLField(error_messages={"required": "课程封面", "invalid": "课程封面地址不合法"})
    video_url = forms.URLField(error_messages={"required": "课程视频不能为空", "invalid": "视频地址不合法"})
    duration = forms.IntegerField(error_messages={"required": "课程时长不能为空"})
    profile = forms.CharField(error_messages={"required": "课程简介不能为空"})
    outline = forms.CharField(error_messages={"required": "课程大纲不能为空"})


# 和models.serialize一样直接对读模型的字段验证
class DocUploadForm(forms.ModelForm, FormMixin):
    class Meta:
        model = Doc
        fields = '__all__'
        error_messages = {
            "file_path": {
                "required": "文件路径不能为空"
            },
            "title": {
                "required": "文档标题不能为空"
            }
        }
