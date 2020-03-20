from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.shortcuts import redirect

from .filters import ItemFilterSet, RoomFilterSet, RoomJoinRequestFilterSet, CommentFilterSet, OshihikiFilterSet
from .forms import ItemForm, RoomForm, RoomJoinRequestForm, RoomUserForm, CommentForm
from .models import User, Item, Room, RoomJoinRequest, RoomUser, Comment, Oshihiki
from pprint import pprint
from django.db.models import Prefetch

# 未ログインのユーザーにアクセスを許可する場合は、LoginRequiredMixinを継承から外してください。
#
# LoginRequiredMixin：未ログインのユーザーをログイン画面に誘導するMixin
# 参考：https://docs.djangoproject.com/ja/2.1/topics/auth/default/#the-loginrequired-mixin


class ItemFilterView(LoginRequiredMixin, FilterView):
    """
    ビュー：一覧表示画面

    以下のパッケージを使用
    ・django-filter 一覧画面(ListView)に検索機能を追加
    https://django-filter.readthedocs.io/en/master/
    """
    model = Item

    # django-filter 設定
    filterset_class = ItemFilterSet
    # django-filter ver2.0対応 クエリ未設定時に全件表示する設定
    strict = False

    # 1ページの表示
    paginate_by = 10

    def get(self, request, **kwargs):
        """
        リクエスト受付
        セッション変数の管理:一覧画面と詳細画面間の移動時に検索条件が維持されるようにする。
        """

        # 一覧画面内の遷移(GETクエリがある)ならクエリを保存する
        if request.GET:
            request.session['query'] = request.GET
        # 詳細画面・登録画面からの遷移(GETクエリはない)ならクエリを復元する
        else:
            request.GET = request.GET.copy()
            if 'query' in request.session.keys():
                for key in request.session['query'].keys():
                    request.GET[key] = request.session['query'][key]

        return super().get(request, **kwargs)

    def get_queryset(self):
        """
        ソート順・デフォルトの絞り込みを指定
        """
        # デフォルトの並び順として、登録時間（降順）をセットする。
        return Item.objects.all().order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        表示データの設定
        """
        # 表示データを追加したい場合は、ここでキーを追加しテンプレート上で表示する
        # 例：kwargs['sample'] = 'sample'
        return super().get_context_data(object_list=object_list, **kwargs)


class ItemDetailView(LoginRequiredMixin, DetailView):
    """
    ビュー：詳細画面
    """
    model = Item

    def get_context_data(self, **kwargs):
        """
        表示データの設定
        """
        # 表示データの追加はここで 例：
        # kwargs['sample'] = 'sample'
        return super().get_context_data(**kwargs)


class ItemCreateView(LoginRequiredMixin, CreateView):
    """
    ビュー：登録画面
    """
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        """
        登録処理
        """
        item = form.save(commit=False)
        item.created_by = self.request.user
        item.created_at = timezone.now()
        item.updated_by = self.request.user
        item.updated_at = timezone.now()
        item.save()

        return HttpResponseRedirect(self.success_url)


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    """
    ビュー：更新画面
    """
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        """
        更新処理
        """
        item = form.save(commit=False)
        item.updated_by = self.request.user
        item.updated_at = timezone.now()
        item.save()

        return HttpResponseRedirect(self.success_url)


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    """
    ビュー：削除画面
    """
    model = Item
    success_url = reverse_lazy('index')

    def delete(self, request, *args, **kwargs):
        """
        削除処理
        """
        item = self.get_object()
        item.delete()

        return HttpResponseRedirect(self.success_url)


class RoomFilterView(FilterView):
    """
    ビュー：一覧表示画面

    以下のパッケージを使用
    ・django-filter 一覧画面(ListView)に検索機能を追加
    https://django-filter.readthedocs.io/en/master/
    """
    model = Room

    # django-filter 設定
    filterset_class = RoomFilterSet
    # django-filter ver2.0対応 クエリ未設定時に全件表示する設定
    strict = False

    # 1ページの表示
    paginate_by = 10

    def get(self, request, **kwargs):
        """
        リクエスト受付
        セッション変数の管理:一覧画面と詳細画面間の移動時に検索条件が維持されるようにする。
        """

        # 一覧画面内の遷移(GETクエリがある)ならクエリを保存する
        if request.GET:
            request.session['query'] = request.GET
        # 詳細画面・登録画面からの遷移(GETクエリはない)ならクエリを復元する
        else:
            request.GET = request.GET.copy()
            if 'query' in request.session.keys():
                for key in request.session['query'].keys():
                    request.GET[key] = request.session['query'][key]

        return super().get(request, **kwargs)

    def get_queryset(self):
        """
        ソート順・デフォルトの絞り込みを指定
        """

        # デフォルトの並び順として、登録時間（降順）をセットする。
        return Room.objects.all().order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        表示データの設定
        """
        # 表示データを追加したい場合は、ここでキーを追加しテンプレート上で表示する
        # 例：kwargs['sample'] = 'sample'

        rooms = Room.objects.all().order_by('-created_at').prefetch_related(Prefetch("roomjoinrequest_set",
                                                                                     queryset=RoomJoinRequest.objects.filter(user_id=self.request.user.id)))

        requested = {}
        is_room_user = {}
        room_users_except_owner = {}

        for room in rooms:
            # ルームに参加リクエストを送信しているかどうかを判定
            requested[room.id] = len(
                room.roomjoinrequest_set.all().filter(is_approved=0)) > 0
            # ルームの参加者であるかどうかを判定
            is_room_user[room.id] = RoomUser.exists(self, room.id, self.request.user.id)
            # ルームの参加者一覧を取得
            room_users_except_owner[room.id] = Room.get_users_except_owner(room.id)

        kwargs['requested'] = requested
        kwargs['is_room_user'] = is_room_user
        kwargs['room_users_except_owner'] = room_users_except_owner

        return super().get_context_data(object_list=object_list, **kwargs)


class RoomDetailView(DetailView):
    """
    ビュー：詳細画面
    """
    model = Room

    def get_context_data(self, **kwargs):
        """
        表示データの設定
        """
        room_join_requests = RoomJoinRequest.objects.all().filter(
            room_id=self.kwargs.get('pk'), user_id=self.request.user.id).order_by('-created_at')

        kwargs['requested'] = len(room_join_requests) > 0

        return super().get_context_data(**kwargs)


class RoomCreateView(CreateView):
    # TODO ログインしているか確認する処理
    """
    ビュー：登録画面
    """
    model = Room
    form_class = RoomForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        """
        登録処理
        """
        room = form.save(commit=False)
        room.created_by = self.request.user
        room.created_at = timezone.now()
        room.updated_by = self.request.user
        room.updated_at = timezone.now()
        room.save()

        RoomUser.objects.create(
            room_id=room.id, user_id=self.request.user.id, created_at=timezone.now(), is_owner=1)

        return HttpResponseRedirect(self.success_url)


class RoomUpdateView(UpdateView):
    # TODO ログインしているか確認する処理
    """
    ビュー：更新画面
    """
    model = Room
    form_class = RoomForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        """
        更新処理
        """
        room = form.save(commit=False)
        room.updated_by = self.request.user
        room.updated_at = timezone.now()
        room.save()

        return HttpResponseRedirect(self.success_url)


class RoomDeleteView(DeleteView):
    # TODO ログインしているか確認する処理
    """
    ビュー：削除画面
    """
    model = Room
    success_url = reverse_lazy('index')

    def delete(self, request, *args, **kwargs):
        """
        削除処理
        """
        room = self.get_object()
        room.delete()

        return HttpResponseRedirect(self.success_url)


class RoomJoinRequestCreateView(LoginRequiredMixin, CreateView):
    # TODO ログインしているか確認する処理
    """
    ビュー：登録画面
    """
    model = RoomJoinRequest
    form_class = RoomJoinRequestForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        """
        登録処理
        """
        roomjoinreqest = form.save(commit=False)
        roomjoinreqest.user = self.request.user
        roomjoinreqest.room = Room.objects.get(pk=self.kwargs.get('pk'))
        roomjoinreqest.created_at = timezone.now()
        roomjoinreqest.save()

        return HttpResponseRedirect(self.success_url)


class RoomJoinRequestFilterView(LoginRequiredMixin, FilterView):
    model = RoomJoinRequest

    # django-filter 設定
    filterset_class = RoomJoinRequestFilterSet
    # django-filter ver2.0対応 クエリ未設定時に全件表示する設定
    strict = False

    # 1ページの表示
    paginate_by = 10

    def get(self, request, **kwargs):
        """
        リクエスト受付
        セッション変数の管理:一覧画面と詳細画面間の移動時に検索条件が維持されるようにする。
        """
        if not Room.is_owner(self, self.kwargs.get('pk'), self.request.user.id):
            return redirect("index")

        # 一覧画面内の遷移(GETクエリがある)ならクエリを保存する
        if request.GET:
            request.session['query'] = request.GET
        # 詳細画面・登録画面からの遷移(GETクエリはない)ならクエリを復元する
        else:
            request.GET = request.GET.copy()
            if 'query' in request.session.keys():
                for key in request.session['query'].keys():
                    request.GET[key] = request.session['query'][key]

        return super().get(request, **kwargs)

    def get_queryset(self):

        return RoomJoinRequest.objects.all().filter(room_id=self.kwargs.get('pk'), is_approved=False).order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):

        return super().get_context_data(object_list=object_list, **kwargs)


class RoomUserCreateView(LoginRequiredMixin, CreateView):
    """
    ビュー：登録画面
    """
    model = RoomUser
    form_class = RoomUserForm

    def get_success_url(self):
        return reverse('room_join_request', kwargs={"pk": self.kwargs.get('pk')})

    def form_valid(self, form):
        if not Room.is_owner(self, self.kwargs.get('pk'), self.request.user.id):
            return redirect("index")
        """
        登録処理
        """
        room_join_request = RoomJoinRequest.objects.get(
            pk=self.request.POST['roomjoinrequest_id'])

        roomuser = form.save(commit=False)
        roomuser.user = User.objects.get(pk=room_join_request.user.id)
        roomuser.room = Room.objects.get(pk=room_join_request.room.id)
        roomuser.created_at = timezone.now()
        roomuser.save()

        room_join_request.is_approved = True
        room_join_request.save()

        return super(RoomUserCreateView, self).form_valid(form)


class CommentFilterView(LoginRequiredMixin, FilterView):
    model = RoomJoinRequest

    # django-filter 設定
    filterset_class = CommentFilterSet
    # django-filter ver2.0対応 クエリ未設定時に全件表示する設定
    strict = False

    # 1ページの表示
    paginate_by = 1000

    def get(self, request, **kwargs):
        """
        リクエスト受付
        セッション変数の管理:一覧画面と詳細画面間の移動時に検索条件が維持されるようにする。
        """
        if not RoomUser.exists(self, self.kwargs.get('pk'), self.request.user.id):
            return redirect("index")

        # 一覧画面内の遷移(GETクエリがある)ならクエリを保存する
        if request.GET:
            request.session['query'] = request.GET
        # 詳細画面・登録画面からの遷移(GETクエリはない)ならクエリを復元する
        else:
            request.GET = request.GET.copy()
            if 'query' in request.session.keys():
                for key in request.session['query'].keys():
                    request.GET[key] = request.session['query'][key]

        return super().get(request, **kwargs)

    def get_queryset(self):

        return Comment.objects.all().filter(room_id=self.kwargs.get('pk')).order_by('created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        room = Room.objects.get(pk=self.kwargs.get('pk'))
        room_users_except_owner = Room.get_users_except_owner(room.id)

        kwargs['room'] = room
        kwargs['room_users_except_owner'] = room_users_except_owner

        return super().get_context_data(object_list=object_list, **kwargs)


class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    ビュー：登録画面
    """
    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        return reverse('talk', kwargs={"pk": self.kwargs.get('pk')})

    def form_valid(self, form):
        if not RoomUser.exists(self, self.kwargs.get('pk'), self.request.user.id):
            return redirect("index")
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.room = Room.objects.get(pk=self.kwargs.get('pk'))
        comment.content = self.request.POST['content']
        comment.created_at = timezone.now()
        comment.save()

        return super(CommentCreateView, self).form_valid(form)


class OshihikiFilterView(FilterView):
    """
    ビュー：一覧表示画面

    以下のパッケージを使用
    ・django-filter 一覧画面(ListView)に検索機能を追加
    https://django-filter.readthedocs.io/en/master/
    """
    model = Oshihiki

    # django-filter 設定
    filterset_class = OshihikiFilterSet
    # django-filter ver2.0対応 クエリ未設定時に全件表示する設定
    strict = False

    # 1ページの表示
    paginate_by = 10

    def get(self, request, **kwargs):
        """
        リクエスト受付
        セッション変数の管理:一覧画面と詳細画面間の移動時に検索条件が維持されるようにする。
        """

        # 一覧画面内の遷移(GETクエリがある)ならクエリを保存する
        if request.GET:
            request.session['query'] = request.GET
        return super().get(request, **kwargs)

    def get_queryset(self):
        """
        ソート順・デフォルトの絞り込みを指定
        """
        # デフォルトの並び順として、登録時間（降順）をセットする。
        return Oshihiki.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        oshihiki = Oshihiki()
        kwargs['point_option'] = oshihiki.get_point_option()
        kwargs['kyotaku_option'] = oshihiki.get_kyotaku_option()
        kwargs['honba_option'] = oshihiki.get_honba_option()
        kwargs['hoju_rate_option'] = oshihiki.get_hoju_rate_option()

        try:
            point = int(self.request.GET.get("point"))
            kyotaku = int(self.request.GET.get("kyotaku"))
            is_ryokei = int(self.request.GET.get("is_ryokei"))
            hoju_rate = int(self.request.GET.get("hoju_rate"))
            junme = int(self.request.GET.get("junme"))
            you_are_parent = int(self.request.GET.get("you_are_parent"))
            oponent_is_parent = int(self.request.GET.get("oponent_is_parent"))
            is_dora = int(self.request.GET.get("is_dora"))

            kwargs['point'] = point
            kwargs['is_ryokei'] = is_ryokei
            kwargs['hoju_rate'] = hoju_rate
            kwargs['junme'] = junme
            kwargs['you_are_parent'] = you_are_parent
            kwargs['oponent_is_parent'] = oponent_is_parent
            kwargs['is_dora'] = is_dora
            kwargs['kyotaku'] = kyotaku

            required_point = oshihiki.get_required_point(point, is_ryokei, hoju_rate, junme, you_are_parent, oponent_is_parent, is_dora)

            if required_point is None:
                kwargs['cannot_judge'] = True
                kwargs['judge'] = False
            else:
                kwargs['required_point'] = required_point

                # 親の場合は点数変換
                if you_are_parent == 1:
                    point = oshihiki.get_parent_point(point)

                your_point = oshihiki.get_your_point(point, kyotaku)
                kwargs['your_point'] = your_point
                kwargs['should_push'] = your_point >= required_point
                kwargs['judge'] = True
        except ValueError:
            kwargs['judge'] = False
        except TypeError:
            kwargs['judge'] = False
        except KeyError:
            kwargs['judge'] = False

        return super().get_context_data(object_list=object_list, **kwargs)
