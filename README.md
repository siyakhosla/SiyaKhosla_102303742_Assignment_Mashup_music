# YouTube Mashup Generator

A complete web application that creates audio mashups from YouTube videos using Streamlit.

## Features

- **Clean UI**: Modern, professional interface with input validation
- **YouTube Integration**: Automatically searches and downloads audio from YouTube
- **Audio Processing**: Extracts specified duration clips and merges them
- **Cloud Ready**: Fully compatible with Streamlit Cloud deployment
- **Error Handling**: Graceful error handling with user-friendly messages

## Technical Stack

- **Backend**: Python 3.10
- **Frontend**: Streamlit
- **YouTube Download**: yt-dlp
- **Audio Processing**: pydub
- **Audio Encoding**: FFmpeg

## Project Structure

```
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── runtime.txt        # Python version specification
├── packages.txt       # System dependencies (FFmpeg)
└── README.md          # This file
```

## How It Works

1. **Input Collection**: User provides singer name, number of videos, clip duration, and output filename
2. **YouTube Search**: Searches YouTube for videos matching the singer name
3. **Audio Download**: Downloads audio from the top N videos using yt-dlp
4. **Clip Extraction**: Extracts the first specified duration from each video
5. **Audio Merging**: Combines all clips into a single mashup file
6. **Download**: Provides a download button for the generated mashup

## Deployment Instructions

### Method 1: Streamlit Cloud (Recommended)

1. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub repository
   - Select the repository and branch (main)
   - Main file path: `app.py`
   - Click "Deploy"

3. **Configuration**
   - Streamlit Cloud will automatically:
     - Install Python 3.10 (from runtime.txt)
     - Install Python packages (from requirements.txt)
     - Install FFmpeg (from packages.txt)

### Method 2: Local Development

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install FFmpeg**
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt-get install ffmpeg`

3. **Run Application**
   ```bash
   streamlit run app.py
   ```

## Usage Instructions

1. **Enter Singer Name**: Type the name of the artist/singer
2. **Set Number of Videos**: Choose how many videos to process (minimum 10)
3. **Set Clip Duration**: Specify duration in seconds for each clip (minimum 20)
4. **Choose Output Name**: Set the filename for your mashup (defaults to mashup.mp3)
5. **Generate**: Click "Generate Mashup" to start processing
6. **Download**: Once complete, download your mashup file

## Input Validation

- **Singer Name**: Required field, cannot be empty
- **Number of Videos**: Must be ≥ 10, maximum 50
- **Duration**: Must be ≥ 20 seconds, maximum 120 seconds
- **Output File**: Automatically adds .mp3 extension if missing

## Error Handling

The application handles common errors gracefully:
- No videos found for the specified singer
- Videos that are private or unavailable
- Network connectivity issues
- Audio processing errors
- File system permission issues

## Technical Notes

- Uses temporary directories for processing to avoid clutter
- Automatically cleans up temporary files after processing
- Progress indicators show real-time processing status
- Compatible with cloud environments (no local file dependencies)
- Uses yt-dlp for reliable YouTube audio extraction

## Dependencies

### Python Packages (requirements.txt)
- `streamlit`: Web framework
- `yt-dlp`: YouTube video/audio downloading
- `pydub`: Audio processing and manipulation

### System Packages (packages.txt)
- `ffmpeg`: Audio encoding and processing

### Runtime (runtime.txt)
- `python-3.10`: Python version specification

## Troubleshooting

### Common Issues

1. **"No videos found"**
   - Check singer name spelling
   - Try alternative spellings or include "official audio"

2. **"Audio processing failed"**
   - Some videos may be restricted
   - Try reducing the number of videos

3. **"Deployment failed"**
   - Ensure all files are in the repository
   - Check that runtime.txt and packages.txt are correctly formatted

### Performance Tips

- For faster processing, use fewer videos (10-15)
- Shorter clip durations (20-30 seconds) process faster
- Popular artists have more available videos

## License

This project is for educational purposes. Ensure compliance with:
- YouTube's Terms of Service
- Copyright laws in your jurisdiction
- Fair use guidelines for audio mashups

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all dependencies are correctly installed
3. Ensure internet connectivity for YouTube access
