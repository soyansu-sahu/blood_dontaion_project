
from django.template import Context
from django.template.loader import  get_template
from django.core.mail import EmailMessage



# msg_plain = render_to_string('send_mail.txt', {'some_params': some_params})
# msg_html = render_to_string('send_mail.html', {'user_name': user_name})

# send_mail(
#     'email title',
#     msg_plain,
#     'some@sender.com',
#     ['some@receiver.com'],
#     html_message=msg_html,
# )


def send_mail_user(request, user_detail):
    print(str(user_detail.user.email))
    if not user_detail.user and not user_detail.user.email:
        return
    ctx ={
        'user': user_detail.user
    }
    message = get_template('send_mail.html')
    rendered = message.render(ctx)
    print(message)
    msg = EmailMessage(
        'Subject',
        rendered,
        'ssoyansu@gmail.com.com',
        [user_detail.user.email],
    )
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
    print("Mail successfully sent")
