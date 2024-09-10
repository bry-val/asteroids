class Score:
    _instance = None
    _observers = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.score = 0
        return cls._instance
    
    def register_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.scoreupdated(self.score)
    
    def increase_score(self, points):
        self.score += points
        self.notify_observers()
