from django.db import models
from django.contrib.auth.models import User, AbstractUser


class Poll(models.Model):
    """
    Represents a poll created by a superuser.

    Attributes:
        created_by (User): The admin user who created the poll.
        title (str): The title of the poll.
        description (str): A detailed description of the poll.
        is_active (bool): Indicates whether the poll is active.
        created_at (datetime): The timestamp when the poll was created.
        expires_at (datetime): The optional expiration date of the poll.    
    """
    created_by = models.ForeignKey(User,  limit_choices_to={'is_superuser': True},on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title 

class Option(models.Model):
    """
    Represents an option in a poll.

    Attributes:
        poll (Poll): The poll to which the option belongs.
        label (str): The text of the option.
    """
    poll = models.ForeignKey(Poll, related_name="options", on_delete=models.CASCADE)
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label

class Vote(models.Model):
    """
    Represents a user's vote for a specific option in a poll.

    Attributes:
        user (User): The user who cast the vote.
        option (Option): The chosen option.
        poll (Poll): The poll in which the vote was cast.
    Constraints:

        A user can vote only once per poll (unique_together: user, poll).
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, related_name="votes", on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, related_name="votes", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'poll')