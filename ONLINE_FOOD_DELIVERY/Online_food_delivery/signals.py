from django.dispatch import Signal,receiver
from OrderingOnline.models import alert

#signal
notifications = Signal(providing_args=['request','order'])


#reciver
@receiver(notifications)
def show_notification(sender, **kwargs):
    print(sender)
    print(f'{kwargs}')
    print(kwargs['order'])
    order=kwargs['order']
    print(order[0].Item)
    print(order[0].user)
    user=order[0].user
    order_feedback=order[0].id
    notification_=alert(user=user,notification_id=order_feedback)
    notification_.save()
    