$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$htmlPath = Join-Path $root "MSE2_Student_Grievance_Report.html"
$pdfPath = Join-Path $root "MSE2_Student_Grievance_Report.pdf"

function Encode-Html($text) {
  return [System.Net.WebUtility]::HtmlEncode($text)
}

function Read-ProjectFile($relativePath) {
  $fullPath = Join-Path $root $relativePath
  if (Test-Path $fullPath) {
    return Encode-Html (Get-Content -LiteralPath $fullPath -Raw)
  }
  return "File missing: $relativePath"
}

function Add-CodeSection($title, $relativePath) {
  $code = Read-ProjectFile $relativePath
  return @"
<h3>$title</h3>
<div class="file-path">$relativePath</div>
<pre><code>$code</code></pre>
"@
}

function Local-FileUrl($path) {
  return ([System.Uri]$path).AbsoluteUri
}

$screenshotLogin = Local-FileUrl "C:\Users\KARTIKK\Pictures\Screenshots\Screenshot 2026-04-23 155014.png"
$screenshotRegister = Local-FileUrl "C:\Users\KARTIKK\Pictures\Screenshots\Screenshot 2026-04-23 155030.png"
$screenshotSubmit = Local-FileUrl "C:\Users\KARTIKK\Pictures\Screenshots\Screenshot 2026-04-23 155122.png"
$screenshotUpdate = Local-FileUrl "C:\Users\KARTIKK\Pictures\Screenshots\Screenshot 2026-04-23 155144.png"
$screenshotDelete = Local-FileUrl "C:\Users\KARTIKK\Pictures\Screenshots\Screenshot 2026-04-23 155154.png"
$screenshotBackendRender = Local-FileUrl "C:\Users\KARTIKK\Pictures\Screenshots\Screenshot 2026-04-23 161339.png"
$screenshotFrontendRender = Local-FileUrl "C:\Users\KARTIKK\Pictures\Screenshots\Screenshot 2026-04-23 161351.png"
$screenshotVsCode = Local-FileUrl "C:\Users\KARTIKK\Pictures\Screenshots\Screenshot 2026-04-23 161911.png"
$screenshotAtlas = Local-FileUrl "C:\Users\KARTIKK\Pictures\Screenshots\Screenshot 2026-04-23 161249.png"
$screenshotRenderOverview = Local-FileUrl "C:\Users\KARTIKK\Pictures\Screenshots\Screenshot 2026-04-23 161329.png"

$backendSections = @(
  Add-CodeSection "server.js" "backend\server.js"
  Add-CodeSection "config/db.js" "backend\config\db.js"
  Add-CodeSection "models/Student.js" "backend\models\Student.js"
  Add-CodeSection "models/Grievance.js" "backend\models\Grievance.js"
  Add-CodeSection "middleware/authMiddleware.js" "backend\middleware\authMiddleware.js"
  Add-CodeSection "controllers/authController.js" "backend\controllers\authController.js"
  Add-CodeSection "controllers/grievanceController.js" "backend\controllers\grievanceController.js"
  Add-CodeSection "routes/authRoutes.js" "backend\routes\authRoutes.js"
  Add-CodeSection "routes/grievanceRoutes.js" "backend\routes\grievanceRoutes.js"
  Add-CodeSection ".env.example" "backend\.env.example"
) -join "`n"

$frontendSections = @(
  Add-CodeSection "App.jsx" "frontend\src\App.jsx"
  Add-CodeSection "main.jsx" "frontend\src\main.jsx"
  Add-CodeSection "api.js" "frontend\src\api.js"
  Add-CodeSection "components/ProtectedRoute.jsx" "frontend\src\components\ProtectedRoute.jsx"
  Add-CodeSection "context/AuthContext.jsx" "frontend\src\context\AuthContext.jsx"
  Add-CodeSection "pages/Register.jsx" "frontend\src\pages\Register.jsx"
  Add-CodeSection "pages/Login.jsx" "frontend\src\pages\Login.jsx"
  Add-CodeSection "pages/Dashboard.jsx" "frontend\src\pages\Dashboard.jsx"
  Add-CodeSection "index.css" "frontend\src\index.css"
) -join "`n"

$projectTree = Encode-Html @"
C:\Users\KARTIKK\Desktop\Cracks
|-- backend
|   |-- config
|   |   `-- db.js
|   |-- controllers
|   |   |-- authController.js
|   |   `-- grievanceController.js
|   |-- middleware
|   |   `-- authMiddleware.js
|   |-- models
|   |   |-- Grievance.js
|   |   `-- Student.js
|   |-- routes
|   |   |-- authRoutes.js
|   |   `-- grievanceRoutes.js
|   |-- .env.example
|   |-- package.json
|   `-- server.js
|-- frontend
|   |-- src
|   |   |-- components
|   |   |   `-- ProtectedRoute.jsx
|   |   |-- context
|   |   |   `-- AuthContext.jsx
|   |   |-- pages
|   |   |   |-- Dashboard.jsx
|   |   |   |-- Login.jsx
|   |   |   `-- Register.jsx
|   |   |-- api.js
|   |   |-- App.jsx
|   |   |-- index.css
|   |   `-- main.jsx
|   |-- .env.example
|   |-- package.json
|   `-- vite.config.js
|-- README.md
`-- .gitignore
"@

$html = @"
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>AI Driven Full Stack Development MSE2 Submission</title>
  <style>
    @page {
      size: A4;
      margin: 22mm 18mm;
    }
    body {
      color: #111827;
      font-family: "Times New Roman", Arial, sans-serif;
      font-size: 13px;
      line-height: 1.45;
      margin: 0;
    }
    h1 {
      background: #ffff00;
      font-size: 22px;
      margin: 0 auto 8px;
      padding: 4px 8px;
      text-align: center;
      width: fit-content;
    }
    .subtitle {
      background: #00ffff;
      font-size: 18px;
      font-weight: bold;
      margin: 0 auto 28px;
      padding: 3px 8px;
      text-align: center;
      width: fit-content;
    }
    h2 {
      font-size: 18px;
      margin: 26px 0 12px;
      page-break-after: avoid;
    }
    h3 {
      font-size: 15px;
      margin: 18px 0 4px;
      page-break-after: avoid;
    }
    table {
      border-collapse: collapse;
      margin: 12px auto 28px;
      width: 82%;
    }
    th, td {
      border: 1px solid #000;
      padding: 8px 10px;
      text-align: left;
      vertical-align: top;
    }
    th {
      background: #dbe5f1;
      font-weight: bold;
      width: 32%;
    }
    a {
      color: #0645ad;
      word-break: break-all;
    }
    pre {
      background: #f7f7f7;
      border: 1px solid #c8c8c8;
      font-family: Consolas, "Courier New", monospace;
      font-size: 8.8px;
      line-height: 1.25;
      margin: 6px 0 14px;
      padding: 8px;
      white-space: pre-wrap;
      word-break: break-word;
    }
    .file-path {
      color: #444;
      font-family: Consolas, "Courier New", monospace;
      font-size: 11px;
      margin-bottom: 4px;
    }
    .note {
      background: #fff7d6;
      border: 1px solid #e5d58a;
      margin: 12px 0;
      padding: 10px;
    }
    .placeholder {
      border: 2px dashed #777;
      height: 210px;
      margin: 8px 0 18px;
      padding-top: 92px;
      text-align: center;
    }
    .screenshot {
      border: 1px solid #777;
      display: block;
      margin: 8px auto 20px;
      max-height: 500px;
      max-width: 100%;
      page-break-inside: avoid;
    }
    .page-break {
      page-break-before: always;
    }
  </style>
</head>
<body>
  <h1>AI Driven Full Stack Development (AI308B)</h1>
  <div class="subtitle">Moodle MSE2 Submission Format</div>

  <table>
    <tr><th>Name</th><td>Kartik Upadhyay</td></tr>
    <tr><th>Branch</th><td>CSE (AI&amp;ML)</td></tr>
    <tr><th>Roll Number</th><td>202501200400005</td></tr>
    <tr><th>Section</th><td>AI-B</td></tr>
    <tr><th>Shift</th><td>Evening</td></tr>
    <tr><th>Case Study Name</th><td>Student Grievance Management System</td></tr>
  </table>

  <h2>GitHub Repository Link</h2>
  <p><a href="https://github.com/Kartik3311/student-grievance-management">https://github.com/Kartik3311/student-grievance-management</a></p>

  <h2>Render Deployment Links for all Routes</h2>
  <p><strong>Backend Deployment Link</strong></p>
  <p><a href="https://student-grievance-management-dsst.onrender.com">https://student-grievance-management-dsst.onrender.com</a></p>

  <p><strong>Frontend Deployment Link</strong></p>
  <p><a href="https://student-grievance-frontend-f7o4.onrender.com">https://student-grievance-frontend-f7o4.onrender.com</a></p>

  <h2>Project Code</h2>
  <div class="note">
    Backend main file is <strong>server.js</strong>. Real <strong>.env</strong> file is not included because it contains the MongoDB Atlas password. The safe <strong>.env.example</strong> file is shown.
  </div>

  <h2>Backend Code</h2>
  <p><strong>Backend Code (server.js, .git, .env, model.js etc.) which is used in the project development.</strong></p>
  $backendSections

  <h2 class="page-break">Frontend Code</h2>
  <p><strong>Frontend Code (App.jsx, main.jsx, Dashboard.jsx, Login.jsx, Register.jsx etc.) which are used in the project development.</strong></p>
  $frontendSections

  <h2 class="page-break">Screenshots of Login, Register, Dashboard and All Functional Modules</h2>
  <h3>Register Page</h3>
  <img class="screenshot" src="$screenshotRegister" alt="Register Page Screenshot">
  <h3>Login Page</h3>
  <img class="screenshot" src="$screenshotLogin" alt="Login Page Screenshot">
  <h3>Dashboard Page</h3>
  <img class="screenshot" src="$screenshotSubmit" alt="Dashboard Page Screenshot">
  <h3>Submit Grievance Module</h3>
  <img class="screenshot" src="$screenshotSubmit" alt="Submit Grievance Screenshot">
  <h3>Search Grievance Module</h3>
  <div class="placeholder">Paste Search Screenshot Here</div>
  <h3>Update Grievance Module</h3>
  <img class="screenshot" src="$screenshotUpdate" alt="Update Grievance Screenshot">
  <h3>Delete Grievance Module</h3>
  <img class="screenshot" src="$screenshotDelete" alt="Delete Grievance Screenshot">
  <h3>MongoDB Atlas Students Collection</h3>
  <img class="screenshot" src="$screenshotAtlas" alt="MongoDB Atlas Collection Screenshot">
  <h3>MongoDB Atlas Grievances Collection</h3>
  <img class="screenshot" src="$screenshotAtlas" alt="MongoDB Atlas Grievances Collection Screenshot">
  <h3>Render Backend Deployment Screenshot</h3>
  <img class="screenshot" src="$screenshotBackendRender" alt="Render Backend Deployment Screenshot">
  <h3>Render Frontend Deployment Screenshot</h3>
  <img class="screenshot" src="$screenshotFrontendRender" alt="Render Frontend Deployment Screenshot">
  <h3>Render Project Overview Screenshot</h3>
  <img class="screenshot" src="$screenshotRenderOverview" alt="Render Project Overview Screenshot">

  <h2 class="page-break">Screenshot of VS Code Project Structure</h2>
  <pre><code>$projectTree</code></pre>
  <img class="screenshot" src="$screenshotVsCode" alt="VS Code Project Structure Screenshot">
</body>
</html>
"@

Set-Content -LiteralPath $htmlPath -Value $html -Encoding UTF8

$chromePaths = @(
  "C:\Program Files\Google\Chrome\Application\chrome.exe",
  "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
)

$browser = $chromePaths | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $browser) {
  throw "Chrome or Edge was not found."
}

if (Test-Path $pdfPath) {
  Remove-Item -LiteralPath $pdfPath -Force
}

$fileUrl = "file:///" + ($htmlPath -replace "\\", "/")
& $browser --headless --disable-gpu --no-sandbox --print-to-pdf="$pdfPath" "$fileUrl" | Out-Null

Write-Host "Created HTML: $htmlPath"
Write-Host "Created PDF: $pdfPath"
