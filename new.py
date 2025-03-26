from datetime import datetime
import math
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha
import keyboard
import threading
import pygame
import time
import os
from tkinter import *
from tkinter import ttk, scrolledtext, messagebox, simpledialog
from PIL import Image, ImageTk
from dotenv import load_dotenv
import google.cloud.texttospeech as tts

# Load environment variables
load_dotenv()

class VoiceAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("JELIL - Voice Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a')
        
        # Configuration
        self.activation_words = ['computer', 'Jelil', 'shodan', 'showdown']
        self.tts_type = 'local'  # Change to 'google' for cloud TTS
        self.appId = '5R49J7-J888YX9J2V'
        self.wolframClient = wolframalpha.Client(self.appId)
        
        # Initialize components
        self.setup_tts()
        self.setup_browser()
        self.create_widgets()
        self.update_status("All systems nominal")
        
        # State variables
        self.listening = False
        self.is_speaking = False

    def setup_tts(self):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.engine.setProperty('rate', 150)
        
    def setup_browser(self):
        firefox_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"
        webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(firefox_path))

    def create_widgets(self):
        # Main container
        main_frame = Frame(self.root, bg='#1a1a1a')
        main_frame.pack(expand=True, fill=BOTH, padx=10, pady=10)

        # Header
        header_frame = Frame(main_frame, bg='#1a1a1a')
        header_frame.pack(fill=X)
        
        try:
            self.logo_img = ImageTk.PhotoImage(Image.open("ai_icon.png").resize((60,60)))
            Label(header_frame, image=self.logo_img, bg='#1a1a1a').pack(side=LEFT, padx=5)
        except FileNotFoundError:
            pass
        
        Label(header_frame, text="JELIL", font=('Impact', 28), 
             fg='#00ff99', bg='#1a1a1a').pack(side=LEFT, padx=10)

        # Conversation history
        self.history_text = scrolledtext.ScrolledText(main_frame, wrap=WORD,
                                                    font=('Consolas', 12),
                                                    bg='#000000', fg='#00ff99',
                                                    insertbackground='white')
        self.history_text.pack(expand=True, fill=BOTH, pady=10)
        self.history_text.configure(state='disabled')

        # Controls
        control_frame = Frame(main_frame, bg='#1a1a1a')
        control_frame.pack(fill=X, pady=5)
        
        self.mic_img = self.create_icon_button("mic_icon.png")
        self.mic_btn = Button(control_frame, image=self.mic_img, command=self.toggle_listening,
                             bg='#2d2d2d', activebackground='#404040', bd=0)
        self.mic_btn.pack(side=LEFT, padx=5)

        self.input_entry = ttk.Entry(control_frame, width=50, font=('Arial', 12))
        self.input_entry.pack(side=LEFT, expand=True, fill=X, padx=5)
        self.input_entry.bind('<Return>', self.process_text_input)

        ttk.Button(control_frame, text="Send", command=self.process_text_input).pack(side=LEFT)

        # Status bar
        self.status_bar = Label(self.root, text="Ready", bd=1, relief=SUNKEN,
                              anchor=W, fg='#00ff99', bg='#2d2d2d', font=('Arial', 10))
        self.status_bar.pack(side=BOTTOM, fill=X)

    def create_icon_button(self, icon_path):
        try:
            img = Image.open(icon_path).resize((30,30))
            return ImageTk.PhotoImage(img)
        except FileNotFoundError:
            return ImageTk.PhotoImage(Image.new('RGB', (30,30), color='#2d2d2d'))

    def update_status(self, message):
        self.status_bar.config(text=message)
        self.root.update()

    def toggle_listening(self):
        if not self.listening:
            self.listening = True
            self.mic_btn.config(bg='#cc0000', activebackground='#ff4444')
            threading.Thread(target=self.process_voice_input, daemon=True).start()
        else:
            self.listening = False
            self.mic_btn.config(bg='#2d2d2d', activebackground='#404040')

    def process_voice_input(self):
        self.update_history("System", "Listening...", "#0099ff")
        query = self.recognize_speech()
        # Update GUI state after processing
        self.root.after(0, self.set_listening_false)
        if query:
            self.root.after(0, self.update_history, "User", query, "#00ff99")
            self.root.after(0, self.process_command, query.lower().split())

    def set_listening_false(self):
        self.listening = False
        self.mic_btn.config(bg='#2d2d2d', activebackground='#404040')

    def process_text_input(self, event=None):
        text = self.input_entry.get()
        if text:
            self.input_entry.delete(0, END)
            self.update_history("User", text, "#00ff99")
            self.process_command(text.lower().split())

    def recognize_speech(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = None
            while self.listening:
                try:
                    # Listen for a short duration to allow checking the listening state
                    audio = recognizer.listen(source, timeout=0.5, phrase_time_limit=5)
                    break  # Exit loop if audio captured
                except sr.WaitTimeoutError:
                    continue  # Continue listening while self.listening is True
            if audio:
                try:
                    return recognizer.recognize_google(audio, language='en_gb')
                except sr.UnknownValueError:
                    self.update_history("System", "Could not understand audio", "#ff4444")
                except sr.RequestError as e:
                    self.update_history("System", f"Recognition error: {e}", "#ff4444")
            return None

    def update_history(self, sender, message, color):
        self.history_text.configure(state='normal')
        self.history_text.insert(END, f"{sender}: ", (sender, color))
        self.history_text.insert(END, f"{message}\n")
        self.history_text.tag_config(sender, foreground=color)
        self.history_text.configure(state='disabled')
        self.history_text.see(END)
        self.root.update()

    def speak(self, text, rate=120):
        self.update_history("Assistant", text, "#0099ff")
        if self.tts_type == 'local':
            self.engine.setProperty('rate', rate)
            self.engine.say(text)
            self.engine.runAndWait()
        elif self.tts_type == 'google':
            self.google_tts(text)

    def google_tts(self, text):
        try:
            audio_content = google_text_to_wav('en-US-News-K', text)
            pygame.mixer.init()
            sound = pygame.mixer.Sound(audio_content)
            sound.play()
            while pygame.mixer.get_busy():
                time.sleep(0.1)
            pygame.mixer.quit()
        except Exception as e:
            self.update_history("System", f"TTS Error: {e}", "#ff4444")

    def process_command(self, query):
        try:
            if not query:
                return

            if query[0] in self.activation_words and len(query) > 1:
                query.pop(0)

            if query[0] == 'say':
                self.speak(' '.join(query[1:]))

            elif query[0] == 'go' and query[1] == 'to':
                self.open_website(' '.join(query[2:]))

            elif query[0] == 'wikipedia':
                self.search_wikipedia(' '.join(query[1:]))

            elif query[0] in ('compute', 'computer'):
                self.wolfram_alpha_query(' '.join(query[1:]))

            elif query[0] == 'log':
                self.create_note()

            elif query[0] == 'exit':
                self.root.destroy()

        except Exception as e:
            self.update_history("System", f"Command error: {e}", "#ff4444")

    def open_website(self, url):
        try:
            if not url.startswith(('http://', 'https://')):
                url = f'https://{url.replace(" ", "")}'
            url = url.replace(".org", ".com").replace(" ", "-")
            webbrowser.get('firefox').open_new(url)
            self.speak(f"Opening {url}")
        except Exception as e:
            self.speak(f"Failed to open {url}")
            self.update_history("System", f"Browser error: {e}", "#ff4444")

    def search_wikipedia(self, query):
        try:
            self.update_status("Searching Wikipedia...")
            result = wikipedia.summary(query, sentences=3)
            self.speak(result)
        except Exception as e:
            self.speak("No Wikipedia results found")
            self.update_history("System", f"Wikipedia error: {e}", "#ff4444")

    def wolfram_alpha_query(self, query):
        try:
            res = self.wolframClient.query(query)
            if res['@success'] == 'false':
                self.speak("Unable to compute")
            else:
                result = next(res.results).text
                self.speak(result)
        except Exception as e:
            self.speak("Computation failed")
            self.update_history("System", f"Wolfram error: {e}", "#ff4444")

    def create_note(self):
        try:
            # Ask user if they want to type or speak
            response = messagebox.askyesno("Note Type", "Type note instead of speaking?")
            
            if response:  # Text input
                note = simpledialog.askstring("Text Note", "Enter your note:")
                if not note:
                    return
            else:  # Voice input
                self.speak("Ready to record your note")
                note = self.recognize_speech()

            if note:
                os.makedirs("notes", exist_ok=True)
                filename = f"notes/note_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(filename, 'w') as f:
                    f.write(note)
                self.speak("Note saved successfully")
                self.update_history("System", f"Note saved to {filename}", "#00ff99")
            else:
                self.speak("No note content detected")

        except Exception as e:
            self.update_history("System", f"Note error: {str(e)}", "#ff4444")
            self.speak("Failed to save note")
    

def google_text_to_wav(voice_name: str, text: str):
    client = tts.TextToSpeechClient()
    input_text = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code="-".join(voice_name.split("-")[:2]),
        name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)
    return client.synthesize_speech(
        input=input_text, voice=voice_params, audio_config=audio_config
    ).audio_content

if __name__ == '__main__':
    root = Tk()
    gui = VoiceAssistantGUI(root)
    root.mainloop()