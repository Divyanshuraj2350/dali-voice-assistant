
import re

class IntentHandler:
    def __init__(self):
        self.context = {}
        
    def classify_intent(self, text):
        text = text.lower()
        
        # Full name query - NEW!
        if any(phrase in text for phrase in ['full name', 'your name', 'what is your name', 'who are you']):
            return 'full_name', None
        
        # Weather
        elif any(word in text for word in ['weather', 'temperature']):
            return 'weather', None
        
        # Music
        elif any(word in text for word in ['play', 'music', 'song']):
            return 'music', self.extract_song(text)
        
        # Reminder
        elif 'remind' in text:
            return 'reminder', text
        
        # Time
        elif any(word in text for word in ['time', 'clock']):
            return 'time', None
        
        # Date
        elif 'date' in text or 'today' in text:
            return 'date', None
        
        # Search
        elif any(word in text for word in ['search', 'find', 'google']):
            return 'search', self.extract_search(text)
        
        # Open app
        elif 'open' in text:
            return 'open', self.extract_app(text)
        
        # Greeting
        elif any(word in text for word in ['hello', 'hi', 'hey']):
            return 'greeting', None
        
        # Wikipedia
        elif 'tell me about' in text or 'wikipedia' in text or 'who is' in text:
            return 'wikipedia', self.extract_wiki(text)
        
        # Joke
        elif 'joke' in text or 'funny' in text:
            return 'joke', None
        
        # Exit
        elif any(word in text for word in ['exit', 'quit', 'bye', 'goodbye', 'stop']):
            return 'exit', None
        
        else:
            return 'unknown', None
    
    def extract_song(self, text):
        for pattern in [r'play (.+)', r'music (.+)']:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return 'music'
    
    def extract_search(self, text):
        for prefix in ['search for', 'search', 'find', 'google']:
            if prefix in text:
                return text.split(prefix, 1)[1].strip()
        return text
    
    def extract_app(self, text):
        return text.replace('open', '').strip()
    
    def extract_wiki(self, text):
        for phrase in ['tell me about', 'wikipedia', 'who is', 'what is']:
            if phrase in text:
                return text.split(phrase, 1)[1].strip()
        return text
