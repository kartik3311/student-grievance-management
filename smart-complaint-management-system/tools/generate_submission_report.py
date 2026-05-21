from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "AIFS_AIML_ESE_Smart_Complaint_Submission.html"


def read(rel_path):
    return (ROOT / rel_path).read_text(encoding="utf-8")


def code_section(title, path, content=None):
    body = content if content is not None else read(path)
    return f"""
  <h3>{escape(title)}</h3>
  <div class="file-path">{escape(path.replace("/", "\\"))}</div>
  <pre><code>{escape(body)}</code></pre>
"""


def img(name, alt):
    path = (ROOT / "submission-assets" / name).resolve().as_posix()
    return f'<img class="screenshot" src="file:///{path}" alt="{escape(alt)}">'


def placeholder(text):
    return f'<div class="placeholder">{escape(text)}</div>'


tree = r"""C:\Users\KARTIKK\Desktop\Cracks\smart-complaint-management-system
|-- backend
|   |-- config
|   |   -- db.js
|   |-- controllers
|   |   |-- aiController.js
|   |   |-- authController.js
|   |   -- complaintController.js
|   |-- middleware
|   |   |-- authMiddleware.js
|   |   -- errorMiddleware.js
|   |-- models
|   |   |-- Complaint.js
|   |   -- User.js
|   |-- routes
|   |   |-- aiRoutes.js
|   |   |-- authRoutes.js
|   |   -- complaintRoutes.js
|   |-- .env.example
|   |-- package.json
|   -- server.js
|-- frontend
|   |-- src
|   |   |-- components
|   |   |   -- ProtectedRoute.jsx
|   |   |-- context
|   |   |   -- AuthContext.jsx
|   |   |-- pages
|   |   |   |-- Dashboard.jsx
|   |   |   |-- Login.jsx
|   |   |   -- Register.jsx
|   |   |-- api.js
|   |   |-- App.jsx
|   |   |-- index.css
|   |   -- main.jsx
|   |-- .env.example
|   |-- package.json
|   -- vite.config.js
|-- README.md
-- .gitignore"""

api_table = """
  <table>
    <tr><th>Endpoint</th><td>Purpose</td></tr>
    <tr><th>POST /api/register</th><td>Signup with bcrypt password hashing</td></tr>
    <tr><th>POST /api/login</th><td>Login and generate JWT token</td></tr>
    <tr><th>POST /api/complaints</th><td>Add complaint</td></tr>
    <tr><th>GET /api/complaints</th><td>View all complaints</td></tr>
    <tr><th>GET /api/complaints/search?location=Ghaziabad</th><td>Search/filter complaints by location/category</td></tr>
    <tr><th>PUT /api/complaints/:id</th><td>Update complaint status</td></tr>
    <tr><th>DELETE /api/complaints/:id</th><td>Delete complaint</td></tr>
    <tr><th>POST /api/ai/analyze</th><td>Analyze complaint text with AI API</td></tr>
    <tr><th>POST /api/complaints/:id/analyze</th><td>Analyze saved complaint and store AI result</td></tr>
  </table>
"""

html = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>AI Driven Full Stack Development ESE Submission</title>
  <style>
    @page {{ size: A4; margin: 22mm 18mm; }}
    body {{
      color: #111827;
      font-family: "Times New Roman", Arial, sans-serif;
      font-size: 13px;
      line-height: 1.45;
      margin: 0;
    }}
    h1 {{
      background: #ffff00;
      font-size: 22px;
      margin: 0 auto 8px;
      padding: 4px 8px;
      text-align: center;
      width: fit-content;
    }}
    .subtitle {{
      background: #00ffff;
      font-size: 18px;
      font-weight: bold;
      margin: 0 auto 28px;
      padding: 3px 8px;
      text-align: center;
      width: fit-content;
    }}
    h2 {{ font-size: 18px; margin: 26px 0 12px; page-break-after: avoid; }}
    h3 {{ font-size: 15px; margin: 18px 0 4px; page-break-after: avoid; }}
    table {{
      border-collapse: collapse;
      margin: 12px auto 28px;
      width: 82%;
    }}
    th, td {{
      border: 1px solid #000;
      padding: 8px 10px;
      text-align: left;
      vertical-align: top;
    }}
    th {{ background: #dbe5f1; font-weight: bold; width: 32%; }}
    a {{ color: #0645ad; word-break: break-all; }}
    pre {{
      background: #f7f7f7;
      border: 1px solid #c8c8c8;
      font-family: Consolas, "Courier New", monospace;
      font-size: 8.8px;
      line-height: 1.25;
      margin: 6px 0 14px;
      padding: 8px;
      white-space: pre-wrap;
      word-break: break-word;
    }}
    .file-path {{
      color: #444;
      font-family: Consolas, "Courier New", monospace;
      font-size: 11px;
      margin-bottom: 4px;
    }}
    .note {{
      background: #fff7d6;
      border: 1px solid #e5d58a;
      margin: 12px 0;
      padding: 10px;
    }}
    .placeholder {{
      border: 2px dashed #777;
      height: 210px;
      margin: 8px 0 18px;
      padding-top: 92px;
      text-align: center;
    }}
    .screenshot {{
      border: 1px solid #777;
      display: block;
      margin: 8px auto 20px;
      max-height: 500px;
      max-width: 100%;
      page-break-inside: avoid;
    }}
    .page-break {{ page-break-before: always; }}
  </style>
</head>
<body>
  <h1>AI Driven Full Stack Development (AI308B)</h1>
  <div class="subtitle">Moodle ESE AIML Submission Format</div>

  <table>
    <tr><th>Name</th><td>Kartik Upadhyay</td></tr>
    <tr><th>Branch</th><td>CSE (AI&amp;ML)</td></tr>
    <tr><th>Roll Number</th><td>2500291539005</td></tr>
    <tr><th>Section</th><td>B</td></tr>
    <tr><th>Shift</th><td>Evening</td></tr>
    <tr><th>Case Study Name</th><td>AI-Based Smart Complaint Management System</td></tr>
  </table>

  <h2>GitHub Repository Link</h2>
  <p>Paste GitHub repository link after pushing the project.</p>

  <h2>Render Deployment Links for all Routes</h2>
  <table>
    <tr><th>Backend Deployment Link</th><td>Paste backend Render URL after deployment</td></tr>
    <tr><th>Frontend Deployment Link</th><td>Paste frontend Render URL after deployment</td></tr>
    <tr><th>POST /api/register</th><td>https://your-backend.onrender.com/api/register</td></tr>
    <tr><th>POST /api/login</th><td>https://your-backend.onrender.com/api/login</td></tr>
    <tr><th>POST /api/complaints</th><td>https://your-backend.onrender.com/api/complaints</td></tr>
    <tr><th>GET /api/complaints</th><td>https://your-backend.onrender.com/api/complaints</td></tr>
    <tr><th>GET /api/complaints/search?location=Ghaziabad</th><td>https://your-backend.onrender.com/api/complaints/search?location=Ghaziabad</td></tr>
    <tr><th>PUT /api/complaints/:id</th><td>https://your-backend.onrender.com/api/complaints/:id</td></tr>
    <tr><th>DELETE /api/complaints/:id</th><td>https://your-backend.onrender.com/api/complaints/:id</td></tr>
    <tr><th>POST /api/ai/analyze</th><td>https://your-backend.onrender.com/api/ai/analyze</td></tr>
  </table>

  <h2>Project Code</h2>
  <p>Backend main file is server.js. Real .env file is not included because it contains MongoDB Atlas password and API keys. The safe .env.example file is shown.</p>

  <h2>Backend Code</h2>
  <p>Backend Code (server.js, .git, .env, model.js etc.) which is used in the project development.</p>
  {code_section("server.js", "backend/server.js")}
  {code_section("config/db.js", "backend/config/db.js")}
  {code_section(".env.example", "backend/.env.example")}
  {code_section("models/User.js", "backend/models/User.js")}
  {code_section("models/Complaint.js", "backend/models/Complaint.js")}
  {code_section("middleware/authMiddleware.js", "backend/middleware/authMiddleware.js")}
  {code_section("middleware/errorMiddleware.js", "backend/middleware/errorMiddleware.js")}
  {code_section("controllers/authController.js", "backend/controllers/authController.js")}
  {code_section("controllers/complaintController.js", "backend/controllers/complaintController.js")}
  {code_section("controllers/aiController.js", "backend/controllers/aiController.js")}
  {code_section("routes/authRoutes.js", "backend/routes/authRoutes.js")}
  {code_section("routes/complaintRoutes.js", "backend/routes/complaintRoutes.js")}
  {code_section("routes/aiRoutes.js", "backend/routes/aiRoutes.js")}

  <h2 class="page-break">Frontend Code</h2>
  <p>Frontend Code (App.jsx, main.jsx, Dashboard.jsx, Login.jsx, Register.jsx etc.) which are used in the project development.</p>
  {code_section("App.jsx", "frontend/src/App.jsx")}
  {code_section("main.jsx", "frontend/src/main.jsx")}
  {code_section("api.js", "frontend/src/api.js")}
  {code_section("context/AuthContext.jsx", "frontend/src/context/AuthContext.jsx")}
  {code_section("components/ProtectedRoute.jsx", "frontend/src/components/ProtectedRoute.jsx")}
  {code_section("Register.jsx", "frontend/src/pages/Register.jsx")}
  {code_section("Login.jsx", "frontend/src/pages/Login.jsx")}
  {code_section("Dashboard.jsx", "frontend/src/pages/Dashboard.jsx")}
  {code_section("index.css", "frontend/src/index.css")}

  <h2 class="page-break">Postman / Thunder Client HTTP Request Screenshots</h2>
  {api_table}
  {placeholder("Paste Postman/Thunder Client Register Request Screenshot Here")}
  {placeholder("Paste Postman/Thunder Client Login Request Screenshot Here")}
  {placeholder("Paste Postman/Thunder Client Complaint Request Screenshot Here")}
  {placeholder("Paste Postman/Thunder Client AI Analyze Request Screenshot Here")}

  <h2 class="page-break">Screenshots of Login, Register, Dashboard and All Functional Modules</h2>
  <h3>Register Page</h3>
  {img("register.png", "Register Page Screenshot")}
  <h3>Login Page</h3>
  {img("login.png", "Login Page Screenshot")}
  <h3>Dashboard / Complaint List Page</h3>
  {img("dashboard.png", "Dashboard Screenshot")}
  <h3>Complaint Registration Form</h3>
  {img("dashboard.png", "Complaint Registration Form Screenshot")}
  <h3>AI Analysis Result Display</h3>
  {img("ai-analysis.png", "AI Analysis Result Screenshot")}
  <h3>Complaint Status Update Page</h3>
  {placeholder("Paste Status Update Screenshot Here")}
  <h3>MongoDB Atlas Users Collection</h3>
  {placeholder("Paste MongoDB Atlas Users Collection Screenshot Here")}
  <h3>MongoDB Atlas Complaints Collection</h3>
  {placeholder("Paste MongoDB Atlas Complaints Collection Screenshot Here")}
  <h3>Render Backend Deployment Screenshot</h3>
  {placeholder("Paste Render Backend Deployment Screenshot Here")}
  <h3>Render Frontend Deployment Screenshot</h3>
  {placeholder("Paste Render Frontend Deployment Screenshot Here")}

  <h2 class="page-break">Screenshot of VS Code Project Structure</h2>
  <pre><code>{escape(tree)}</code></pre>
  {placeholder("Paste VS Code Project Structure Screenshot Here")}

  <h2 class="page-break">Manual Process Required</h2>
  <div class="note">
    <p><b>1. Paste secrets in backend/.env:</b> MONGO_URI, JWT_SECRET, and OPENROUTER_API_KEY. Do not commit .env.</p>
    <p><b>2. Push to GitHub:</b> initialize git, commit, add remote, and push main branch.</p>
    <p><b>3. Deploy backend on Render:</b> Root Directory backend, Build Command npm install, Start Command npm start.</p>
    <p><b>4. Deploy frontend on Render:</b> Root Directory frontend, Build Command npm install &amp;&amp; npm run build, Publish Directory dist.</p>
    <p><b>5. Add frontend env on Render:</b> VITE_API_URL=https://your-backend.onrender.com/api.</p>
    <p><b>6. Add screenshots:</b> MongoDB Atlas collections, Postman/Thunder requests, Render success pages, and VS Code project structure.</p>
  </div>
</body>
</html>
"""

OUT.write_text(html, encoding="utf-8")
print(OUT)
