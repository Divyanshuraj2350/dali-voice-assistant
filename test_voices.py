import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

print("\n🎙️ Available Voices:\n")
for idx, voice in enumerate(voices):
    print(f"{idx}: {voice.name}")
    engine.setProperty('voice', voice.id)
    engine.say(f"Hello, I am voice number {idx}. This is how I sound.")
    engine.runAndWait()
    print()

print("\n✅ Test complete! Choose the voice number you prefer.")
