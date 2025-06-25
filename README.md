# MLOPS Project
## Muhammad Awais
## MSDS24035

### Project Details:

# 📝 Handwritten Quiz Grader

**Handwritten Quiz Grader** is a Streamlit-based application that automates the grading of handwritten quizzes using cutting-edge AI models from Google Gemini and OpenAI. This tool enables educators to upload scanned or photographed student quiz responses along with a grading rubric (either as text or image), and receive structured, detailed grading reports automatically.

## 🚀 Features

- 📷 **Multi-page Image Upload** or Camera Capture  
  Upload multiple quiz images or take photos directly within the app.

- 🤖 **Text Extraction with Google Gemini**  
  Accurately extracts handwritten content from student quiz images, including MCQs, using `gemini-2.5-flash`.

- 📋 **Flexible Rubric Input**  
  Enter rubric as structured text or upload an image rubric that gets processed via AI.

- 🧠 **Grading with OpenAI GPT-4o**  
  Grades answers according to your rubric with detailed, question-by-question feedback, partial credit, and total score.

- 📊 **Clear Result Presentation**  
  View extracted answers and formatted grading results with total score metrics.

- 🔒 **Secure Key Input**  
  Input and manage your API keys securely from the sidebar.

## 📸 How It Works

1. Upload or capture student quiz images.
2. Provide grading rubric (text or image).
3. Click “Grade Quiz” to process responses and generate results.
4. Review extracted answers and receive a comprehensive grading breakdown.

## 🧰 Tech Stack

- **Frontend**: Streamlit  
- **Image Text Extraction**: Google Gemini (via `google.generativeai`)  
- **Answer Grading**: OpenAI GPT-4o  
- **Image Handling**: PIL, Base64, Hashing for deduplication

## 🔑 Requirements

- Google Gemini API Key  
- OpenAI API Key

## 🛠️ Installation

```bash
git clone https://github.com/yourusername/handwritten-quiz-grader.git
cd handwritten-quiz-grader
pip install -r requirements.txt
streamlit run app.py
```

## 🧪 Example Use Cases

- Grade handwritten math, science, or language quizzes  
- Evaluate subjective answers with custom rubrics  
- Quickly process large batches of student responses

## Project UI Images
![Alt text](https://res.cloudinary.com/dyxlufcgu/image/upload/v1750867930/1_wzrv9l.png)
![Alt text](https://res.cloudinary.com/dyxlufcgu/image/upload/v1750868043/2_esl0wi.png)
![Alt text](https://res.cloudinary.com/dyxlufcgu/image/upload/v1750868073/3_j14ngp.png)
![Alt text](https://res.cloudinary.com/dyxlufcgu/image/upload/v1750868112/4_jdq2ec.png)
![Alt text](https://res.cloudinary.com/dyxlufcgu/image/upload/v1750868148/5_a88b6h.png)
![Alt text](https://res.cloudinary.com/dyxlufcgu/image/upload/v1750868178/6_zslwo7.png)


