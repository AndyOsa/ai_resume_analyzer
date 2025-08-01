from Flask import Flask, request, jsonify
from resume_parser import extract_text_from_pdf
import openai
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
app = Flask(__name__)
@app.route("/analyze", methods=["POST"])
def analyze_resume():
  if 'file' not in request.files:
    return jsonify({"error": "No file part"}), 400

file = request.files['file']
if file.filename == "":
  return jsonify({"error": "No selected file"}), 400

text = extract_text_from_pdf(file)
prompt = f""
You are a resume expert.Analyze the following resume text:
{text}
Give a structured response:
1. Structure quality
2. Key skills present
3. Weaknesses
4. Suggestions for improvement
"""
 response = openai.ChatCompletion.create(
   model="gpt-4",
   messages=[{"role": "system", "content": "You are an HR expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
        )
        result = response["choices"][0]["message"]["content"]
        return jsonify({"analysis":result})

        if __name__ == "__main__":
          app.run(debug=True)
     
