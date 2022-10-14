from rest_framework import permissions

# allowing only the owner to permit actions

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # return super().has_object_permission(request, view, obj)

        # check if user == author
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user