from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.core.mail import send_mail


if not post_save.receivers:
    @receiver(post_save, sender='posts.Comment')
    def post_save_comment(sender, instance, created, **kwargs):

        if not created:
            return

        comment = instance

        if not comment.post:
            return
        
        if comment.author == comment.post.author:
            return
        
        context = {
            'post_content': comment.post.content,
            'comment_content': comment.content,
            'user_name': comment.author.first_name,
        }

        html = render_to_string('emails/post_comment_received.html', context)

        send_mail(
            _('Your comment received a comment'),
            html,
            'no_reply@mail.com',
            [str(comment.post.author.email)],
        )