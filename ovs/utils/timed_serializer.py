"""Houses the timed serializer for secure token generation"""
from itsdangerous import URLSafeTimedSerializer

class Serializer():
    """Class to allow secure de/serialization of attributes using a salt."""
    ts = None

    @staticmethod
    def init_app(app):
        """
        Initializes the static serializer with the app's secret
        Note that it must be done in this manner because the app_context
        is not available until the application is created.

        Args:
            attr: The attribute to serialize
            key: The salt to use with the TimedSerializer

        Returns:
            The serialized string.
        """
        Serializer.ts = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    @staticmethod
    def serialize_attr(attr, key):
        """
        Serializes an attribute, using a key as a salt.

        Args:
            attr: The attribute to serialize
            key: The salt to use with the TimedSerializer

        Returns:
            The serialized string.
        """
        if not Serializer.ts:
            exit('Please initialize the serializer with a secret')

        return Serializer.ts.dumps(attr, salt=key)

    @staticmethod
    def decode_attr(attr, key):
        """
        Deserializes an attribute, using a key as a salt.

        Args:
            attr: The attribute to deserialize
            key: The salt to use with the TimedSerializer

        Returns:
            The deserialized string.
        """
        if not Serializer.ts:
            exit('Please initialize the serializer with a secret')

        return Serializer.ts.loads(attr, salt=key, max_age=86400)
