from openai import OpenAI
import speech_recognition as sr
import pyttsx3
import sys
import json
import os
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT

load_dotenv()

class EggVoiceTerminal:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.client = OpenAI(
            api_key=os.environ.get('OPENAI_API_KEY'),
            base_url="https://api.deepseek.com"
        )
        
        # Configure voice settings
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)
        
    def speak(self, text):
        """Convert text to speech"""
        self.engine.say(text)
        self.engine.runAndWait()
        
    def listen(self):
        """Capture and transcribe user's voice input"""
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
            
        try:
            text = self.recognizer.recognize_google(audio)
            print(f"You: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that")
            return None
        except sr.RequestError:
            print("Speech recognition service unavailable")
            return None
            
    def send_to_egg(self, prompt):
        """Send prompt to Egg via Deepseek API"""
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1024,
                temperature=0.7,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error communicating with Egg: {str(e)}")
            return None
            
    def run(self):
        """Main conversation loop"""
        print("Egg Voice Terminal - Press Ctrl+C to exit")
        while True:
            try:
                # Get user input
                user_input = self.listen()
                if not user_input:
                    continue
                    
                # Get Egg's response
                response = self.send_to_egg(user_input)
                if response:
                    print(f"Egg: {response}")
                    self.speak(response)
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                sys.exit(0)

if __name__ == "__main__":
    terminal = EggVoiceTerminal()
    terminal.run()
