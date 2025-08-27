from django.apps import AppConfig


class TravelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'travel'

    def ready(self):
        # 移除对不存在的signals模块的导入
        pass
