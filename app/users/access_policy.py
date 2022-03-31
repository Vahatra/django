from rest_access_policy import AccessPolicy


class UserAccessPolicy(AccessPolicy):
    statements = [
        # create
        {
            "action": ["create"],
            "principal": ["group:admin"],
            "effect": "allow",
        },
        # read
        {
            "action": ["list"],
            "principal": "authenticated",
            "effect": "allow",
        },
        {
            "action": ["retrieve"],
            "principal": "authenticated",
            "effect": "allow",
        },
        # uppdate
        {
            "action": ["update", "partial_update"],
            "principal": "authenticated",
            "effect": "allow",
        },
        # delete
        {
            "action": ["destroy"],
            "principal": ["group:admin"],
            "effect": "allow",
        },
        # other
        {
            "action": ["me"],
            "principal": "authenticated",
            "effect": "allow",
        },
        {
            "action": ["activate", "deactivate"],
            "principal": ["group:admin"],
            "effect": "allow",
        },
        {
            "action": ["reset_password", "reset_password_confirm"],
            "principal": "*",
            "effect": "allow",
        },
        {
            "action": ["profile"],
            "principal": "*",
            "effect": "allow",
        },
    ]

    @classmethod
    def scope_queryset(cls, request, queryset):
        user = request.user
        if not user.is_staff:
            return queryset.filter(pk=user.pk)

        return queryset

    def is_me(self, request, view, action) -> bool:
        return view.get_object() == request.user
