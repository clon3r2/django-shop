from django.core.management import BaseCommand, CommandError
from apps.customer.models import Customer


class Command(BaseCommand):
    help = 'deactivates a customer'

    def add_arguments(self, parser):
        parser.add_argument('-p', '--phone', type=str, help='customer phone number')

    def handle(self, *args, **options):
        phone = options['phone']
        try:
            customer = Customer.objects.get(user__phone=phone)
            customer.is_active = False
            customer.save()
            self.stdout.write(self.style.SUCCESS(f'user {phone} deactivated successfully'))
        except Customer.DoesNotExist:
            raise CommandError(f'Customer {phone} does not exist')
