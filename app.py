import streamlit as st
import cv2
import tempfile
import os
import io
import zipfile
from PIL import Image

st.set_page_config(page_title="Video Frame Extractor", page_icon="🎞️", layout="wide")

st.title("🎞️ Video Frame Extractor")
st.write("Upload a video and extract frames at regular intervals.")

def clear_frames():
    st.session_state.extracted_frames = None

if "extracted_frames" not in st.session_state:
    st.session_state.extracted_frames = None

# I) The user upload a video
uploaded_video = st.file_uploader("Upload a video file", type=['mp4', 'mov', 'avi', 'mkv'], on_change=clear_frames)

# II) Option to extract one frame each 10, 20, 30, 40, or 50 frames
frame_interval = st.selectbox(
    "Extract 1 frame every X frames:", 
    options=[10, 20, 30, 40, 50],
    index=2,
    on_change=clear_frames
)

if uploaded_video is not None:
    if st.button("Extract Frames", type="primary"):
        with st.spinner("Processing video... This may take a moment."):
            # Save uploaded video to a temp file
            # On Windows, we need to close the temp file before OpenCV can read it
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') 
            tfile.write(uploaded_video.read())
            tfile.close()
            
            # Open video using cv2
            cap = cv2.VideoCapture(tfile.name)
            
            if not cap.isOpened():
                st.error("Error opening video file. Please try another video format.")
            else:
                extracted_frames = []
                frame_count = 0
                
                # Progress bar for better UX
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                progress_bar = st.progress(0)
                
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    if frame_count % frame_interval == 0:
                        # Convert BGR to RGB (OpenCV uses BGR by default, PIL uses RGB)
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        pil_img = Image.fromarray(frame_rgb)
                        
                        # Save to bytes for individual download
                        img_byte_arr = io.BytesIO()
                        pil_img.save(img_byte_arr, format='JPEG', quality=95)
                        img_byte_arr = img_byte_arr.getvalue()
                        
                        extracted_frames.append({
                            "name": f"frame_{frame_count}.jpg",
                            "image": pil_img,
                            "bytes": img_byte_arr
                        })
                    
                    frame_count += 1
                    
                    # Update progress bar
                    if total_frames > 0:
                        progress = min(frame_count / total_frames, 1.0)
                        progress_bar.progress(progress)
                    
                cap.release()
                
                # Clean up temporary file
                try:
                    os.remove(tfile.name)
                except Exception as e:
                    pass
                
                if not extracted_frames:
                    st.warning("No frames were extracted. The video might be too short.")
                else:
                    st.session_state.extracted_frames = extracted_frames

    if st.session_state.extracted_frames:
        st.success(f"Successfully extracted {len(st.session_state.extracted_frames)} frames!")
        
        # IV) One download a zip for all the files
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for frame_data in st.session_state.extracted_frames:
                zip_file.writestr(frame_data["name"], frame_data["bytes"])
        
        st.markdown("### Download All Frames")
        st.download_button(
            label="📦 Download All Frames (ZIP)",
            data=zip_buffer.getvalue(),
            file_name="extracted_frames.zip",
            mime="application/zip",
            type="primary"
        )
        
        st.divider()
        
        # III) Generate a preview of the frame with a download button for each
        st.markdown("### Preview and Individual Downloads")
        
        # Add frame size option
        size_option = st.selectbox("Frame Preview Size:", options=["Super Small", "Small", "Medium", "Large"], index=2)
        
        if size_option == "Super Small":
            num_cols = 6
        elif size_option == "Small":
            num_cols = 4
        elif size_option == "Large":
            num_cols = 2
        else:
            num_cols = 3
            
        # Display frames in a grid layout
        cols = st.columns(num_cols)
        for i, frame_data in enumerate(st.session_state.extracted_frames):
            col = cols[i % num_cols]
            with col:
                st.image(frame_data["image"], caption=frame_data["name"], use_container_width=True)
                # Shortened label to save space in smaller columns
                st.download_button(
                    label="Download",
                    data=frame_data["bytes"],
                    file_name=frame_data["name"],
                    mime="image/jpeg",
                    key=f"download_{frame_data['name']}"
                )
