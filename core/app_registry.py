class AppRegistry:
    def __init__(self):
        self.apps = {}

    def register(
        self,
        app_id,
        name,
        icon,
        window_class,
        single_instance=True
    ):
        self.apps[app_id] = {
            "id": app_id,
            "name": name,
            "icon": icon,
            "window": window_class,
            "single_instance": single_instance
        }

    def get(self, app_id):
        return self.apps.get(app_id)

    def all(self):
        return list(self.apps.values())