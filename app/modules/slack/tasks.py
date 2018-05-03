from __future__ import absolute_import, unicode_literals
from celery import task
from django.contrib.auth.models import Group, User
from django.conf import settings
from modules.slack.models import *
import requests, json, logging
logger = logging.getLogger(__name__)

class RateLimitException(Exception):
    pass

@task()
def sync_slack_users():
    logger.info("Syncing slack users")
    for user in User.objects.all():
        try:
            slack_user = SlackUser.objects.get(user=user)
            logger.info("Retrieved slack user for %s" % user.pk)
        except Exception as e:
            slack_user = None
            logger.info("Searching for slack user %s: %s" % (user.pk, e))
            get_slack_user.apply_async(args=[user.pk])

        if slack_user:
            for group in slack_user.user.groups.all():
                if SlackChannel.objects.filter(groups__name__in=[group]).exists():
                    slack_channels = SlackChannel.objects.filter(groups__name__in=[group])
                    for slack_channel in slack_channels:
                        add_slack_user_to_channel.apply_async(args=[slack_channel.slack_id, slack_user.slack_id])

@task(bind=True)
def add_slack_user(self, user):
    """
    Expects an Authentication User
    """
    user = User.objects.get(pk=user)
    logger.info("Inviting %s to Slack" % user.email)
    url = settings.SLACK_BASE_URL + "users.admin.invite"
    data = {
            'token': settings.SLACK_LEGACY_TOKEN,
            'email': user.email
    }
    response = requests.put(url=url, data=data)
    if response.status_code == 429:
        raise RateLimitException
    elif response.status_code == 200:
        logger.info(response.json())

@task(bind=True)
def get_slack_user(self, user):
    """
    Expects an Authentication User
    """
    user = User.objects.get(pk=user)
    logger.info("Getting slack user %s" % user.username)
    url = settings.SLACK_BASE_URL + "users.lookupByEmail"
    data = {
            'token': settings.SLACK_TOKEN,
            'email': user.email
    }
    response = requests.put(url=url, data=data)
    if response.status_code == 429:
        raise RateLimitException
    elif response.status_code == 200:
        logger.info("Success with %s" % response.json())
        slack_user = SlackUser(slack_id=response.json()['user']['id'], user=user)
        slack_user.save()

@task(bind=True)
def add_slack_channel(self, channel, groups=None):
    """
    Expects a string 'channel' for the channel name
    Expects groups string seperated by -
    """
    logger.info("Creating Slack channel: %s" % channel)
    if groups:
        raw_groups = groups.split("-")
        groups = []
        url = settings.SLACK_BASE_URL + "groups.create"
        for group in raw_groups:
            groups.append(Group.objects.get(pk=group))

    else:
        url = settings.SLACK_BASE_URL + "channels.create"
    data = {
            'token': settings.SLACK_TOKEN,
            'name': channel
    }
    response = requests.put(url=url, data=data)
    if response.status_code == 429:
        raise RateLimitException
    elif response.status_code == 200:
        if groups:
            slack_channel = SlackChannel(slack_id=response.json()['group']['id'], name=channel)
            slack_channel.save()
            slack_channel.groups.set(groups)
        else:
            slack_channel = SlackChannel(slack_id=response.json()['channel']['id'], name=channel)
            slack_channel.save()
        logger.info(response.json())

@task(bind=True)
def add_slack_user_to_channel(self, channel, user):
    """
    Expects a slack channel and user ID
    """
    logger.info("Adding user %s to slack channel %s" % (channel, user))
    channel = SlackChannel.objects.get(slack_id=channel)
    if channel.groups.all():
        url = settings.SLACK_BASE_URL + "groups.invite"
    else:
        url = settings.SLACK_BASE_URL + "channels.invite"
    data = {
            'token': settings.SLACK_TOKEN,
            'channel': channel.slack_id,
            'user': user
    }
    response = requests.put(url=url, data=data)
    if response.status_code == 429:
        raise RateLimitException
    elif response.status_code == 200:
        logger.info(response.json())

@task(bind=True)
def remove_slack_user_from_channel(self, channel, user):
    """
    Expects a slack channel and user ID
    """
    logger.info("Removing user %s from slack channel %s" % (channel, user))
    channel = SlackChannel.objects.get(slack_id=channel)
    if channel.groups.all():
        url = settings.SLACK_BASE_URL + "groups.kick"
    else:
        url = settings.SLACK_BASE_URL + "channels.kick"
    data = {
            'token': settings.SLACK_TOKEN,
            'channel': channel.slack_id,
            'user': user
    }
    response = requests.put(url=url, data=data)
    if response.status_code == 429:
        raise RateLimitException
    elif response.status_code == 200:
        logger.info(response.json())