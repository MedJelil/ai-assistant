# JELIL Voice Assistant

A modern, feature-rich voice assistant with a graphical user interface.

## Features

- Voice command recognition
- Text-to-speech output
- Web browsing
- Wikipedia searches
- Mathematical computations using Wolfram Alpha
- Note-taking capability
- Modern GUI interface
- Support for both voice and text input

## Requirements

- Python 3.8 or higher
- Firefox browser (for web browsing)
- Wolfram Alpha API key (optional, for computations)
- Google Cloud credentials (optional, for cloud TTS)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/jelil-voice-assistant.git
cd jelil-voice-assistant
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
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
- `compute [expression]`: Calculate mathematical expressions
- `log [note]`: Create a new note
- `exit`: Close the application

### Activation Words

The assistant responds to the following activation words:

- "computer"
- "Jelil"
- "shodan"
- "showdown"

## Project Structure

- `main.py`: Application entry point
- `config.py`: Configuration settings
- `speech_handler.py`: Speech recognition and TTS functionality
- `command_processor.py`: Command processing logic
- `gui.py`: Graphical user interface
- `assets/`: Directory for images and other assets
- `notes/`: Directory for saved notes

## Logging

Logs are saved to `voice_assistant.log` in the project root directory.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
