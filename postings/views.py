import json

from django.http  import JsonResponse
from django.views import View
from django.forms import ValidationError

from .models          import Post, Image, Comments
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
            "1. user_name"      : user.name,
            "2. content"   : post.content,
            "3. images"    : [image.image_url for image in post.images.all()],
            "4. created_at": post.created_at
        } for post in posts]

        return JsonResponse({"my_posts" : my_posts}, status = 200)

class CommentView(View):
    @login_decorate
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user
            post = Post.objects.get(id = data["postID"])

            comment = Comments.objects.create(
                user    = user,
                post    = post,
                content = data["content"]
            )

            return JsonResponse({"created" : comment.id}, status = 201)
        except KeyError:
            return JsonResponse({"message" : "There is no content."}, status = 400)
        
    @login_decorate
    def get(self, request):
        data = json.loads(request.body)
        post = Post.objects.get(id = data["postID"])

        post_comments = [{
            "1. user_name" : comment.user.name,
            "2. content" : comment.content,
            "3. created_at" : comment.created_at
        } for comment in post.comments.all()]

        return JsonResponse({"post_comments" : post_comments}, status = 200)
