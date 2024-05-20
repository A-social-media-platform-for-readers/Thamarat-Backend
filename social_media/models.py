from django.db import models


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    image = models.ImageField(upload_to="media/posts/images/", blank=True)
    video = models.FileField(upload_to="media/posts/videos/", blank=True)
    creat_time = models.DateTimeField(auto_now_add=True)
    like_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="posts"
    )

    class Meta:
        ordering = ["-creat_time"]  # Default ordering by latest posts first

    def __str__(self):
        if self.content:
            return f"{self.user.name}: {self.content[:25]}..."  # Truncated content for list displays
        else:
            if self.image:
                return f"{self.user.name}: Image Post"
            elif self.video:
                return f"{self.user.name}: Video Post"
            else:
                return f"{self.user.name}: Empty Post"

    def like(self):
        self.like_count += 1
        self.save()

    def remove_like(self):
        if self.like_count > 0:
            self.like_count -= 1
            self.save()

    def add_comment(self):
        self.comment_count += 1
        self.save()

    def remove_comment(self):
        if self.comment_count > 0:
            self.comment_count -= 1
            self.save()
