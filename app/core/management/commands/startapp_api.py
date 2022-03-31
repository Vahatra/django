import os

from django.conf import settings
from django.core.management.base import CommandError
from django.core.management.templates import TemplateCommand


class Command(TemplateCommand):
    help = (
        "Creates a Django app directory structure for the given app name in "
        "the current directory or optionally in the given directory."
    )
    missing_args_message = "You must provide an application name."

    def validate_name(self, name, name_or_dir="name"):
        # super().validate_name(name, name_or_dir="name")
        if name is None:
            raise CommandError(
                "you must provide {an} {app} name".format(
                    an=self.a_or_an,
                    app=self.app_or_project,
                )
            )
        # Check it's a valid directory name.
        if not name.isidentifier():
            raise CommandError(
                "'{name}' is not a valid {app} {type}. Please make sure the "
                "{type} is a valid identifier.".format(
                    name=name,
                    app=self.app_or_project,
                    type=name_or_dir,
                )
            )
        # removed this check because it always fails if we create the target dir
        # # Check it cannot be imported.
        # try:
        #     import_module(name)
        # except ImportError:
        #     pass
        # else:
        #     raise CommandError(
        #         "'{name}' conflictsss with the name of an existing Python "
        #         "module and cannot be used as {an} {app} {type}. Please try "
        #         "another {type}.".format(
        #             name=name,
        #             an=self.a_or_an,
        #             app=self.app_or_project,
        #             type=name_or_dir,
        #         )
        #     )

    def handle(self, **options):
        app_name = options.pop("name")
        template_dir = os.path.join(settings.APPS_DIR, "core/app_template")
        options["template"] = template_dir
        target_dir = os.path.join(settings.APPS_DIR, app_name)
        try:
            os.makedirs(target_dir)
        except FileExistsError:
            raise CommandError("'%s' already exists" % target_dir)
        except OSError as e:
            raise CommandError(e)
        super().handle("app", app_name, target_dir, **options)
