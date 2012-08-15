from django.core.management.base import BaseCommand
from django.db.models import get_model

from easyrec.utils import get_gateway
from easyrec.receivers import EasyRecListeners

Order = get_model('order', 'Order')
listeners = EasyRecListeners(get_gateway())


class Command(BaseCommand):

    help = "Import all existing orders into EasyRec"

    def handle(self, *args, **options):
        self.stdout.write('Starting order import')
        self.stdout.write('Found %d orders to import', Order.objects.count())
        imported = 0
        skipped = 0
        for order in Order.objects.all():
            if order.is_anonymous:
                skipped += 1
                continue
            user = order.user
            listeners.on_order_placed(self, order, user)
            imported += 1
        self.stdout.write('Import completed (%d imports, %d skipped)',
            (imported, skipped))
