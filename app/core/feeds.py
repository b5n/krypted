from django_ical.views import ICalFeed
from core.models import Event

class EventFeed(ICalFeed):
    """
    A simple event calender
    """
    product_id = '-//example.com//Example//EN'
    timezone = 'UTC'
    file_name = "event.ics"

    def items(self):
        return Event.objects.all().order_by('-start_datetime')

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description

    def item_start_datetime(self, item):
        return item.start_datetime
