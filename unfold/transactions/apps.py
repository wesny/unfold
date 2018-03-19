from django.apps import AppConfig


class TransactionConfig(AppConfig):
    name = 'unfold.transactions'
    verbose_name = "Transactions"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
