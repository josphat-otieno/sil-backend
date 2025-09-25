from .sms import send_customer_sms
from .emailer import send_admin_email
from orders.models import Order

def notify_order_placed(order_id: int):
    order = Order.objects.select_related('customer').prefetch_related('items__product').get(pk=order_id)
    if order.customer and order.customer.phone:
        send_customer_sms(order.customer.phone, f"Your order #{order.id} has been placed. Total: {order.total}.")
    else:
        print("[SMS MOCK] No phone on customer; skipping SMS.")
    items = "\n".join([f"- {i.quantity} x {i.product.name} @ {i.price}" for i in order.items.all()])
    send_admin_email(subject=f"[Orders] New Order #{order.id}", body=f"Customer: {order.customer.email}\nTotal: {order.total}\nItems:\n{items}")
