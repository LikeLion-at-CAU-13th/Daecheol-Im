from rest_framework.permissions import BasePermission, SAFE_METHODS
from datetime import datetime
import pytz

#�� 10�� ~ ��ħ 7�� ���̿��� ���� ����
class TimeRestrictedPermission(BasePermission):
    def has_permission(self, request, view):
        kst = pytz.timezone('Asia/Seoul')
        # �ѱ��ð����� ����
        now = datetime.now(kst).time()
        # datetime.now().time() -> �ð� ��ü�� ���� ex) 14:28:00
        if now.hour >= 22 or now.hour < 7:
            return False
        return True # �̿� �ð��̸� ���� ���

#�ۼ��ڸ� ����/���� ����, �� �ܴ� �б⸸ ����
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS�� �ش��ϴ� ��û�̸� ���� ���
        if request.method in SAFE_METHODS:
            return True
        # �̿��� ��û�� �ۼ��ڸ� ���� ���
        return obj.user == request.user
    
class TimeAndOwnerPermission(TimeRestrictedPermission, IsOwnerOrReadOnly):
    def has_permission(self, request, view):
        # TimeRestrictedPermission�� has_permission�� ���
        return TimeRestrictedPermission().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        # IsOwnerOrReadOnly�� has_object_permission�� ���
        return IsOwnerOrReadOnly().has_object_permission(request, view, obj)
