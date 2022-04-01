# from dynamic_preferences.preferences import Section
# from dynamic_preferences.registries import global_preferences_registry
# from dynamic_preferences.types import ChoicePreference, StringPreference
# from dynamic_preferences.users.registries import user_preferences_registry

# general = Section("general")
# user = Section("user")


# @global_preferences_registry.register
# class GlobalPreference(StringPreference):
#     """A pointless globale preference to demonstrate usage"""

#     section = general
#     name = "name"
#     required = True
#     default = "Just a string"


# @user_preferences_registry.register
# class Language(ChoicePreference):
#     section = user
#     name = "language"
#     choices = [
#         ("en", "English"),
#         ("fr", "France"),
#     ]
#     default = "en"
