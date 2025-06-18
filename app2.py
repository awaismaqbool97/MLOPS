import base64
import google.generativeai as genai
import openai
import streamlit as st
from PIL import Image
import io
import hashlib

st.set_page_config(page_title="Quiz Grader", page_icon="📝", layout="wide")

# Initialize session state
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = ""
if 'grading_result' not in st.session_state:
    st.session_state.grading_result = ""
if 'uploaded_images' not in st.session_state:
    st.session_state.uploaded_images = []
if 'rubric_image' not in st.session_state:
    st.session_state.rubric_image = None
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False
if 'camera_counter' not in st.session_state:
    st.session_state.camera_counter = 0

# Function to generate image hash
def generate_image_hash(image_bytes):
    return hashlib.md5(image_bytes).hexdigest()

# Function to encode image
def read_and_encode_image(uploaded_file):
    image_bytes = uploaded_file.getvalue()
    base64_encoded = base64.b64encode(image_bytes).decode("utf-8")
    
    try:
        img = Image.open(io.BytesIO(image_bytes))
        image_format = img.format.lower()
        return {"mime_type": f"image/{image_format}", "data": base64_encoded}
    except:
        return {"mime_type": "image/jpeg", "data": base64_encoded}

# Function to extract text with Gemini
def extract_text_with_gemini(image_data, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        response = model.generate_content([
            "Extract all text from this image exactly as written. Preserve line breaks, spacing, and formatting. If its an MCQ, give marked with option which student marked correct",
            {"inline_data": image_data}
        ])
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Function to grade with OpenAI
def grade_with_openai(extracted_text, rubric_text, api_key):
    try:
        client = openai.OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert teacher assistant that grades student work. Be fair and accurate."},
                {"role": "user", "content": f"""
                **Student's Handwritten Answers:**
                ----------
                {extracted_text}
                ----------
                
                **Grading Rubric:**
                ----------
                {rubric_text}
                ----------
                
                **Grading Instructions:**
                1. Evaluate each answer against the rubric
                2. Award partial credit where appropriate
                3. Ignore minor spelling/grammar errors
                4. Provide specific feedback for each question
                5. Highlight correct and incorrect answers
                6. Calculate total score/marks
                7. Format final output as:
                   - Question-by-question breakdown
                   - Detailed feedback
                   - TOTAL SCORE: [score]/[max possible]
                """}
            ],
            temperature=0.1
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Main app
st.title("📝 Handwritten Quiz Grader")
st.subheader("Upload multiple quiz images and rubric (text or image) for automatic grading")

# Sidebar for API keys and reset
with st.sidebar:
    st.header("Configuration")
    gemini_key = st.text_input("Gemini API Key", type="password")
    openai_key = st.text_input("OpenAI API Key", type="password")
    
    st.divider()
    if st.button("Reset All", use_container_width=True, type="secondary"):
        for key in list(st.session_state.keys()):
            if key != 'camera_counter':
                del st.session_state[key]
        st.rerun()
    
    st.info("Workflow:")
    st.info("1. Upload or Take quiz images\n2. Provide rubric (text or image)\n3. Process quiz\n4. Review results")

# Main content tabs
tab1, tab2, tab3 = st.tabs(["📷 Upload Quiz", "📝 Grading Rubric", "📊 Results"])

# Quiz images upload
with tab1:
    st.subheader("Upload Quiz Images")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        source = st.radio("Image source:", ("Upload Images", "Take Photos"), horizontal=True)
        
        if source == "Upload Images":
            uploaded_files = st.file_uploader(
                "Select quiz images (multiple allowed)",
                type=["jpg", "jpeg", "png"],
                accept_multiple_files=True
            )
            if uploaded_files:
                # Create a set of existing image hashes
                existing_hashes = set()
                if st.session_state.uploaded_images:
                    for img in st.session_state.uploaded_images:
                        existing_hashes.add(generate_image_hash(img.getvalue()))
                
                # Add new files that aren't duplicates
                for file in uploaded_files:
                    file_hash = generate_image_hash(file.getvalue())
                    if file_hash not in existing_hashes:
                        st.session_state.uploaded_images.append(file)
                        existing_hashes.add(file_hash)
        else:
            # Use counter to manage camera widget
            camera_files = st.camera_input(
                "Take pictures of quiz pages (capture one at a time)",
                key=f"camera_{st.session_state.camera_counter}",
                label_visibility="collapsed"
            )
            if camera_files:
                # Create a set of existing image hashes
                existing_hashes = set()
                if st.session_state.uploaded_images:
                    for img in st.session_state.uploaded_images:
                        existing_hashes.add(generate_image_hash(img.getvalue()))
                
                # Add new camera capture if not duplicate
                file_hash = generate_image_hash(camera_files.getvalue())
                if file_hash not in existing_hashes:
                    st.session_state.uploaded_images.append(camera_files)
                
                # Increment counter to reset camera
                st.session_state.camera_counter += 1
                st.rerun()
    
    with col2:
        if st.session_state.uploaded_images:
            st.subheader(f"{len(st.session_state.uploaded_images)} Images Ready")
            for i, img in enumerate(st.session_state.uploaded_images):
                cols = st.columns([4, 1])
                with cols[0]:
                    st.image(img, caption=f"Page {i+1}", width=150)
                with cols[1]:
                    if st.button("❌", key=f"remove_{i}"):
                        st.session_state.uploaded_images.pop(i)
                        st.rerun()
        else:
            st.info("No images uploaded yet")

# Rubric input
with tab2:
    st.subheader("Grading Rubric")
    rubric_method = st.radio("Rubric input method:", ("Text", "Image"), horizontal=True, index=0)
    
    if rubric_method == "Text":
        rubric_text = st.text_area(
            "Enter grading criteria:",
            height=250,
            placeholder="Example:\nQ1. Correct answer: 42 (3 points)\nQ2. Show your work (5 points)\n...",
            key="rubric_text"
        )
    else:
        rubric_img = st.file_uploader(
            "Upload rubric image (will be converted to text)",
            type=["jpg", "jpeg", "png"],
            key="rubric_uploader"
        )
        if rubric_img:
            st.session_state.rubric_image = rubric_img
            st.image(rubric_img, caption="Rubric Image", use_column_width=True)
            rubric_text = ""

# Results tab
with tab3:
    st.subheader("Processing and Results")
    
    if st.button("Grade Quiz", type="primary", use_container_width=True):
        # Validation checks
        if not st.session_state.uploaded_images:
            st.warning("Please upload at least one quiz image")
            st.stop()
        if not gemini_key or not openai_key:
            st.warning("Please enter both API keys")
            st.stop()
        
        # Process rubric
        rubric_text = ""
        if rubric_method == "Text":
            if not st.session_state.get('rubric_text', '').strip():
                st.warning("Please provide grading instructions")
                st.stop()
            rubric_text = st.session_state.rubric_text
        else:
            if not st.session_state.rubric_image:
                st.warning("Please upload a rubric image")
                st.stop()
            with st.spinner("Extracting rubric text..."):
                image_data = read_and_encode_image(st.session_state.rubric_image)
                rubric_text = extract_text_with_gemini(image_data, gemini_key)
        
        # Process quiz images
        all_extracted_text = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, img in enumerate(st.session_state.uploaded_images):
            status_text.text(f"Processing page {i+1}/{len(st.session_state.uploaded_images)}...")
            image_data = read_and_encode_image(img)
            extracted = extract_text_with_gemini(image_data, gemini_key)
            all_extracted_text.append(extracted)
            progress_bar.progress((i+1) / len(st.session_state.uploaded_images))
        
        full_text = "\n\n--- PAGE BREAK ---\n\n".join(all_extracted_text)
        st.session_state.extracted_text = full_text
        
        # Grade with OpenAI
        with st.spinner("Grading answers..."):
            st.session_state.grading_result = grade_with_openai(
                full_text, 
                rubric_text, 
                openai_key
            )
        
        st.session_state.processing_complete = True
    
    # Display extracted text
    if st.session_state.extracted_text:
        st.subheader("Extracted Text")
        with st.expander("View extracted text from images"):
            st.text_area("", 
                        st.session_state.extracted_text, 
                        height=300,
                        disabled=True,
                        label_visibility="collapsed")
    
    # Display grading results
    if st.session_state.grading_result:
        st.divider()
        st.subheader("Grading Results")
        
        if "TOTAL SCORE:" in st.session_state.grading_result:
            # Extract and display score prominently
            score_part = st.session_state.grading_result.split("TOTAL SCORE:")[-1].split('\n')[0].strip()
            st.metric("Final Score", score_part)
        
        st.markdown(st.session_state.grading_result)
        
        if st.session_state.processing_complete:
            st.balloons()
            st.session_state.processing_complete = False

# Footer
st.divider()
st.caption("Handwritten Quiz Grader | Automate your grading workflow")
