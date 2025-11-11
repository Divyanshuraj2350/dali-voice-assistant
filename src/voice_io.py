
import speech_recognition as sr
import pyttsx3
import time

class VoiceIO:
    def __init__(self):
        self.engine = pyttsx3.init('nsss')
        self.setup_voice()
        self.recognizer = sr.Recognizer()
        
        # IMPROVED settings for better recognition
        self.recognizer.energy_threshold = 2000  # Lower to catch more sounds
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.6  # Shorter pause between words
        self.recognizer.phrase_threshold = 0.1  # Lower threshold
        self.recognizer.non_speaking_duration = 0.3
        
    def setup_voice(self):
        try:
            voices = self.engine.getProperty('voices')
            # Find best voice
            preferred_voices = ['Samantha', 'Alex', 'Karen', 'Daniel']
            selected_voice = voices[0].id
            selected_name = voices[0].name
            
            for preferred in preferred_voices:
                for voice in voices:
                    if preferred.lower() in voice.name.lower():
                        selected_voice = voice.id
                        selected_name = voice.name
                        break
                if selected_voice != voices[0].id:
                    break
            
            self.engine.setProperty('voice', selected_voice)
            self.engine.setProperty('rate', 140)  # Slower for clarity
            self.engine.setProperty('volume', 1.0)
            
            print(f"✅ Voice: {selected_name}")
            print("✅ Speech Recognition Ready\n")
        except Exception as e:
            print(f"⚠️ Voice error: {e}")
        
    def speak(self, text):
        """SPEAK OUT LOUD with error handling"""
        try:
            print(f"\n🤖 Dali: {text}\n")
            
            # Actually speak the text
            self.engine.say(text)
            self.engine.runAndWait()
            
            time.sleep(0.5)
        except KeyboardInterrupt:
            self.engine.stop()
            raise
        except Exception as e:
            print(f"❌ Speak error: {e}")
    
    def listen(self, timeout=20, phrase_time_limit=15):
        """IMPROVED listening with better recognition"""
        try:
            with sr.Microphone() as source:
                print("🎤 Listening... (Speak now - clear and loud)")
                
                # Longer noise adjustment for better baseline
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                
                # Listen with extended timeout
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            
            print("🔄 Processing your speech...")
            
            # Try with Indian English first (your accent)
            try:
                text = self.recognizer.recognize_google(
                    audio,
                    language='en-IN',
                    show_all=False
                )
                print(f"✅ Recognized (IN): {text}\n")
                return text.lower()
            except sr.UnknownValueError:
                # Try with US English as backup
                try:
                    text = self.recognizer.recognize_google(
                        audio,
                        language='en-US',
                        show_all=False
                    )
                    print(f"✅ Recognized (US): {text}\n")
                    return text.lower()
                except:
                    raise sr.UnknownValueError()
            
        except sr.WaitTimeoutError:
            print("⏱️ Timeout - no speech detected\n")
            return ""
        except sr.UnknownValueError:
            print("❌ Couldn't understand - please speak more clearly\n")
            return ""
        except sr.RequestError as e:
            print(f"❌ Google API error: {e}\n")
            return ""
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(f"❌ Error: {e}\n")
            return ""
