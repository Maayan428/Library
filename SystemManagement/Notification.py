

class Notification:
    def __init__(self):
        self._observers = []
        self._messages = []

    def register_observer(self, observer):
        self._observers.append(observer)

    def unregister_observer(self, observer):
        self._observers.remove(observer)


    def notify_observers(self, message):
        self._messages.append(message)
        for observer in self._observers:
            try:
                observer.update(message)
            except Exception as e:
                print(f"Error notifying observer: {e}")

    def get_all_notifications(self):
        return self._messages