from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Video
import django_rq
from .tasks import process_video


@receiver(post_save, sender=Video)
def video_upload_handler(sender, instance, created, **kwargs):
    """Automatisch Videoverarbeitungs-Task in die RQ-Warteschlange stellen."""
    if created and instance.video_file:
        instance.refresh_from_db()
        queue = django_rq.get_queue('default')
        queue.enqueue(process_video, instance.id)
