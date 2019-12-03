from django.apps import AppConfig

class BeaconConfig(AppConfig):
    name = 'beaconui'
    verbose_name = "Beacon Frontend"


default_app_config = 'beaconui.BeaconConfig'
