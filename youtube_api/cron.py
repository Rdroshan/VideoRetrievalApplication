# third party imports
from django_cron import CronJobBase, Schedule

# app level imports
from .models import YoutubeData

class YoutubeJob(CronJobBase):
    RUN_EVERY_MINS = 5 # every 5 minute

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.my_cron_job'    # a unique code

    def do(self):
    	pass






 