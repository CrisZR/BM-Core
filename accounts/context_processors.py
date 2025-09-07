def theme_context(request):
    if request.user.is_authenticated:
        profile = getattr(request.user, "userprofile", None)
        if profile:
            return {"theme_preference": profile.theme_preference}
    return {"theme_preference": None}
