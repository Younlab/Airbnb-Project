from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated as DefaultIsAuthenticated

__all__ = (
    'AdminUserReadOnly',
    'IsAuthenticated',

)

User = get_user_model()


class AdminUserReadOnly(permissions.BasePermission):
    """
    Admin User만 접근 가능한 권한
    """

    def has_permission(self, request, view):
        # IsAdminUser permission참조해서 다시 작성
        # True or False를 반환
        # request.user의 어떤 요소를 검사 후, 권한이 있다면 True 아니면 False를 리턴
        return request.user.is_superuser


class IsAuthenticated(DefaultIsAuthenticated):
    pass
