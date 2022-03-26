import json

from django.http  import JsonResponse
from django.views import View
from django.forms import ValidationError

from .models          import Post, Image
from users.models     import User
from utils.decorators import login_decorate
from utils.validators import url_validator

class MyPostView(View):
    @login_decorate
    def post(self, request):
        try:
            data   = json.loads(request.body)
            user   = request.user
            images = data["images"].split(",")

            for image in images:
                url_validator(image)
            
            if len(images) > 10:
                return JsonResponse({"message" : "You can only take up to 10 images."}, status = 400)

            post = Post.objects.create(
                user    = user,
                content = data["content"]
            )

            for image in images:
                Image.objects.create(
                    post      = post,
                    image_url = image
                )

            return JsonResponse({"created" : post.id}, status = 200)
        except KeyError:
            return JsonResponse({"message" : "Image was not entered."}, status = 400)
        except ValidationError as e:
            return JsonResponse({"message" : e.message}, status = 400)
    
    @login_decorate
    def get(self, request):
        user  = request.user
        posts = Post.objects.filter(user = user)

        my_posts = [{
            "1. user"      : user.name,
            "2. content"   : post.content,
            "3. images"    : [image.image_url for image in post.images.all()],
            "4. created_at": post.created_at
        } for post in posts]

        return JsonResponse({"my_posts" : my_posts}, status = 200)


