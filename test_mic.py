import speech_recognition as sr

print("\n🎤 MICROPHONE TEST")
print("="*50)

recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True

print("\n1. Testing microphone detection...")
try:
    mic_list = sr.Microphone.list_microphone_names()
    print(f"✅ Found {len(mic_list)} microphone(s)")
    for i, mic in enumerate(mic_list):
        print(f"   {i}: {mic}")
except Exception as e:
    print(f"❌ Error: {e}")
    exit()

print("\n2. Testing speech recognition...")
print("   Say something when you see 'Speak now!'")

try:
    with sr.Microphone() as source:
        print("   Adjusting for noise... (please wait)")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("   ✅ Ready! Speak now...")
        
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
        
    print("   Processing...")
    
    # Try both US and Indian English
    try:
        text = recognizer.recognize_google(audio, language='en-US')
        print(f"   ✅ SUCCESS (US English): '{text}'")
    except:
        text = recognizer.recognize_google(audio, language='en-IN')
        print(f"   ✅ SUCCESS (Indian English): '{text}'")
        
    print("\n✅ Microphone is working perfectly!")
    
except sr.WaitTimeoutError:
    print("   ❌ No speech detected - check your microphone")
except sr.UnknownValueError:
    print("   ❌ Couldn't understand - speak more clearly")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*50)
