from datetime import datetime, timedelta

class SpamProtector(object):
    """protects the bot from too many requests"""
    def __init__(self, ignore_period = 15, spam_window = 30, request_limit = 10):
        self.ignore_period = ignore_period
        self.spam_window = spam_window
        self.request_limit = request_limit

        
        self.requests = {}  # userid : request timestamps list
        self.ignored = {}   # userid : when we stop ignorinng them

    def ignore(self, user):
        """returns true if this user should be ignored and updates other information"""
        if user not in self.requests:
            return False

        if user in self.ignored:
            if datetime.now() > self.ignored[user]:
                del self.ignored[user]
                self.requests[user] = []
                return False
            return True

        else:
            earliest = datetime.now() - timedelta(seconds = self.spam_window)
            
            for index, time in enumerate(self.requests[user]):
                if time >= earliest:
                    self.requests[user] = self.requests[user][index:]
                    break

            if len(self.requests[user]) >= self.request_limit:
                self.ignored[user] = datetime.now() + timedelta(seconds = self.ignore_period)
                return True
            return False

    def log(self, user):
        """logs a request"""        
        if user in self.requests:
            self.requests[user].append(datetime.now())
        else:
            self.requests[user] = [datetime.now()]
