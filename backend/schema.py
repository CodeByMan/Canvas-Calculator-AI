import base64
import binascii

from pydantic import BaseModel, ConfigDict, StrictFloat, StrictInt, StrictStr, field_validator

from constants import (
    MAX_IMAGE_BASE64_CHARS,
    MAX_IMAGE_BYTES,
    MAX_VARIABLE_KEY_LENGTH,
    MAX_VARIABLES,
    MAX_VARIABLE_VALUE_LENGTH,
)


VariableValue = StrictStr | StrictInt | StrictFloat


class ImageData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    image: str
    dict_of_vars: dict[str, VariableValue]

    @field_validator("image")
    @classmethod
    def validate_image(cls, value: str) -> str:
        if len(value) > MAX_IMAGE_BASE64_CHARS:
            raise ValueError("Image payload is too large")

        prefix, separator, encoded_image = value.partition(",")
        allowed_prefixes = {
            "data:image/png;base64",
            "data:image/jpeg;base64",
            "data:image/jpg;base64",
            "data:image/webp;base64",
        }
        if not separator or prefix.lower() not in allowed_prefixes:
            raise ValueError("Image must be a PNG, JPEG, or WebP data URL")

        try:
            decoded_image = base64.b64decode(encoded_image, validate=True)
        except (binascii.Error, ValueError) as error:
            raise ValueError("Image data is not valid base64") from error

        if not decoded_image or len(decoded_image) > MAX_IMAGE_BYTES:
            raise ValueError("Image payload is too large or empty")

        return value

    @field_validator("dict_of_vars")
    @classmethod
    def validate_variables(cls, value: dict[str, VariableValue]) -> dict[str, VariableValue]:
        if len(value) > MAX_VARIABLES:
            raise ValueError(f"A maximum of {MAX_VARIABLES} variables is supported")

        for key, variable_value in value.items():
            if len(key) > MAX_VARIABLE_KEY_LENGTH:
                raise ValueError("Variable names are too long")
            if isinstance(variable_value, str) and len(variable_value) > MAX_VARIABLE_VALUE_LENGTH:
                raise ValueError("Variable values are too long")

        return value
