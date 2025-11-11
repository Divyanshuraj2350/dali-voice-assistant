
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from voice_io import VoiceIO
from intent_handler import IntentHandler
from action_executor import ActionExecutor
import time

class Dali:
    def __init__(self):
        print("\n🔧 Initializing Dali...\n")
        self.voice = VoiceIO()
        self.intent = IntentHandler()
        self.action = ActionExecutor()
        self.is_running = True
        
        # Better wake words
        self.wake_words = [
            "hey dali", "dali", "dali wake up", "wake up dali",
            "dali is here", "hey daily", "hey dolly"
        ]
        
    def start(self):
        print("="*70)
        print("🤖 DALI - DYNAMIC AI LISTENING INTERFACE")
        print("="*70)
        print("\n💡 Wake words:")
        print("   • 'Hey Dali'")
        print("   • 'Dali wake up'")
        print("   • 'Dali is here'")
        print("\n📝 Examples:")
        print("   • 'Hey Dali, tell me a joke'")
        print("   • 'Dali wake up, what time is it'")
        print("   • 'Hey Dali, what is your full name'")
        print("\n" + "="*70 + "\n")
        
        # Greeting - WILL SPEAK
        self.voice.speak("Hello! I'm Dali. Say Hey Dali, then your command.")
        print("💡 Listening mode active...\n")
        
        while self.is_running:
            try:
                # Listen for voice input
                text = self.voice.listen()
                
                if not text:
                    continue
                
                # Check for wake word
                wake_detected = False
                detected_wake = None
                
                for wake in self.wake_words:
                    if wake in text:
                        wake_detected = True
                        detected_wake = wake
                        break
                
                if wake_detected:
                    # Remove wake word to get command
                    cmd = text.replace(detected_wake, "").strip()
                    
                    if not cmd:
                        self.voice.speak("Yes? I'm listening.")
                        continue
                    
                    print(f"✅ Command: '{cmd}'")
                    
                    # Classify intent
                    intent_type, data = self.intent.classify_intent(cmd)
                    print(f"🔍 Intent: {intent_type}")
                    
                    # Execute action and get response
                    response = self.action.execute_action(intent_type, data)
                    
                    # Check for exit
                    if response == "exit":
                        self.voice.speak("Goodbye! Have a great day!")
                        self.is_running = False
                        break
                    
                    # SPEAK THE RESPONSE (This is important!)
                    if response:
                        print(f"\n📢 Speaking: {response}")
                        self.voice.speak(response)
                    else:
                        self.voice.speak("I didn't get a response. Try again.")
                
                else:
                    print(f"⚠️ No wake word in: '{text}'")
                    print("💡 Please say 'Hey Dali' first\n")

            except KeyboardInterrupt:
                print("\n\n👋 Shutting down...")
                try:
                    self.voice.speak("Goodbye!")
                except:
                    pass
                self.is_running = False
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(1)
    
    def stop(self):
        """Stop the assistant"""
        self.is_running = False
