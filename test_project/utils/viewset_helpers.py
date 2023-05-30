from rest_framework.permissions import SAFE_METHODS


class SerializerFindMixin:
    def get_serializer_class(self):
        model_name = self.__class__.__name__[:-7]  # trim the last letters "ViewSet"
        serializers_mod_path = (
            self.__module__[: self.__module__.rfind(".")] + ".serializers"
        )
        serializers = __import__(
            serializers_mod_path,
            fromlist=[
                model_name + "Serializer",
                model_name + "DetailSerializer",
            ],
        )
        default_serializer = getattr(serializers, model_name + "Serializer")
        detail_serializer = getattr(
            serializers, model_name + "DetailSerializer", default_serializer
        )
        if self.request.method not in SAFE_METHODS:
            return default_serializer
        else:
            return detail_serializer
