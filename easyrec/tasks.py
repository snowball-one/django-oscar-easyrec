from celery import task

from easyrec import utils

gateway = utils.get_gateway()

@task
def add_view(*args, **kwargs):
   return gateway.add_view(*args, **kwargs)

@task
def add_buy(*args, **kwargs):
   return gateway.add_buy(*args, **kwargs)

@task
def add_rating(*args, **kwargs):
   return gateway.add_rating(*args, **kwargs)
