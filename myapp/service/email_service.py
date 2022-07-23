
from django.shortcuts import render
from django.template import Context
from django.template.loader import  get_template
from django.core.mail import EmailMessage

def send_mail_user(user_detail, user_id, request_session_id, host):
    if not user_detail.user and not user_detail.user.email:
        return
    ctx ={
        'user': user_detail.user,
        'user_id':str(user_id),
        'session_id':str(request_session_id),
        'host': host,
    }
    message = get_template('send_mail.html')
    rendered = message.render(ctx)
    

    msg = EmailMessage(
        'Subject',
        rendered,
        'ssoyansu@gmail.com.com',
        [user_detail.user.email],
    )
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
    print("Mail successfully sent : ", user_detail.user.email)
