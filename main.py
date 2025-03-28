from datetime import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha
import threading
import time
import os
from tkinter import *
from tkinter import ttk, scrolledtext, messagebox, simpledialog
from PIL import Image, ImageTk
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ModernButton(Button):
    # Custom button class with modern styling and hover effects
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(
            bg='#2d2d2d',
            fg='#00ff99',
            activebackground='#404040',
            activeforeground='#00ff99',
            relief=FLAT,
            font=('Helvetica', 10, 'bold'),
            padx=15,
            pady=5
        )
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

    def on_enter(self, e):
        self.config(background='#404040')

    def on_leave(self, e):
        self.config(background='#2d2d2d')

class VoiceAssistantGUI:
    # Main GUI class for the voice assistant application
    def __init__(self, root):
        self.root = root
        self.root.title("JELIL - Voice Assistant")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1a1a1a')
        
        # Configuration
        self.activation_words = ['computer', 'Jelil']
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

    # Initialize text-to-speech engine with voice settings
    def setup_tts(self):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.engine.setProperty('rate', 150)
        
    # Configure Firefox as the default web browser
    def setup_browser(self):
        firefox_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"
        webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(firefox_path))

    # Create and configure all GUI widgets and layout
    def create_widgets(self):
        # Main container with gradient effect
        main_frame = Frame(self.root, bg='#1a1a1a')
        main_frame.pack(expand=True, fill=BOTH, padx=20, pady=20)

        # Header with modern design
        header_frame = Frame(main_frame, bg='#1a1a1a')
        header_frame.pack(fill=X, pady=(0, 20))
        
        try:
            self.logo_img = ImageTk.PhotoImage(Image.open("./assets/ai_icon.png").resize((80,80)))
            logo_label = Label(header_frame, image=self.logo_img, bg='#1a1a1a')
            logo_label.pack(side=LEFT, padx=10)
        except FileNotFoundError:
            pass
        
        title_frame = Frame(header_frame, bg='#1a1a1a')
        title_frame.pack(side=LEFT, padx=10)
        
        Label(title_frame, text="JELIL", font=('Impact', 36), 
             fg='#00ff99', bg='#1a1a1a').pack(side=LEFT)
        
        Label(title_frame, text="AI Assistant", font=('Helvetica', 14),
             fg='#888888', bg='#1a1a1a').pack(side=LEFT, padx=10)

        # Conversation history with modern styling
        history_frame = Frame(main_frame, bg='#2d2d2d', padx=10, pady=10)
        history_frame.pack(expand=True, fill=BOTH, pady=(0, 20))
        
        self.history_text = scrolledtext.ScrolledText(
            history_frame,
            wrap=WORD,
            font=('Consolas', 12),
            bg='#1a1a1a',
            fg='#00ff99',
            insertbackground='white',
            padx=10,
            pady=10
        )
        self.history_text.pack(expand=True, fill=BOTH)
        self.history_text.configure(state='disabled')

        # Controls with modern design
        control_frame = Frame(main_frame, bg='#1a1a1a')
        control_frame.pack(fill=X, pady=10)
        
        # Create a container for the input area with rounded corners
        input_container = Frame(control_frame, bg='#2d2d2d', padx=15, pady=10)
        input_container.pack(fill=X, expand=True)
        
        # Microphone button with modern styling
        self.mic_img = self.create_icon_button("./assets/mic_icon.png")
        self.mic_btn = ModernButton(
            input_container,
            image=self.mic_img,
            command=self.toggle_listening,
            width=45,
            height=45,
            borderwidth=0
        )
        self.mic_btn.pack(side=LEFT, padx=(0, 10))

        # Modern entry field with improved styling
        entry_frame = Frame(input_container, bg='#2d2d2d')
        entry_frame.pack(side=LEFT, expand=True, fill=X, padx=5)
        
        self.input_entry = Entry(
            entry_frame,
            width=50,
            font=('Helvetica', 12),
            bg='#1a1a1a',
            fg='#00ff99',
            insertbackground='#00ff99',
            relief=FLAT,
            highlightthickness=1,
            highlightbackground='#404040',
            highlightcolor='#00ff99'
        )
        self.input_entry.pack(side=LEFT, expand=True, fill=X)
        self.input_entry.bind('<Return>', self.process_text_input)
        
        # Placeholder text
        self.input_entry.insert(0, "Type your message or use voice command...")
        self.input_entry.bind('<FocusIn>', lambda e: self.on_entry_click())
        self.input_entry.bind('<FocusOut>', lambda e: self.on_focus_out())

        # Send button with modern styling
        send_btn = ModernButton(
            input_container,
            text="Send",
            command=self.process_text_input,
            width=10,
            height=2,
            font=('Helvetica', 11, 'bold')
        )
        send_btn.pack(side=LEFT, padx=(10, 0))

        # Status bar with modern design
        self.status_bar = Label(
            self.root,
            text="Ready",
            bd=0,
            relief=FLAT,
            anchor=W,
            fg='#00ff99',
            bg='#2d2d2d',
            font=('Helvetica', 10),
            padx=10,
            pady=5
        )
        self.status_bar.pack(side=BOTTOM, fill=X)

    # Create and return an icon button from image file
    def create_icon_button(self, icon_path):
        try:
            img = Image.open(icon_path).resize((30,30))
            return ImageTk.PhotoImage(img)
        except FileNotFoundError:
            return ImageTk.PhotoImage(Image.new('RGB', (30,30), color='#2d2d2d'))

    # Update the status bar message
    def update_status(self, message):
        self.status_bar.config(text=message)
        self.root.update()

    # Toggle voice input listening state
    def toggle_listening(self):
        if not self.listening:
            self.listening = True
            self.mic_btn.config(bg='#cc0000', activebackground='#ff4444')
            threading.Thread(target=self.process_voice_input, daemon=True).start()
        else:
            self.listening = False
            self.mic_btn.config(bg='#2d2d2d', activebackground='#404040')

    # Process voice input from microphone
    def process_voice_input(self):
        self.update_history("System", "Listening...", "#0099ff")
        query = self.recognize_speech()
        # Update GUI state after processing
        self.root.after(0, self.set_listening_false)
        if query:
            self.root.after(0, self.update_history, "User", query, "#00ff99")
            self.root.after(0, self.process_command, query.lower().split())

    # Reset listening state and button appearance
    def set_listening_false(self):
        self.listening = False
        self.mic_btn.config(bg='#2d2d2d', activebackground='#404040')

    # Process text input from entry field
    def process_text_input(self, event=None):
        text = self.input_entry.get()
        if text:
            self.input_entry.delete(0, END)
            self.update_history("User", text, "#00ff99")
            self.process_command(text.lower().split())

    # Recognize speech from microphone using Google Speech Recognition
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

    # Update the conversation history with new messages
    def update_history(self, sender, message, color):
        self.history_text.configure(state='normal')
        self.history_text.insert(END, f"{sender}: ", (sender, color))
        self.history_text.insert(END, f"{message}\n")
        self.history_text.tag_config(sender, foreground=color)
        self.history_text.configure(state='disabled')
        self.history_text.see(END)
        self.root.update()

    # Convert text to speech and speak it
    def speak(self, text, rate=120):
        self.update_history("Assistant", text, "#0099ff")
        self.engine.setProperty('rate', rate)
        self.engine.say(text)
        self.engine.runAndWait()

    # Process and execute user commands
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

            elif query[0] == 'google':
                self.google_search(' '.join(query[1:]))

            elif query[0] in ('compute', 'computer'):
                self.wolfram_alpha_query(' '.join(query[1:]))

            elif query[0] == 'log':
                self.create_note()

            elif query[0] == 'exit':
                self.root.destroy()

        except Exception as e:
            self.update_history("System", f"Command error: {e}", "#ff4444")

    # Open a website in the default browser
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

    # Search Wikipedia and speak the summary
    def search_wikipedia(self, query):
        try:
            self.update_status("Searching Wikipedia...")
            result = wikipedia.summary(query, sentences=2)
            self.speak(result)
        except Exception as e:
            self.speak("No Wikipedia results found")
            self.update_history("System", f"Wikipedia error: {e}", "#ff4444")

    # Query Wolfram Alpha for computations
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

    # Create and save a note using voice or text input
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

    # Perform a Google search in the default browser
    def google_search(self, query):
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.get('firefox').open_new(search_url)
            self.speak(f"Searching Google for {query}")
        except Exception as e:
            self.speak("Failed to perform Google search")
            self.update_history("System", f"Google search error: {e}", "#ff4444")

    # Handle entry field focus in event
    def on_entry_click(self):
        if self.input_entry.get() == "Type your message or use voice command...":
            self.input_entry.delete(0, END)
            self.input_entry.config(fg='#00ff99')

    # Handle entry field focus out event
    def on_focus_out(self):
        if self.input_entry.get() == "":
            self.input_entry.insert(0, "Type your message or use voice command...")
            self.input_entry.config(fg='#666666')

if __name__ == '__main__':
    root = Tk()
    gui = VoiceAssistantGUI(root)
    root.mainloop()