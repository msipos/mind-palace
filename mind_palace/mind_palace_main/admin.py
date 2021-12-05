import pprint

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

from mind_palace.mind_palace_main.models import Collection
from mind_palace.mind_palace_main.models.note_model import Note, SnoozeEvent


# Register sessions in admin
class SessionAdmin(admin.ModelAdmin):
    def user(self, obj):
        session_user = obj.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=session_user)
        return user.username

    def _session_data(self, obj):
        return pprint.pformat(obj.get_decoded()).replace('\n', '<br>\n')


    _session_data.allow_tags=True
    list_display = ['user', 'session_key', '_session_data', 'expire_date']
    readonly_fields = ['_session_data']
    exclude = ['session_data']
    date_hierarchy='expire_date'


admin.site.register(Session, SessionAdmin)


# Register collections, notes and snooze events
for m in [Collection, Note, SnoozeEvent]:
    admin.site.register(m)


pfx = settings.MIND_PALACE_URL_PREFIX
admin.site.site_url = f'/{pfx}'
admin.site.site_header = 'Mind Palace Admin'
