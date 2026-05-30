from flask import (
    Flask, render_template, request, redirect,
    url_for, jsonify, send_from_directory
)
from flask_cors import CORS
from groq import Groq
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()

# -------------------------------------------------
# APP CONFIG
# -------------------------------------------------
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DATABASE = "database.db"

# -------------------------------------------------
# LOAD KNOWLEDGE BASE (CHATBOT)
# -------------------------------------------------
def load_knowledge_base():
    try:
        with open("knowledge_base.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

knowledge_base = load_knowledge_base()

# -------------------------------------------------
# GROQ CLIENT
# -------------------------------------------------



client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

# -------------------------------------------------
# HOME
# -------------------------------------------------
@app.route("/")
def home():
    return render_template("home.html")

# -------------------------------------------------
# APPLY (INTERNSHIP)
# -------------------------------------------------
@app.route("/apply", methods=["GET", "POST"])
def apply():

    if request.method == "POST":

        try:

            print("\n===== FORM SUBMITTED =====")

            print("FORM DATA:", request.form)
            print("FILES:", request.files)

            name = request.form["name"]
            email = request.form["email"]
            phone = request.form["phone"]
            college = request.form["college"]
            department = request.form["department"]
            year = request.form["year"]

            resume = request.files["resume"]

            print("Resume Name:", resume.filename)

            resume_filename = resume.filename

            resume.save(
                os.path.join(UPLOAD_FOLDER, resume_filename)
            )

            print("Resume saved successfully")

            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO applications
                (name,email,phone,college,department,year,resume)
                VALUES (?,?,?,?,?,?,?)
            """, (
                name,
                email,
                phone,
                college,
                department,
                year,
                resume_filename
            ))

            conn.commit()

            print("Database saved successfully")

            conn.close()

            return redirect(url_for("apply_success"))

        except Exception as e:

            print("ERROR OCCURRED:")
            print(e)

            return str(e)

    return render_template("apply.html")
@app.route("/apply-success")
def apply_success():
    return render_template("apply_success.html")

# -------------------------------------------------
# OTHER WEBSITE PAGES
# -------------------------------------------------
@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# -------------------------------------------------
# SERVICES
# -------------------------------------------------
@app.route("/service/cloud")
def service_cloud():
    return render_template("service-cloud.html")

@app.route("/service/fullstack")
def service_fullstack():
    return render_template("service-fullstack.html")

@app.route("/service/genai")
def service_genai():
    return render_template("service-genai.html")

@app.route("/service/ml")
def service_ml():
    return render_template("service-ML.html")

@app.route("/service/sap")
def service_sap():
    return render_template("service-sap.html")

@app.route("/service/ui")
def service_ui():
    return render_template("service-ui.html")

# -------------------------------------------------
# CHATBOT UI PAGE
# -------------------------------------------------
@app.route("/chat")
def chat_page():
    return render_template("chat.html")

# -------------------------------------------------
# CHATBOT API (USED BY JS)
# -------------------------------------------------
@app.route("/chatbot", methods=["POST"])
def chatbot_api():
    user_message = request.json.get("message", "")

    prompt = f"""
You are Mindful AI — a calm, professional, emotionally supportive AI assistant.

Use ONLY the knowledge base below when relevant.

Knowledge base:
{knowledge_base}

User message:
{user_message}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are Mindful AI."},
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content
    return jsonify({"reply": answer})

# -------------------------------------------------
# ADMIN – VIEW APPLICATIONS
# -------------------------------------------------
@app.route("/admin/applications")
def view_applications():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM applications")
    data = cursor.fetchall()
    conn.close()
    return render_template("applications.html", applications=data)

# -------------------------------------------------
# DOWNLOAD UPLOADED FILES
# -------------------------------------------------
@app.route("/uploads/<filename>")
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# -------------------------------------------------
# RUN APP
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
