from django.core.mail import send_mail
from django.conf import settings

def send_admin_email(order, items):
    subject = f"New Order #{order.pk} from {order.customer}"
    body_lines = [
        f"Customer: {order.customer}",
        f"Total: {order.total}",
        f"Created at: {order.created_at}",
        "",
        "Items:"
    ]
    for item in items:
        body_lines.append(f"- {item.product.name} x {item.quantity} @ {item.price}")
    body = "\n".join(body_lines)
    try:

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )

    except Exception as e:
        pass
