$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$outputHtml = Join-Path $root "MSE2_Student_Grievance_Submission.html"
$outputDocx = Join-Path $root "MSE2_Student_Grievance_Submission.docx"
$outputPdf = Join-Path $root "MSE2_Student_Grievance_Submission.pdf"

function HtmlEncode($value) {
  return [System.Net.WebUtility]::HtmlEncode($value)
}

function ReadCode($relativePath) {
  $fullPath = Join-Path $root $relativePath
  if (Test-Path $fullPath) {
    return HtmlEncode((Get-Content -LiteralPath $fullPath -Raw))
  }
  return "File not found: $relativePath"
}

function CodeBlock($title, $relativePath) {
  $code = ReadCode $relativePath
  return @"
<h3>$title</h3>
<p class="path">$relativePath</p>
<pre><code>$code</code></pre>
"@
}

$projectTree = @"
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

$backendCode = @(
  CodeBlock "Backend Main File - server.js" "backend\server.js"
  CodeBlock "Database Connection - db.js" "backend\config\db.js"
  CodeBlock "Student Model - Student.js" "backend\models\Student.js"
  CodeBlock "Grievance Model - Grievance.js" "backend\models\Grievance.js"
  CodeBlock "Authentication Middleware - authMiddleware.js" "backend\middleware\authMiddleware.js"
  CodeBlock "Authentication Controller - authController.js" "backend\controllers\authController.js"
  CodeBlock "Grievance Controller - grievanceController.js" "backend\controllers\grievanceController.js"
  CodeBlock "Authentication Routes - authRoutes.js" "backend\routes\authRoutes.js"
  CodeBlock "Grievance Routes - grievanceRoutes.js" "backend\routes\grievanceRoutes.js"
  CodeBlock "Backend Environment Example - .env.example" "backend\.env.example"
  CodeBlock "Backend package.json" "backend\package.json"
) -join "`n"

$frontendCode = @(
  CodeBlock "React Entry File - main.jsx" "frontend\src\main.jsx"
  CodeBlock "React Routes - App.jsx" "frontend\src\App.jsx"
  CodeBlock "API Helper - api.js" "frontend\src\api.js"
  CodeBlock "Protected Route - ProtectedRoute.jsx" "frontend\src\components\ProtectedRoute.jsx"
  CodeBlock "Auth Context - AuthContext.jsx" "frontend\src\context\AuthContext.jsx"
  CodeBlock "Register Page - Register.jsx" "frontend\src\pages\Register.jsx"
  CodeBlock "Login Page - Login.jsx" "frontend\src\pages\Login.jsx"
  CodeBlock "Dashboard Page - Dashboard.jsx" "frontend\src\pages\Dashboard.jsx"
  CodeBlock "Frontend CSS - index.css" "frontend\src\index.css"
  CodeBlock "Frontend package.json" "frontend\package.json"
) -join "`n"

$html = @"
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>AI Driven Full Stack Development MSE2 Submission</title>
  <style>
    body {
      color: #111827;
      font-family: Arial, Helvetica, sans-serif;
      line-height: 1.45;
      margin: 40px;
    }
    h1, h2, h3 {
      color: #0f172a;
    }
    h1 {
      text-align: center;
      font-size: 24px;
      margin-bottom: 8px;
    }
    h2 {
      border-bottom: 2px solid #d1d5db;
      font-size: 20px;
      margin-top: 32px;
      padding-bottom: 6px;
      page-break-after: avoid;
    }
    h3 {
      font-size: 16px;
      margin-top: 22px;
      page-break-after: avoid;
    }
    table {
      border-collapse: collapse;
      margin: 18px 0;
      width: 100%;
    }
    td, th {
      border: 1px solid #9ca3af;
      padding: 9px;
      vertical-align: top;
    }
    th {
      background: #e5e7eb;
      text-align: left;
    }
    a {
      color: #1d4ed8;
    }
    pre {
      background: #f3f4f6;
      border: 1px solid #d1d5db;
      border-radius: 6px;
      font-size: 10px;
      overflow-wrap: break-word;
      padding: 12px;
      white-space: pre-wrap;
      word-break: break-word;
    }
    .subtitle {
      text-align: center;
      margin-bottom: 24px;
    }
    .path {
      color: #4b5563;
      font-size: 12px;
      margin-top: -8px;
    }
    .placeholder {
      border: 2px dashed #9ca3af;
      color: #374151;
      margin: 12px 0 22px;
      min-height: 160px;
      padding: 18px;
      text-align: center;
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
    <tr><th>Branch</th><td>AIML</td></tr>
    <tr><th>Roll Number</th><td>202501200400005</td></tr>
    <tr><th>Section</th><td>AI-B</td></tr>
    <tr><th>Shift</th><td>Evening</td></tr>
    <tr><th>Case Study Name</th><td>Student Grievance Management System</td></tr>
  </table>

  <h2>GitHub Repository Link</h2>
  <p><a href="https://github.com/Kartik3311/student-grievance-management">https://github.com/Kartik3311/student-grievance-management</a></p>

  <h2>Render Deployment Links for all Routes</h2>
  <table>
    <tr>
      <th>Backend Deployment Link</th>
      <td><a href="https://student-grievance-management-dsst.onrender.com">https://student-grievance-management-dsst.onrender.com</a></td>
    </tr>
    <tr>
      <th>Frontend Deployment Link</th>
      <td><a href="https://student-grievance-frontend-f7o4.onrender.com">https://student-grievance-frontend-f7o4.onrender.com</a></td>
    </tr>
  </table>

  <h2>Project Code</h2>
  <p>This project uses <strong>server.js</strong> as the backend entry file instead of index.js. The real backend <strong>.env</strong> file contains private database credentials and is not included in the report. The safe <strong>.env.example</strong> file is included.</p>

  <h2>Backend Code</h2>
  $backendCode

  <h2 class="page-break">Frontend Code</h2>
  $frontendCode

  <h2 class="page-break">Screenshots of Login, Register, Dashboard and All Functional Modules</h2>
  <p>Paste your screenshots below in the required order before final PDF submission.</p>

  <h3>1. Register Page</h3>
  <div class="placeholder">Paste Register Page Screenshot Here</div>

  <h3>2. Login Page</h3>
  <div class="placeholder">Paste Login Page Screenshot Here</div>

  <h3>3. Dashboard Page</h3>
  <div class="placeholder">Paste Dashboard Page Screenshot Here</div>

  <h3>4. Submit Grievance Module</h3>
  <div class="placeholder">Paste Submit Grievance Screenshot Here</div>

  <h3>5. View All Grievances Module</h3>
  <div class="placeholder">Paste Grievance List Screenshot Here</div>

  <h3>6. Search Grievance Module</h3>
  <div class="placeholder">Paste Search Grievance Screenshot Here</div>

  <h3>7. Update Grievance Module</h3>
  <div class="placeholder">Paste Update Grievance Screenshot Here</div>

  <h3>8. Delete Grievance Module</h3>
  <div class="placeholder">Paste Delete Grievance Screenshot Here</div>

  <h3>9. MongoDB Atlas Students Collection</h3>
  <div class="placeholder">Paste MongoDB Atlas Students Collection Screenshot Here</div>

  <h3>10. MongoDB Atlas Grievances Collection</h3>
  <div class="placeholder">Paste MongoDB Atlas Grievances Collection Screenshot Here</div>

  <h3>11. Render Backend Deployment</h3>
  <div class="placeholder">Paste Render Backend Deployment Screenshot Here</div>

  <h3>12. Render Frontend Deployment</h3>
  <div class="placeholder">Paste Render Frontend Deployment Screenshot Here</div>

  <h2 class="page-break">Screenshot of VS Code Project Structure</h2>
  <p>Project structure used for the Student Grievance Management System:</p>
  <pre><code>$(HtmlEncode $projectTree)</code></pre>
  <div class="placeholder">Paste VS Code Project Structure Screenshot Here</div>
</body>
</html>
"@

Set-Content -LiteralPath $outputHtml -Value $html -Encoding UTF8

$wordCreated = $false
try {
  $word = New-Object -ComObject Word.Application
  $word.Visible = $false
  $document = $word.Documents.Open($outputHtml)
  $document.SaveAs([ref]$outputDocx, [ref]16)
  $document.ExportAsFixedFormat($outputPdf, 17)
  $document.Close()
  $word.Quit()
  $wordCreated = $true
} catch {
  if ($document) { $document.Close($false) }
  if ($word) { $word.Quit() }
  Write-Host "Word PDF conversion skipped: $($_.Exception.Message)"
}

Write-Host "Created HTML report: $outputHtml"
if ($wordCreated) {
  Write-Host "Created Word report: $outputDocx"
  Write-Host "Created PDF report: $outputPdf"
}
