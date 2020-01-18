from django import forms

from .models import Item, Room, RoomJoinRequest, RoomUser


class ItemForm(forms.ModelForm):
    """
    モデルフォーム構成クラス
    ・公式 モデルからフォームを作成する
    https://docs.djangoproject.com/ja/2.1/topics/forms/modelforms/
    """

    class Meta:
        model = Item
        fields = '__all__'

        # 以下のフィールド以外が入力フォームに表示される
        # AutoField
        # auto_now=True
        # auto_now_add=Ture
        # editable=False

class RoomForm(forms.ModelForm):

    class Meta:
        model = Room
        fields = '__all__'

class RoomJoinRequestForm(forms.ModelForm):

    class Meta:
        model = RoomJoinRequest
        fields = '__all__'

class RoomUserForm(forms.ModelForm):

    class Meta:
        model = RoomUser
        fields = '__all__'
