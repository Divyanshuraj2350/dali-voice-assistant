
import speech_recognition as sr
import threading

class WakeWordDetector:
    """Continuous background listener for wake words"""
    
    def __init__(self, callback):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 2000
        self.recognizer.dynamic_energy_threshold = True
        self.callback = callback  # Called when wake word detected
        self.is_listening = False
        self.thread = None
        
        self.wake_words = [
            "dali", "hey dali", "hey darling", "darling",
            "dali wake up", "wake up dali", "dali is here",
            "hey daily", "daily"
        ]
    
    def start(self):
        """Start background listening"""
        if not self.is_listening:
            self.is_listening = True
            self.thread = threading.Thread(target=self._listen_loop, daemon=True)
            self.thread.start()
            print("🎙️ Background listener started")
    
    def stop(self):
        """Stop background listening"""
        self.is_listening = False
        print("🎙️ Background listener stopped")
    
    def _listen_loop(self):
        """Continuous listening loop"""
        while self.is_listening:
            try:
                with sr.Microphone() as source:
                    # Shorter listening for wake word detection
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    
                    # Listen for short phrases only
                    try:
                        audio = self.recognizer.listen(
                            source,
                            timeout=2,  # Short timeout
                            phrase_time_limit=2  # Short phrase
                        )
                    except sr.WaitTimeoutError:
                        continue
                
                # Try to recognize - very quick
                try:
                    text = self.recognizer.recognize_google(
                        audio,
                        language='en-IN'
                    )
                    text = text.lower()
                    
                    # Check for wake word
                    for wake in self.wake_words:
                        if wake in text:
                            print(f"✅ Wake word detected: '{wake}'")
                            self.callback(text)  # Call the callback
                            break
                            
                except:
                    pass
                    
            except Exception as e:
                pass

