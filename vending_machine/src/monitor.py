class Monitor():
    
    def __init__(self):
        self.display_log = []

    def display(self, text: str):
        self.display_log.append(text)
        print(text)
