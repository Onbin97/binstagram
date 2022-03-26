import json, bcrypt, jwt
from django.forms import ValidationError


from django.http import JsonResponse
from django.views import View
from django.db import IntegrityError

from .models import User
from utils.validators import email_validator, password_validator, phone_number_validator

class SignUpView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            email        = data["email"]
            phone_number = data["phone_number"]
            password     = data["password"]

            email_validator(email)
            password_validator(password)
            phone_number_validator(phone_number)

            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            User.objects.create(
                name         = data["name"],
                email        = email,
                password     = hashed_password,
                phone_number = phone_number
            )
            
            return JsonResponse({"message" : "SUCCESS"}, status = 201)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
        except IntegrityError:
            return JsonResponse({"message" : "This Email already exists..."})
        except ValidationError as e :
            return JsonResponse({"message" : e.message}, status = 400)

