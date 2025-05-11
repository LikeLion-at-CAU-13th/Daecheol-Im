from rest_framework.permissions import BasePermission, SAFE_METHODS
from datetime import datetime
import pytz

#밤 10시 ~ 아침 7시 사이에는 접근 금지
class TimeRestrictedPermission(BasePermission):
    def has_permission(self, request, view):
        kst = pytz.timezone('Asia/Seoul')
        # 한국시간으로 보정
        now = datetime.now(kst).time()
        # datetime.now().time() -> 시간 객체만 추출 ex) 14:28:00
        if now.hour >= 22 or now.hour < 7:
            return False
        return True # 이외 시간이면 접근 허용

#작성자만 수정/삭제 가능, 그 외는 읽기만 가능
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS에 해당하는 요청이면 권한 허용
        if request.method in SAFE_METHODS:
            return True
        # 이외의 요청은 작성자만 권한 허용
        return obj.user == request.user
    
class TimeAndOwnerPermission(TimeRestrictedPermission, IsOwnerOrReadOnly):
    def has_permission(self, request, view):
        # TimeRestrictedPermission의 has_permission을 사용
        return TimeRestrictedPermission().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        # IsOwnerOrReadOnly의 has_object_permission을 사용
        return IsOwnerOrReadOnly().has_object_permission(request, view, obj)
