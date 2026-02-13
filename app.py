import streamlit as st
import yt_dlp
from pydub import AudioSegment
import os
import tempfile
import shutil
from pathlib import Path
import time

# Configure page
st.set_page_config(
    page_title="YouTube Mashup Generator",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .input-container {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
    .generate-btn {
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        padding: 0.75rem 2rem;
        border: none;
        border-radius: 5px;
        width: 100%;
        margin-top: 1rem;
    }
    .generate-btn:hover {
        background-color: #155a8a;
    }
</style>
""", unsafe_allow_html=True)

def download_audio_from_youtube(singer_name, num_videos, duration_seconds, progress_bar):
    """
    Download audio clips from YouTube videos based on singer name
    """
    temp_dir = tempfile.mkdtemp()
    audio_clips = []
    
    try:
        # Configure yt-dlp options with more aggressive bypass
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'no_check_certificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'ios', 'web'],
                    'player_skip': ['configs', 'webpage', 'js'],
                }
            },
            'socket_timeout': 60,
            'retries': 3,
            'fragment_retries': 3,
        }
        
        # Try multiple search queries
        search_queries = [
            f"{singer_name} official audio",
            f"{singer_name} audio",
            f"{singer_name} song",
            f"best {singer_name} songs"
        ]
        
        videos_found = []
        
        for search_query in search_queries:
            if len(videos_found) >= num_videos:
                break
                
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Search and get video info
                    search_results = ydl.extract_info(
                        f"ytsearch{num_videos}:{search_query}",
                        download=False,
                        process=True
                    )
                    
                    if search_results and 'entries' in search_results:
                        for video in search_results['entries']:
                            if video and len(videos_found) < num_videos:
                                # Skip if already in list
                                if video.get('id') not in [v.get('id') for v in videos_found]:
                                    videos_found.append(video)
                                    
            except Exception as e:
                continue  # Try next search query
        
        if not videos_found:
            raise Exception(f"No videos found for '{singer_name}'. Try a different artist name.")
        
        # Download and process each video
        successful_downloads = 0
        for i, video in enumerate(videos_found):
            if successful_downloads >= num_videos:
                break
                
            progress = (i + 1) / num_videos
            progress_bar.progress(progress, f"Processing video {i+1}/{num_videos}")
            
            try:
                # Get video URL - try different possible keys
                video_url = None
                if 'url' in video:
                    video_url = video['url']
                elif 'webpage_url' in video:
                    video_url = video['webpage_url']
                elif 'id' in video:
                    video_url = f"https://www.youtube.com/watch?v={video['id']}"
                
                if not video_url:
                    st.warning(f"No valid URL found for video {i+1}")
                    continue
                
                # Try to download with retry logic
                for attempt in range(3):
                    try:
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            video_info = ydl.extract_info(video_url, download=True)
                            break
                    except Exception as retry_error:
                        if attempt == 2:  # Last attempt
                            raise retry_error
                        time.sleep(2)  # Wait before retry
                
                # Find the downloaded audio file
                audio_file = None
                for file in os.listdir(temp_dir):
                    if file.endswith('.mp3'):
                        audio_file = os.path.join(temp_dir, file)
                        break
                
                if audio_file:
                    # Load audio and extract first duration seconds
                    audio = AudioSegment.from_mp3(audio_file)
                    
                    # Extract the specified duration
                    if len(audio) > duration_seconds * 1000:
                        clip = audio[:duration_seconds * 1000]
                    else:
                        clip = audio
                    
                    audio_clips.append(clip)
                    successful_downloads += 1
                    
                    # Remove the temporary file
                    os.remove(audio_file)
                
            except Exception as e:
                st.warning(f"Could not process video {i+1}: {str(e)}")
                continue
        
        if not audio_clips:
            raise Exception("No audio clips could be processed. Try a different artist or reduce the number of videos.")
        
        return audio_clips, temp_dir
    
    except Exception as e:
        # Clean up temp directory on error
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        raise e

def create_mashup(audio_clips, output_filename):
    """
    Merge audio clips into a single mashup file
    """
    # Concatenate all audio clips
    final_audio = sum(audio_clips)
    
    # Create temporary output file
    temp_output = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    temp_output.close()
    
    # Export the mashup
    final_audio.export(temp_output.name, format='mp3')
    
    return temp_output.name

def main():
    # Header
    st.markdown('<h1 class="main-header">🎵 YouTube Mashup Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">Create amazing audio mashups from YouTube videos</p>', unsafe_allow_html=True)
    
    # Input section
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        singer_name = st.text_input(
            "Singer/Artist Name*",
            placeholder="e.g., Taylor Swift, Ed Sheeran",
            help="Enter the name of the singer or artist"
        )
        
        num_videos = st.number_input(
            "Number of Videos*",
            min_value=10,
            max_value=50,
            value=10,
            step=1,
            help="Minimum 10 videos will be processed"
        )
    
    with col2:
        duration_seconds = st.number_input(
            "Duration per Clip (seconds)*",
            min_value=20,
            max_value=120,
            value=30,
            step=5,
            help="Duration to extract from each video (minimum 20 seconds)"
        )
        
        output_filename = st.text_input(
            "Output File Name",
            value="mashup.mp3",
            help="Name of the final mashup file"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Validation
    if not singer_name.strip():
        st.error("Please enter a singer/artist name")
        return
    
    if not output_filename.endswith('.mp3'):
        output_filename += '.mp3'
    
    # Generate button
    if st.button("🎵 Generate Mashup", key="generate_btn", use_container_width=True):
        # Create progress container
        progress_container = st.container()
        
        with progress_container:
            progress_bar = st.progress(0, "Initializing...")
            status_text = st.empty()
            
            try:
                # Step 1: Download and process audio
                status_text.text("Searching and downloading audio from YouTube...")
                audio_clips, temp_dir = download_audio_from_youtube(
                    singer_name, num_videos, duration_seconds, progress_bar
                )
                
                # Step 2: Create mashup
                progress_bar.progress(0.8, "Creating mashup...")
                status_text.text("Merging audio clips...")
                mashup_file = create_mashup(audio_clips, output_filename)
                
                # Step 3: Complete
                progress_bar.progress(1.0, "Complete!")
                status_text.text("Mashup generated successfully!")
                
                # Success message
                st.markdown(
                    f'<div class="success-message">✅ Successfully created mashup with {len(audio_clips)} audio clips!</div>',
                    unsafe_allow_html=True
                )
                
                # Provide download button
                with open(mashup_file, 'rb') as f:
                    st.download_button(
                        label="📥 Download Mashup",
                        data=f.read(),
                        file_name=output_filename,
                        mime='audio/mpeg',
                        use_container_width=True
                    )
                
                # Clean up
                os.unlink(mashup_file)
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                
            except Exception as e:
                # Error handling
                st.markdown(
                    f'<div class="error-message">❌ Error: {str(e)}</div>',
                    unsafe_allow_html=True
                )
                st.info("💡 Tips: Make sure the singer name is correct and try again. Some videos may be restricted or unavailable.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #999; font-size: 0.9rem;">'
        'YouTube Mashup Generator • Powered by Streamlit</p>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
