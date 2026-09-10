import base64
import unittest

from pydantic import ValidationError

from schema import ImageData


VALID_IMAGE = "data:image/png;base64," + base64.b64encode(b"test-image").decode("ascii")


class ImageDataValidationTests(unittest.TestCase):
    def test_accepts_supported_data_url(self):
        data = ImageData(image=VALID_IMAGE, dict_of_vars={"x": 4})

        self.assertEqual(data.dict_of_vars["x"], 4)

    def test_rejects_non_image_data_url(self):
        with self.assertRaises(ValidationError):
            ImageData(image="data:text/plain;base64,dGVzdA==", dict_of_vars={})

    def test_rejects_invalid_base64(self):
        with self.assertRaises(ValidationError):
            ImageData(image="data:image/png;base64,not valid base64", dict_of_vars={})

    def test_rejects_too_many_variables(self):
        variables = {f"x{index}": index for index in range(51)}

        with self.assertRaises(ValidationError):
            ImageData(image=VALID_IMAGE, dict_of_vars=variables)


if __name__ == "__main__":
    unittest.main()
