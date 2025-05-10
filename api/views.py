import msal
from employee_management.settings import AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_AUTHORITY, AZURE_REDIRECT_URI
from django.shortcuts import redirect
from django.contrib.auth import login as django_login
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view

User = get_user_model()

def get_msal_app():
    return msal.ConfidentialClientApplication(
        client_id=AZURE_CLIENT_ID,
        authority=AZURE_AUTHORITY,
        client_credential=AZURE_CLIENT_SECRET,
    )

@api_view(['GET'])
def login(request):
    msal_app = get_msal_app()
    auth_url = msal_app.get_authorization_request_url(
        scopes=[],
        redirect_uri=AZURE_REDIRECT_URI
    )
    return redirect(auth_url)

@api_view(['GET'])
def callback(request):
    code = request.GET.get("code")
    msal_app = get_msal_app()
    result = msal_app.acquire_token_by_authorization_code(
        code,
        scopes=[],
        redirect_uri=AZURE_REDIRECT_URI,
    )
    if "id_token_claims" in result:
        email = result["id_token_claims"].get("preferred_username")
        user, _ = User.objects.get_or_create(email=email, defaults={"email": email})
        django_login(request, user)
        return Response(user.get)
    print(result)
    return Response(result, status=401)
