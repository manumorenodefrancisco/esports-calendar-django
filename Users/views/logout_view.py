from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist() #el token no servirá tras logout
            
            return Response({"success": True}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"success": False, "errors": ["Invalid token"]}, status=status.HTTP_400_BAD_REQUEST)
