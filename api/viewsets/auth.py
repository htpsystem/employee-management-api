# api/views.py

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from employee_management.settings import AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_AUTHORITY, AZURE_REDIRECT_URI
from django.shortcuts import redirect
from django.contrib.auth import login as django_login
from django.contrib.auth import get_user_model
import msal

User = get_user_model()

class AuthViewSet(ViewSet):
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
                if not user:
                    return Response({"error": "User not found"}, status=404)
                print(user)
                django_login(request, user)
                return Response(user.get_employee_details())
            # print(result)
            return Response(result, status=401)
        except User.DoesNotExist:
            return Response({"error": f"User '{email}'  does not exist"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)