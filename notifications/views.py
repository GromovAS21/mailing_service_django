from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications.serializers import NotificationSerializer
from notifications.utils import send_notification


class NotifyView(APIView):
    """Представление для отправки уведомлений."""

    def post(self, request) -> Response:
        """Отправка уведомлений."""
        serializer = NotificationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        recipients = serializer.initial_data["recipient"]
        message = serializer.initial_data["message"]
        delay = serializer.initial_data["delay"]
        try:
            send_notification(recipients, message, delay)
        except Exception as e:
            return Response(
                {"message": f"Ошибка отправки уведомлений: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        else:
            return Response({"message": "Уведомления отправлены"}, status=status.HTTP_200_OK)
