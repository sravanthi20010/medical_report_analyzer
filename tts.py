import pyttsx3
import time

def speak(text):
    try:
        engine = pyttsx3.init()
        
        # Configure voice settings
        voices = engine.getProperty('voices')
        if voices:
            # Try to use a female voice if available
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
        
        # Set speech rate (words per minute)
        engine.setProperty('rate', 180)  # Slightly slower for clarity
        
        # Set volume
        engine.setProperty('volume', 0.8)
        
        print(f"🎤 Speaking text: {text[:50]}...")
        engine.say(text)
        engine.runAndWait()
        print("✅ Speech completed")
        
    except Exception as e:
        print(f"❌ TTS Error: {str(e)}")
        # Fallback: try to use system text-to-speech
        try:
            import os
            if os.name == 'nt':  # Windows
                os.system(f'powershell -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{text.replace(chr(39), chr(34))}\')"')
            else:
                print("TTS not available on this system")
        except:
            print("Fallback TTS also failed")