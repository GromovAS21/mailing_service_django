from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications.serializers import NotificationSerializer


class NotifyView(APIView):
    """Представление для отправки уведомлений."""

    def post(self, request) -> Response:
        """Отправка уведомлений."""
        serializer = NotificationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
