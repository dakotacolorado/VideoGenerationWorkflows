# AI Video Generation Workflows

A simple Python project for generating videos from text prompts using AI tools. This is a v0 initiative focused on basic text-to-video generation.

## Project Overview

This project provides a simple interface to generate videos from text prompts:

- **Basic Video Generation**: Generate videos from text prompts with specified duration
- **Simple Interface**: Just provide a prompt, duration, and filename
- **Modular Design**: Base video generation is separate from future enhancements

## Features (v0)

- 🎬 Basic text-to-video generation
- ⏱️ Configurable video duration
- 📁 Simple file output
- 🔧 Modular workflow design

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd VideoGenerationWorkflows
   ```

2. **Create a virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp env.example .env
   
   # Edit .env with your API keys
   # OPENAI_API_KEY=your_openai_key_here
   ```

## Project Structure

```
VideoGenerationWorkflows/
├── src/
│   ├── base_video_gen/    # Basic video generation module
│   └── utils/             # Utility functions
├── requirements.txt       # Python dependencies
├── env.example           # Environment variables template
└── README.md            # This file
```

## Usage

### Basic Video Generation

```python
from src.base_video_gen.generator import BaseVideoGenerator

# Initialize generator
generator = BaseVideoGenerator()

# Generate video from text prompt
result = generator.generate(
    prompt="A beautiful sunset over mountains",
    duration=10,
    filename="sunset_video.mp4"
)
```

## Configuration

Create a `.env` file with your API keys:

```env
# AI Service API Keys
OPENAI_API_KEY=your_openai_key_here
```

## Next Steps

Future versions may include:
- Video enhancement and editing
- Audio generation and synchronization
- Batch processing capabilities
- Additional AI model integrations
