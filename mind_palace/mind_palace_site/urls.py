from django.conf import settings
from django.contrib import admin
from django.urls import path

from mind_palace.mind_palace_main.views.api_views.collection_api_views import NewNoteAPIView, NewCollectionAPIView
from mind_palace.mind_palace_main.views.api_views.note_api_views import EditNoteAPIView, NoteActionAPIView
from mind_palace.mind_palace_main.views.api_views.repeat_api_views import RepeatAPIView
from mind_palace.mind_palace_main.views.auth_views import MpLoginView, MpLogoutView
from mind_palace.mind_palace_main.views.collection_views import ListCollectionView, NewNoteView
from mind_palace.mind_palace_main.views.home_view import HomeView
from mind_palace.mind_palace_main.views.note_views import ViewNoteView, EditNoteView
from mind_palace.mind_palace_main.views.repeat_views import RepeatView
from mind_palace.mind_palace_main.views.search_views import SearchResultsView

pfx = settings.MIND_PALACE_URL_PREFIX

urlpatterns = [
    # Auth and admin
    path(f'{pfx}admin/', admin.site.urls),
    path(f'{pfx}login/', MpLoginView.as_view(), name='login'),
    path(f'{pfx}logout/', MpLogoutView.as_view(), name='logout'),

    # Home/collections/notes
    path(f'{pfx}', HomeView.as_view(), name='home'),
    path(f'{pfx}c/<uuid:id>/', ListCollectionView.as_view(), name='list_collection'),
    path(f'{pfx}c/<uuid:id>/new/', NewNoteView.as_view(), name='new_note'),
    path(f'{pfx}n/<uuid:id>/', ViewNoteView.as_view(), name='view_note'),
    path(f'{pfx}n/<uuid:id>/edit/', EditNoteView.as_view(), name='edit_note'),
    path(f'{pfx}repeat/', RepeatView.as_view(), name='repeat'),
    path(f'{pfx}search/', SearchResultsView.as_view(), name='search'),

    # Api views
    path(f'{pfx}api/n/<uuid:id>/edit/', EditNoteAPIView.as_view(), name='api_edit_note'),
    path(f'{pfx}api/n/<uuid:id>/action/', NoteActionAPIView.as_view(), name='api_note_action'),
    path(f'{pfx}api/c/new/', NewCollectionAPIView.as_view(), name='api_new_collection'),
    path(f'{pfx}api/c/<uuid:id>/new/', NewNoteAPIView.as_view(), name='api_new_note'),
    path(f'{pfx}api/repeat/', RepeatAPIView.as_view(), name='api_repeat'),
]
