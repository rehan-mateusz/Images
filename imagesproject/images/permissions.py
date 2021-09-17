from rest_framework import permissions


class IsImageOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, image):
        return image.owner == request.user

class IsImageOwnerAndCanLink(permissions.BasePermission):

    def has_object_permission(self, request, view, image):
        return ((image.owner == request.user) and request.user.plan.can_share)
