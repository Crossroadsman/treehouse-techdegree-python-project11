import datetime
import tempfile
import unittest

from django.core.files.uploadedfile import SimpleUploadedFile

from pugorugh.file_handling import rename, handle_uploaded_file, process_upload


# Base TestCase
# =============
class FileHandlingTests(unittest.TestCase):

    # Setup and Teardown
    # ------------------
    def setUp(self):
        self.upload_dir = tempfile.TemporaryDirectory()

        self.test_content = "This is a test"
        self.test_uploadedfile = SimpleUploadedFile(
            'test_uploadedfile.test',
            self.test_content.encode()
        )


# TestCases
# =========
class RenameTests(FileHandlingTests):

    def test_rename_generates_correct_string(self):

        test_filename = "somejpg.bmp.jpg"
        test_prefix = "01"
        expected_result = "01.jpg"

        self.assertEqual(
            rename(test_filename, test_prefix),
            expected_result
        )


class HandleUploadedFileTests(FileHandlingTests):

    def test_upload_writes_file_to_disk(self):

        now = datetime.datetime.now()
        now = str(now.timestamp())

        test_path = self.upload_dir.name
        test_name = f"test_{now}.test"

        handle_uploaded_file(
            self.test_uploadedfile,
            test_path,
            test_name
        )

        # test we can read the file
        # (implicitly tests correct filename)
        with open(f'{test_path}/{test_name}', 'r') as fh:
            result = fh.readline()

        self.assertEqual(
            result,
            self.test_content
        )


class ProcessUploadTests(FileHandlingTests):

    def test_process_upload_returns_correct_filename(self):

        test_pk = '02'
        expected_name = rename(self.test_uploadedfile.name, test_pk)

        result = process_upload(self.test_uploadedfile, test_pk, self.upload_dir.name)

        self.assertEqual(
            result,
            expected_name
        )
