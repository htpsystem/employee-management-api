from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from employee_management.settings import AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_AUTHORITY, AZURE_REDIRECT_URI
from django.shortcuts import redirect
from django.contrib.auth import login as django_login
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.permissions import AllowAny, IsAuthenticated
import msal

User = get_user_model()

class AuthViewSet(ViewSet):

    def get_permissions(self):
        if self.action in ['login', 'callback']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_msal_app(self):
        return msal.ConfidentialClientApplication(
            client_id=AZURE_CLIENT_ID,
            authority=AZURE_AUTHORITY,
            client_credential=AZURE_CLIENT_SECRET,
        )
    
    @action(detail=False, methods=["get"])
    def login(self, request):
        msal_app = self.get_msal_app()
        auth_url = msal_app.get_authorization_request_url(
            scopes=[],
            redirect_uri=AZURE_REDIRECT_URI
        )
        return redirect(auth_url)
    
    @action(detail=False, methods=["get"])
    def logout(self, request):
        logout(request)
        return Response({"message": "Logged out successfully."}, status=HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def callback(self, request):
        code = request.GET.get("code")
        msal_app = self.get_msal_app()
        result = msal_app.acquire_token_by_authorization_code(
            code,
            scopes=[],
            redirect_uri=AZURE_REDIRECT_URI,
        )

        try:
            if "id_token_claims" in result:
                email = result["id_token_claims"].get("preferred_username")
                user = User.objects.get(email=email)
                django_login(request, user)
                return Response(user.get_employee_details())
            return Response(result, status=HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({"error": f"User '{email}'  does not exist"}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)