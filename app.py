import streamlit as st
import os
import sys
import subprocess
import shutil
import yt_dlp
import zipfile
from pdf2docx import Converter
from PIL import Image
import fitz  # PyMuPDF

# =========================================================================
# SYSTEM PATH INJECTION
# Forces the cloud Linux environment to expose APT binary directories globally.
# =========================================================================
os.environ["PATH"] = os.environ.get("PATH", "") + os.pathsep + "/usr/bin" + os.pathsep + "/usr/local/bin" + os.pathsep + "/bin"

# Initialize configuration
st.set_page_config(page_title="LocalMediaEngine Online", page_icon="🎬", layout="wide")

st.title("🌐 LOCAL MEDIA ENGINE | Cloud Processing Hub")
st.write("Process your video, audio, and documents on high-performance cloud pipelines.")

# Core Status Monitoring Sidebar Panel
if shutil.which("ffmpeg"):
    st.sidebar.success("⚡ Audio/Video Encoder: ONLINE")
else:
    st.sidebar.error("❌ Audio/Video Encoder: OFFLINE (Reboot App)")

COOKIES_FILE = "cookies.txt"
BLOG_URL = "https://localmediaengineofficial.blogspot.com/p/process-complete-your-media-has-been.html"

# Workspace Routing
workspace = st.sidebar.selectbox(
    "Select Workspace", 
    ["YouTube Video Download", "Document & Format Hub", "Codec & Extraction Hub"]
)

# Output caching directory layout setup
out_dir = "./output_media"
os.makedirs(out_dir, exist_ok=True)

def render_monetized_download(file_path):
    """Renders the Step 1 (Ad Redirect) and Step 2 (Secure Download) flow."""
    st.success("🎉 Processing complete! Stream is locked and ready.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🔓 Step 1: Unlock Secure Download")
        st.write("Click below to pass verification and register your transaction payout profile.")
        st.link_button("👉 CLICK HERE TO UNLOCK (Opens Ads Page)", BLOG_URL, type="primary", use_container_width=True)
        
    with col2:
        st.markdown("### 📥 Step 2: Save Target File")
        st.write("After initiating Step 1, click below to pull the compiled binary straight to local memory.")
        with open(file_path, "rb") as f:
            st.download_button(
                label="📥 DOWNLOAD NOW",
                data=f,
                file_name=os.path.basename(file_path),
                use_container_width=True
            )

# ==========================================
# WORKSPACE 1: YOUTUBE DOWNLOADER
# ==========================================
if workspace == "YouTube Video Download":
    st.header("🌐 Secure YouTube Extraction Hub")
    
    st.info("💡 **Cloud Data-Center Routing Note:** YouTube applies fragment validation rules to data-center server addresses. To avoid 403 Forbidden flags, the extraction hub automatically processes downloads using unified single-container streams.")
    
    url = st.text_input("Paste YouTube Video URL:")
    mode = st.selectbox("Select Extractor Stream Profile:", [
        "Standard Video + Audio (Cloud Bypass Mode)", 
        "High-Definition Video Only (No Audio Fallback)", 
        "High-Quality Audio Only (.mp3)"
    ])
    
    if st.button("RUN EXTRACTOR ARRAY", type="primary"):
        if not url:
            st.error("Error: Destination URL boundary cannot be empty.")
        else:
            with st.spinner("Acquiring container headers and streaming chunks..."):
                opts = {
                    'outtmpl': os.path.join(out_dir, '%(title)s.%(ext)s'),
                    'noplaylist': True,
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Origin': 'https://www.youtube.com'
                    },
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['android', 'web'],
                            'skip': ['webpage']
                        }
                    }
                }
                
                if os.path.exists(COOKIES_FILE): 
                    opts['cookiefile'] = COOKIES_FILE
                
                if mode == "Standard Video + Audio (Cloud Bypass Mode)": 
                    opts.update({'format': 'best'})
                elif mode == "High-Definition Video Only (No Audio Fallback)": 
                    opts.update({'format': 'bestvideo/best'})
                elif mode == "High-Quality Audio Only (.mp3)": 
                    opts.update({
                        'format': 'bestaudio/best', 
                        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}]
                    })
                    
                try:
                    with yt_dlp.YoutubeDL(opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        filename = ydl.prepare_filename(info)
                        if mode == "High-Quality Audio Only (.mp3)":
                            filename = os.path.splitext(filename)[0] + ".mp3"
                    
                    render_monetized_download(filename)
                except Exception as e:
                    st.error(f"Extractor Pipeline Fault: {str(e)}")

# ==========================================
# WORKSPACE 2: DOCUMENT & FORMAT HUB
# ==========================================
elif workspace == "Document & Format Hub":
    st.header("📄 Document & Format Conversion Hub")
    uploaded_file = st.file_uploader("Upload target media or text document:")
    
    fmt = st.selectbox("Media Conversion Mapping:", ["-- None --", "Video to .mp4", "Video to .gif", "Video to .webm", "Video to .mov", "Video to .mkv", "Audio to .wav", "Image to .png", "Image to .jpeg"])
    doc = st.selectbox("Document Processing Route:", ["-- None --", ".docx to .pdf", ".pdf to .docx", ".pdf to image (.png)", ".jpeg to .pdf", ".png to .pdf"])
    
    if st.button("EXECUTE HUB PROCESSING", type="primary"):
        if not uploaded_file:
            st.error("Error: Please drag and drop or select an input file first.")
        else:
            action = fmt if fmt != "-- None --" else doc
            if action == "-- None --":
                st.error("Error: Please specify an operation target layout.")
            else:
                base_name, _ = os.path.splitext(uploaded_file.name)
                input_path = os.path.join(out_dir, uploaded_file.name)
                
                with open(input_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                    
                out_file = None
                cmd = ["ffmpeg", "-y", "-i", input_path]
                is_ffmpeg = False
                
                if action == "Video to .mp4":
                    out_file = os.path.join(out_dir, f"{base_name}.mp4")
                    cmd.extend(["-c:v", "libx264", "-preset", "fast", "-c:a", "aac", out_file])
                    is_ffmpeg = True
                elif action == "Video to .gif":
                    out_file = os.path.join(out_dir, f"{base_name}.gif")
                    cmd.extend(["-vf", "fps=15,scale=640:-1:flags=lanczos", "-c:v", "gif", out_file])
                    is_ffmpeg = True
                elif action == "Video to .webm":
                    out_file = os.path.join(out_dir, f"{base_name}.webm")
                    cmd.extend(["-c:v", "libvpx", "-b:v", "1M", "-c:a", "libvorbis", out_file])
                    is_ffmpeg = True
                elif action == "Video to .mov":
                    out_file = os.path.join(out_dir, f"{base_name}.mov")
                    cmd.extend(["-c:v", "libx264", "-c:a", "aac", out_file])
                    is_ffmpeg = True
                elif action == "Video to .mkv":
                    out_file = os.path.join(out_dir, f"{base_name}.mkv")
                    cmd.extend(["-c:v", "copy", "-c:a", "copy", out_file])
                    is_ffmpeg = True
                elif action == "Audio to .wav":
                    out_file = os.path.join(out_dir, f"{base_name}.wav")
                    cmd.extend(["-vn", "-c:a", "pcm_s16le", out_file])
                    is_ffmpeg = True
                elif action in ["Image to .png", "Image to .jpeg"]:
                    ext = "." + action.split(".")[-1]
                    out_file = os.path.join(out_dir, f"{base_name}{ext}")
                    cmd.extend(["-c", "copy", out_file])
                    is_ffmpeg = True

                try:
                    with st.spinner(f"Compiling conversion array for {action}..."):
                        if is_ffmpeg:
                            subprocess.run(cmd, check=True)
                        elif action == ".docx to .pdf":
                            out_file = os.path.join(out_dir, f"{base_name}.pdf")
                            subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", out_dir, input_path], check=True)
                        elif action == ".pdf to .docx":
                            out_file = os.path.join(out_dir, f"{base_name}.docx")
                            cv = Converter(input_path)
                            cv.convert(out_file)
                            cv.close()
                        elif action in [".jpeg to .pdf", ".png to .pdf"]:
                            out_file = os.path.join(out_dir, f"{base_name}.pdf")
                            img = Image.open(input_path).convert('RGB')
                            img.save(out_file)
                        elif action == ".pdf to image (.png)":
                            doc_pdf = fitz.open(input_path)
                            out_file = os.path.join(out_dir, f"{base_name}_extracted_pages.zip")
                            with zipfile.ZipFile(out_file, 'w') as zipf:
                                for idx in range(len(doc_pdf)):
                                    page = doc_pdf.load_page(idx)
                                    pix = page.get_pixmap(dpi=300)
                                    img_name = f"{base_name}_page_{idx+1}.png"
                                    img_path = os.path.join(out_dir, img_name)
                                    pix.save(img_path)
                                    zipf.write(img_path, img_name)
                                    os.remove(img_path)

                    if out_file and os.path.exists(out_file):
                        render_monetized_download(out_file)
                except Exception as e:
                    st.error(f"Engine Core Fault: {str(e)}")

# ==========================================
# WORKSPACE 3: CODEC & EXTRACTION HUB
# ==========================================
elif workspace == "Codec & Extraction Hub":
    st.header("🎬 Advanced Codec & Extraction Suite")
    uploaded_file = st.file_uploader("Upload source system video container:")
    action = st.selectbox("Select Target Pipeline Matrix Operation:", [
        "-- None --", 
        "Standard AVC (H.264) to HEVC (H.265)", 
        "HEVC (H.265) to Standard AVC (H.264)", 
        "Standard AVC (H.264) to AV1",
        "AV1 to Standard AVC (H.264)",
        "Video to Apple ProRes 422", 
        "Apple ProRes to Standard Video (.mp4)",
        "Extract Audio", 
        "Extract Video"
    ])
    
    if st.button("RUN ENGINE OPERATIONAL ARRAY", type="primary"):
        if not uploaded_file:
            st.error("Error: Input video object is missing.")
        elif action == "-- None --":
            st.error("Error: Please assign an operation pipeline.")
        else:
            base_name, ext = os.path.splitext(uploaded_file.name)
            input_path = os.path.join(out_dir, uploaded_file.name)
            with open(input_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
                
            cmd = ["ffmpeg", "-y", "-i", input_path]
            out_file = None
            
            if action == "Standard AVC (H.264) to HEVC (H.265)":
                out_file = os.path.join(out_dir, f"{base_name}_HEVC.mp4")
                cmd.extend(["-c:v", "libx265", "-pix_fmt", "yuv420p", "-c:a", "copy", out_file])
            elif action == "HEVC (H.265) to Standard AVC (H.264)":
                out_file = os.path.join(out_dir, f"{base_name}_AVC.mp4")
                cmd.extend(["-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "copy", out_file])
            elif action == "Standard AVC (H.264) to AV1":
                out_file = os.path.join(out_dir, f"{base_name}_AV1.mkv")
                cmd.extend(["-c:v", "libaom-av1", "-cpu-used", "6", "-c:a", "copy", out_file])
            elif action == "AV1 to Standard AVC (H.264)":
                out_file = os.path.join(out_dir, f"{base_name}_AVC_from_AV1.mp4")
                cmd.extend(["-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "copy", out_file])
            elif action == "Video to Apple ProRes 422":
                out_file = os.path.join(out_dir, f"{base_name}_master.mov")
                cmd.extend(["-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le", "-c:a", "pcm_s16le", out_file])
            elif action == "Apple ProRes to Standard Video (.mp4)":
                out_file = os.path.join(out_dir, f"{base_name}_from_prores.mp4")
                cmd.extend(["-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", out_file])
            elif action == "Extract Audio":
                out_file = os.path.join(out_dir, f"{base_name}_audio.mp3")
                cmd.extend(["-vn", "-c:a", "libmp3lame", "-q:a", "2", out_file])
            elif action == "Extract Video":
                out_file = os.path.join(out_dir, f"{base_name}_video_only{ext}")
                cmd.extend(["-map", "v:0", "-c:v", "copy", "-an", out_file])
                
            try:
                with st.spinner("Executing system encoding array..."):
                    subprocess.run(cmd, check=True)
                render_monetized_download(out_file)
            except Exception as e:
                st.error(f"FFmpeg Matrix Operational Fault: {str(e)}")
