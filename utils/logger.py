import datetime

class Logger:
    def __init__(self, filename="astra_log.txt"):
        self.filename = filename

    def log(self, message, level="INFO"):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"[{timestamp}] [{level}] {message}\n"
        with open(self.filename, "a", encoding="utf-8") as file:
            file.write(formatted_message)

    def log_user_message(self, message):
        self.log(f"USER: {message}", level="USER")

    def log_ai_response(self, response):
        self.log(f"ASTRA: {response}", level="AI")