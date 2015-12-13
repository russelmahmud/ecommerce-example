from rest_framework import permissions


class IsStaffOrTargetUser(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        # allow logged in user to view own details, allows staff to view all records
        return request.user.is_staff or obj == request.user
