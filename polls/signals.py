from django.db.models.signals import m2m_changed , post_save
from django.dispatch import receiver
from .models import Choice , Poll , UserVotes


@receiver(m2m_changed , sender=Choice.users.through)
def users_changed(sender , instance , **kwargs):

	instance.total = instance.users.count()
	instance.save()


@receiver(m2m_changed , sender=Poll.users.through)
def poll_users_changed(sender , instance , **kwargs):

	instance.total = instance.users.count()
	instance.save()

	
	