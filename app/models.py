import math
from django.db import models

from users.models import User


class Item(models.Model):
    """
    データ定義クラス
      各フィールドを定義する
    参考：
    ・公式 モデルフィールドリファレンス
    https://docs.djangoproject.com/ja/2.1/ref/models/fields/
    """

    # サンプル項目1 文字列
    # sample_1 = models.CharField(
    #     verbose_name='サンプル項目1 文字列',
    #     max_length=20,
    #     blank=True,
    #     null=True,
    # )

    # サンプル項目2 メモ
    sample_2 = models.TextField(
        verbose_name='サンプル項目2 メモ',
        blank=True,
        null=True,
    )

    # サンプル項目3 整数
    sample_3 = models.IntegerField(
        verbose_name='サンプル項目3 整数',
        blank=True,
        null=True,
    )

    # サンプル項目4 浮動小数点
    sample_4 = models.FloatField(
        verbose_name='サンプル項目4 浮動小数点',
        blank=True,
        null=True,
    )

    # サンプル項目5 固定小数点
    sample_5 = models.DecimalField(
        verbose_name='サンプル項目5 固定小数点',
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )

    # サンプル項目6 ブール値
    sample_6 = models.BooleanField(
        verbose_name='サンプル項目6 ブール値',
    )

    # サンプル項目7 日付
    sample_7 = models.DateField(
        verbose_name='サンプル項目7 日付',
        blank=True,
        null=True,
    )

    # サンプル項目8 日時
    sample_8 = models.DateTimeField(
        verbose_name='サンプル項目8 日時',
        blank=True,
        null=True,
    )

    # サンプル項目9 選択肢（固定）
    sample_9_choice = (
        (1, '選択１'),
        (2, '選択２'),
        (3, '選択３'),
    )

    sample_9 = models.IntegerField(
        verbose_name='サンプル項目9_選択肢（固定）',
        choices=sample_9_choice,
        blank=True,
        null=True,
    )

    # サンプル項目9 選択肢（マスタ連動）
    sample_10 = models.ForeignKey(
        User,
        verbose_name='サンプル項目10_選択肢（マスタ連動）',
        blank=True,
        null=True,
        related_name='sample_10',
        on_delete=models.SET_NULL,
    )

    # 以下、管理項目

    # 作成者(ユーザー)
    created_by = models.ForeignKey(
        User,
        verbose_name='作成者',
        blank=True,
        null=True,
        related_name='CreatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )

    # 作成時間
    created_at = models.DateTimeField(
        verbose_name='作成時間',
        blank=True,
        null=True,
        editable=False,
    )

    # 更新者(ユーザー)
    updated_by = models.ForeignKey(
        User,
        verbose_name='更新者',
        blank=True,
        null=True,
        related_name='UpdatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )

    # 更新時間
    updated_at = models.DateTimeField(
        verbose_name='更新時間',
        blank=True,
        null=True,
        editable=False,
    )

    def __str__(self):
        """
        リストボックスや管理画面での表示
        """
        return self.sample_2

    class Meta:
        """
        管理画面でのタイトル表示
        """
        verbose_name = 'サンプル'
        verbose_name_plural = 'サンプル'

class Room(models.Model):

    title = models.CharField(
        verbose_name='タイトル',
        max_length=50,
        blank=False,
        null=False,
    )

    content = models.TextField(
        verbose_name='詳細',
        blank=True,
        null=True,
    )

    place = models.CharField(
        verbose_name='場所',
        max_length=50,
        blank=True,
        null=True,
    )

    start_at = models.DateTimeField(
        verbose_name='開始日時',
        blank=True,
        null=True,
    )

    # 以下、管理項目

    # 作成者(ユーザー)
    created_by = models.ForeignKey(
        User,
        verbose_name='作成者',
        blank=True,
        null=True,
        related_name='room_created_by',
        on_delete=models.SET_NULL,
        editable=False,
    )

    created_at = models.DateTimeField(
        verbose_name='作成時間',
        blank=True,
        null=True,
        editable=False,
    )

    # 更新者(ユーザー)
    updated_by = models.ForeignKey(
        User,
        verbose_name='更新者',
        blank=True,
        null=True,
        related_name='room_updated_by',
        on_delete=models.SET_NULL,
        editable=False,
    )

    # 更新時間
    updated_at = models.DateTimeField(
        verbose_name='更新時間',
        blank=True,
        null=True,
        editable=False,
    )

    def __str__(self):
        """
        リストボックスや管理画面での表示
        """
        return self.title

    def is_owner(self, room_id, user_id):
        return len(RoomUser.objects.all().filter(room_id=room_id, user_id=user_id, is_owner=1)) > 0

    def get_users_except_owner(room_id):
        return User.objects.raw('select * from users_user INNER JOIN app_roomuser on users_user.id=app_roomuser.user_id INNER JOIN app_room on app_roomuser.room_id=app_room.id where app_room.id=%s and app_roomuser.is_owner is False', [room_id])
class RoomJoinRequest(models.Model):

    comment = models.TextField(
        verbose_name='コメント',
        blank=True,
        null=True,
    )

    room = models.ForeignKey(
        Room,
        verbose_name='部屋ID',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        editable=False,
    )

    user = models.ForeignKey(
        User,
        verbose_name='ユーザID',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        editable=False,
    )
    created_at = models.DateTimeField(
        verbose_name='作成時間',
        blank=True,
        null=True,
        editable=False,
    )

    is_approved = models.BooleanField(
        verbose_name='承認済み',
        default=False,
        editable=False,
    )

    def __str__(self):
        """
        リストボックスや管理画面での表示
        """
        return self.comment

class RoomUser(models.Model):

    room = models.ForeignKey(
        Room,
        verbose_name='部屋ID',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        editable=False,
    )

    user = models.ForeignKey(
        User,
        verbose_name='ユーザID',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        editable=False,
    )

    is_owner = models.BooleanField(
        verbose_name='オーナーである',
        default=False,
        editable=False,
    )

    created_at = models.DateTimeField(
        verbose_name='作成時間',
        blank=True,
        null=True,
        editable=False,
    )
    def exists(self, room_id, user_id):
        return len(RoomUser.objects.all().filter(room_id=room_id, user_id=user_id)) > 0

class Comment(models.Model):

    content = models.TextField(
        verbose_name='コメント',
        blank=True,
        null=True,
    )

    room = models.ForeignKey(
        Room,
        verbose_name='部屋ID',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        editable=False,
    )

    user = models.ForeignKey(
        User,
        verbose_name='ユーザID',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        editable=False,
    )
    created_at = models.DateTimeField(
        verbose_name='作成時間',
        blank=True,
        null=True,
        editable=False,
    )

    def __str__(self):
        """
        リストボックスや管理画面での表示
        """
        return self.comment
class Oshihiki(models.Model):
    HONBA = 300
    point = models.FloatField(
        verbose_name='点数',
        blank=True,
        null=True,
    )

    is_ryokei = models.BooleanField(
        verbose_name='待ち',
        default=True,
        editable=False,
    )

    hoju_rate = models.FloatField(
        verbose_name='放銃率',
        blank=True,
        null=True,
    )

    junme = models.IntegerField(
        verbose_name='順目',
        blank=True,
        null=True,
    )

    you_are_parent = models.BooleanField(
        verbose_name='自分',
        default=False,
        editable=False,
        null=False,
    )

    oponent_is_parent = models.BooleanField(
        verbose_name='相手',
        default=False,
        editable=False,
    )

    is_dora = models.BooleanField(
        verbose_name='一発 or ドラ',
        default=False,
        editable=False,
    )

    def __str__(self):
        """
        リストボックスや管理画面での表示
        """
        return self.point

    def get_required_point(self, point, is_ryokei, hoju_rate, junme, you_are_parent, oponent_is_parent, is_dora):
        oshihiki = Oshihiki.objects.filter(
            is_ryokei=is_ryokei, hoju_rate=hoju_rate, junme=junme, you_are_parent=you_are_parent, oponent_is_parent=oponent_is_parent, is_dora=is_dora)

        if not oshihiki:
            return None

        # TODO
        # 和了価値指標計算
        # 鳴きor門前
        # 天鳳 or Mリーグルール
        return math.floor(oshihiki[0].point)

    def get_parent_point(self, child_point):
        PARENT_POINT_DICT = {
            1000: 1500,
            2000: 2900,
            3900: 5800,
            7700: 11600,
        }
        return PARENT_POINT_DICT[child_point]

    def get_point_option(self):
        point_option = []
        point_option.append({'fu': 30, 'han': 1, 'child_point': 1000, 'parent_point': 1500})
        point_option.append({'fu': 30, 'han': 2, 'child_point': 2000, 'parent_point': 2900})
        point_option.append({'fu': 30, 'han': 3, 'child_point': 3900, 'parent_point': 5800})
        point_option.append({'fu': 30, 'han': 4, 'child_point': 7700, 'parent_point': 11600})

        return point_option

    def get_hoju_rate_option(self):
        hoju_rate_option = []
        hoju_rate_option.append({'value': 5, 'example': 'スジ9本 外側28'})
        hoju_rate_option.append({'value': 10, 'example': 'スジ9本 無スジ28'})
        hoju_rate_option.append({'value': 15, 'example': 'スジ12本 無スジ28'})
        hoju_rate_option.append({'value': 20, 'example': 'スジ14本 無スジ28'})
        hoju_rate_option.append({'value': 25, 'example': 'スジ16本 無スジ28'})

        return hoju_rate_option

    def get_kyotaku_option(self):
        kyotaku_option = []
        for i in range(1, 10, 1):
            kyotaku = {'num': i, 'point': i * 1000}
            kyotaku_option.append(kyotaku)

        return kyotaku_option

    def get_honba_option(self):
        honba_option = []
        for i in range(0, 10, 1):
            honba = {'num': i, 'point': i * self.HONBA}
            honba_option.append(honba)

        return honba_option

    def get_your_point(self, point, kyotaku):

        return point + kyotaku * 1000
