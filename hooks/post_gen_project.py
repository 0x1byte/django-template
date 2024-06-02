import os
import random
import shutil
import string


TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
SUCCESS = "\x1b[1;32m [SUCCESS]: "

DEBUG_VALUE = "debug"


def remove_open_source_files():
    file_names = ["CONTRIBUTORS.txt", "LICENSE"]
    for file_name in file_names:
        os.remove(file_name)


def remove_celery_files():
    file_names = [
        os.path.join("config", "celery_app.py"),
    ]
    for file_name in file_names:
        os.remove(file_name)


def remove_async_files():
    file_names = [
        os.path.join("config", "asgi.py"),
        os.path.join("config", "websocket.py"),
    ]
    for file_name in file_names:
        os.remove(file_name)


def generate_random_string(
    length, using_digits=False, using_ascii_letters=False, using_punctuation=False
):
    """
    Example:
        opting out for 50 symbol-long, [a-z][A-Z][0-9] string
        would yield log_2((26+26+50)^50) ~= 334 bit strength.
    """

    symbols = []
    if using_digits:
        symbols += string.digits
    if using_ascii_letters:
        symbols += string.ascii_letters
    if using_punctuation:
        all_punctuation = set(string.punctuation)
        # These symbols can cause issues in environment variables
        unsuitable = {"'", '"', "\\", "$"}
        suitable = all_punctuation.difference(unsuitable)
        symbols += "".join(suitable)
    return "".join([random.choice(symbols) for _ in range(length)])


def set_flag(file_path, flag, value=None, formatted=None, *args, **kwargs):
    if value is None:
        random_string = generate_random_string(*args, **kwargs)
        if random_string is None:
            print(
                "We couldn't find a secure pseudo-random number generator on your "
                "system. Please, make sure to manually {} later.".format(flag)
            )
            random_string = flag
        if formatted is not None:
            random_string = formatted.format(random_string)
        value = random_string

    with open(file_path, "r+") as f:
        file_contents = f.read().replace(flag, value)
        f.seek(0)
        f.write(file_contents)
        f.truncate()

    return value


def set_django_secret_key(file_path):
    django_secret_key = set_flag(
        file_path,
        "!!!SET DJANGO_SECRET_KEY!!!",
        length=64,
        using_digits=True,
        using_ascii_letters=True,
    )
    return django_secret_key


def set_django_admin_url(file_path):
    django_admin_url = set_flag(
        file_path,
        "!!!SET DJANGO_ADMIN_URL!!!",
        formatted="{}/",
        length=32,
        using_digits=True,
        using_ascii_letters=True,
    )
    return django_admin_url


def set_flags_in_settings_files():
    set_django_secret_key(os.path.join("config", "settings", "dev.py"))


def remove_drf_starter_files():
    os.remove(os.path.join("config", "api_router.py"))
    shutil.rmtree(os.path.join("{{cookiecutter.project_slug}}", "users", "api"))


def generate_random_user():
    return generate_random_string(length=32, using_ascii_letters=True)


def generate_postgres_user(debug=False):
    return DEBUG_VALUE if debug else generate_random_user()


def set_postgres_user(file_path, value):
    postgres_user = set_flag(file_path, "!!!SET POSTGRES_USER!!!", value=value)
    return postgres_user


def set_postgres_password(file_path, value=None):
    postgres_password = set_flag(
        file_path,
        "!!!SET POSTGRES_PASSWORD!!!",
        value=value,
        length=64,
        using_digits=True,
        using_ascii_letters=True,
    )
    return postgres_password


def set_celery_flower_user(file_path, value):
    celery_flower_user = set_flag(
        file_path, "!!!SET CELERY_FLOWER_USER!!!", value=value
    )
    return celery_flower_user


def set_celery_flower_password(file_path, value=None):
    celery_flower_password = set_flag(
        file_path,
        "!!!SET CELERY_FLOWER_PASSWORD!!!",
        value=value,
        length=64,
        using_digits=True,
        using_ascii_letters=True,
    )
    return celery_flower_password


def set_flags_in_envs(postgres_user, celery_flower_user, debug=False):

    set_django_secret_key(".env.sample")
    set_django_admin_url(".env.sample")
    set_postgres_user(".env.sample", value=postgres_user)
    set_postgres_password(".env.sample", value=DEBUG_VALUE if debug else None)
    set_postgres_user(".env.sample", value=postgres_user)
    set_postgres_password(".env.sample", value=DEBUG_VALUE if debug else None)
    set_celery_flower_user(".env.sample", value=celery_flower_user)
    set_celery_flower_password(".env.sample", value=DEBUG_VALUE if debug else None)
    set_celery_flower_user(".env.sample", value=celery_flower_user)
    set_celery_flower_password(".env.sample", value=DEBUG_VALUE if debug else None)


def main():

    debug = "{{ cookiecutter.debug }}".lower() == "y"

    set_flags_in_envs(
        DEBUG_VALUE if debug else generate_random_user(),
        DEBUG_VALUE if debug else generate_random_user(),
        debug=debug,
    )

    set_flags_in_settings_files()

    if "{{ cookiecutter.open_source_license }}" == "Not open source":
        remove_open_source_files()

    if "{{ cookiecutter.use_celery }}".lower() == "n":
        remove_celery_files()

    if "{{ cookiecutter.use_drf }}".lower() == "n":
        remove_drf_starter_files()

    if "{{ cookiecutter.use_async }}".lower() == "n":
        remove_async_files()

    print(SUCCESS + "Project initialized, keep up the good work!" + TERMINATOR)


if __name__ == "__main__":
    main()
