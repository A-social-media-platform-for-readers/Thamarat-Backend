from django.db import models
from django.urls import reverse
from users.models import User


class Post(models.Model):
    """
    Posts Model
    """

    id = models.AutoField(primary_key=True)
    content = models.TextField()
    image = models.ImageField(upload_to="media/posts/images/", blank=True)
    video = models.FileField(upload_to="media/posts/videos/", blank=True)
    creat_time = models.DateTimeField(auto_now_add=True)
    like_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    class Meta:
        """
        Default ordering by latest posts first.
        """

        ordering = ["-creat_time"]

    def __str__(self):
        """
        Returns the user name and the beginning of
        the content of the post.
        """
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
        """
        Add 1 to the like count.
        """
        self.like_count += 1
        self.save()

    def remove_like(self):
        """
        Remove 1 from the like count.
        """
        if self.like_count > 0:
            self.like_count -= 1
            self.save()

    def add_comment(self):
        """
        Add 1 to the comment count.
        """
        self.comment_count += 1
        self.save()

    def remove_comment(self):
        """
        Remove 1 from the comment count.
        """
        if self.comment_count > 0:
            self.comment_count -= 1
            self.save()


class Comment(models.Model):
    """
    Post 's Comments Model.
    """

    content = models.TextField(max_length=1024)
    created_time = models.DateTimeField(auto_now_add=True)
    like_count = models.PositiveIntegerField(default=0)
    inner_comment_count = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    class Meta:
        """
        Default ordering by latest posts first.
        """

        ordering = ["-creat_time"]

    def __str__(self):
        """
        Returns the user name, post id and the beginning of
        the content of the Comment.
        """
        return f"{self.user.name} on {self.post.id}: {self.content[:25]}..."

    def like(self):
        """
        Add 1 to the like count.
        """
        self.like_count += 1
        self.save()

    def remove_like(self):
        """
        Remove 1 from the like count.
        """
        if self.like_count > 0:
            self.like_count -= 1
            self.save()

    def add_inner_comment(self):
        """
        Add 1 to the inner comment count.
        """
        self.inner_comment_count += 1
        self.save()

    def remove_inner_comment(self):
        """
        Remove 1 from the inner comment count.
        """
        if self.inner_comment_count > 0:
            self.inner_comment_count -= 1
            self.save()


class InnerComment(models.Model):
    """
    Comment 's Inner Comments Model.
    """

    content = models.TextField(max_length=1024)
    created_time = models.DateTimeField(auto_now_add=True)
    like_count = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="inner_comments"
    )
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="inner_comments"
    )

    class Meta:
        """
        Default ordering by latest posts first.
        """

        ordering = ["-creat_time"]

    def __str__(self):
        """
        Returns the user name, comment id and the beginning of
        the content of the InnerComment.
        """
        return f"{self.user.name} on {self.comment.id}: {self.content[:25]}..."

    def like(self):
        """
        Add 1 to the like count.
        """
        self.like_count += 1
        self.save()

    def remove_like(self):
        """
        Remove 1 from the like count.
        """
        if self.like_count > 0:
            self.like_count -= 1
            self.save()
