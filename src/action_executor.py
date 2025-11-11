import webbrowser
import subprocess
from datetime import datetime
import random

class ActionExecutor:
    def __init__(self):
        self.reminders = []
        
    def execute_action(self, intent, data):
        actions = {
            'full_name': lambda data=None: self.get_full_name(),  # NEW!
            'weather': lambda data=None: self.get_weather(),
            'music': lambda data: self.play_music(data),
            'reminder': lambda data: self.set_reminder(data),
            'time': lambda data=None: self.get_time(),
            'date': lambda data=None: self.get_date(),
            'search': lambda data: self.web_search(data),
            'open': lambda data: self.open_app(data),
            'greeting': lambda data=None: self.greet(),
            'wikipedia': lambda data: self.get_wikipedia(data),
            'joke': lambda data=None: self.tell_joke(),
            'exit': lambda data=None: 'exit'
        }
        action = actions.get(intent, lambda data=None: "I'm not sure how to help with that.")
        return action(data)
    
    def get_full_name(self):
        """NEW: Return full name"""
        return "My full name is Dynamic AI Listening Interface. But you can call me Dali!"
    
    def get_weather(self):
        responses = [
            "It's a beautiful day!",
            "It's sunny outside!",
            "The weather is perfect today!"
        ]
        return random.choice(responses)
    
    def play_music(self, song):
        try:
            webbrowser.open(f"https://open.spotify.com/search/{song}")
            return f"Playing {song} on Spotify."
        except:
            return "Sorry, could not open Spotify."
    
    def set_reminder(self, task):
        return f"Reminder set for: {task}"
    
    def get_time(self):
        return f"The time is {datetime.now().strftime('%I:%M %p')}."
    
    def get_date(self):
        return f"Today is {datetime.now().strftime('%B %d, %Y')}."
    
    def web_search(self, query):
        try:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return f"Searching Google for: {query}"
        except:
            return "Sorry, I cannot open the web browser."
    
    def open_app(self, app_name):
        try:
            subprocess.run(['open', '-a', app_name])
            return f"Opening {app_name}."
        except:
            return f"Sorry, I couldn't open {app_name}."
    
    def greet(self):
        hour = datetime.now().hour
        if hour < 12:
            return "Good morning!"
        elif hour < 18:
            return "Good afternoon!"
        else:
            return "Good evening!"
    
    def get_wikipedia(self, query):
        try:
            import wikipedia
            return wikipedia.summary(query, sentences=2)
        except:
            return "Sorry, I couldn't find information about that."
    
    def tell_joke(self):
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
            "Why do Java developers wear glasses? Because they can't C sharp!"
        ]
        return random.choice(jokes)
