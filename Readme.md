# JELIL Voice Assistant

A modern, feature-rich voice assistant with a graphical user interface, built with Python and Tkinter.

## Features

- Voice command recognition using SpeechRecognition
- Text-to-speech output using pyttsx3 and Google Cloud TTS
- Web browsing capabilities
- Wikipedia searches
- Mathematical computations using Wolfram Alpha
- Note-taking functionality
- Modern GUI interface with custom styling
- Support for both voice and text input
- Google search integration
- Real-time status updates and command history

## Requirements

- Python 3.8 or higher
- Windows OS (for optimal compatibility)
- Firefox browser (for web browsing)
- Wolfram Alpha API key (for computations)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/jelil-voice-assistant.git
cd jelil-voice-assistant
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your API keys:

```
WOLFRAM_APP_ID=your_wolfram_alpha_app_id
GOOGLE_APPLICATION_CREDENTIALS=path_to_your_google_credentials.json
```

## Usage

1. Run the application:

```bash
python main.py
```

2. Use voice commands by clicking the microphone button or typing in the text input field.

### Available Commands

- `say [text]`: Make the assistant speak the specified text
- `go to [website]`: Open a website in Firefox
- `wikipedia [query]`: Search Wikipedia for information
- `compute [expression]`: Calculate mathematical expressions using Wolfram Alpha
- `google [query]`: Perform a Google search
- `log [note]`: Create a new note
- `exit`: Close the application

### Activation Words

The assistant responds to the following activation words:

- "computer"
- "Jelil"

## Project Structure

- `main.py`: Application entry point and core functionality
- `requirements.txt`: Project dependencies
- `.env`: Environment variables and API keys
- `assets/`: Directory for images and other assets
- `notes/`: Directory for saved notes
- `docker-compose.yml`: Docker configuration (if using containerization)

## Dependencies

Key dependencies include:

- SpeechRecognition: For voice input processing
- pyttsx3: For text-to-speech functionality
- wolframalpha: For mathematical computations
- wikipedia: For Wikipedia searches
- google-cloud-texttospeech: For cloud-based TTS
- tkinter: For the GUI interface
- pygame: For audio handling
- PIL: For image processing

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
