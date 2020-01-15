import logging
from pathlib import Path

from django.conf import settings


def rename(filename, prefix):
    """takes two strings (representing a filename and a prefix) and returns a
    string representing a new filename.
    Example:
    ("foo.jpeg", "bar") -> "bar.jpeg"
    """
    extension = Path(filename).suffix  # still has the `.`
    return f'{prefix}{extension}'


def handle_uploaded_file(uploaded_file, path, name):
    """See https://docs.djangoproject.com/en/2.2/topics/http/file-uploads/ for
    this function and why we use chunks

    `uploaded_file` is of type `UploadedFile` (see process_upload())
    `path` is a string describing the path to the file (ending with `/`)
    `name` is the filename to be written to disk
    """

    logging.debug(f'creating file at {path} called {name}')

    # (w)rite (b)inary mode (+)can update
    with open(f'{path}/{name}', 'wb+') as target_file:
        for chunk in uploaded_file.chunks():
            target_file.write(chunk)

    logging.debug(f'done creating file')


# Note we might need to set MEDIA_URL and MEDIA_ROOT in settings.py (and
# redirect them to static, since react is looking for the images in static)
# (for further discussion see:
# https://simpleisbetterthancomplex.com/tutorial/
# 2016/08/01/how-to-upload-files-with-django.html)
def process_upload(file, pk, upload_dir=settings.DOG_UPLOAD_DIR):
    """Takes `file` of type `UploadedFile` (the type of the 'files' in
    `request.FILES`) then:
    1. creates a new filename from the supplied `pk`;
    2. writes the uploaded file to disk
    3. returns the new filename as a string

    For more on `UploadedFile` see:
    https://docs.djangoproject.com/en/2.2/ref/files/uploads/#uploaded-files
    """

    # 1
    new_name = rename(file.name, pk)

    # 2
    handle_uploaded_file(file, upload_dir, new_name)

    # 3
    return new_name
