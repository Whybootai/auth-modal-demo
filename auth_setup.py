import os
import zipfile

# File contents
files = {
    "index.html": """<!DOCTYPE html>
<html>
<head>
    <title>Auth Modal</title>
    <link rel="stylesheet" href="styles.css">
    <script src="https://accounts.google.com/gsi/client" async defer></script>
</head>
<body>
    <button id="openModal">Login/Signup</button>
    
    <div class="modal" id="authModal">
        <div class="modal-content">
            <span class="close">&times;</span>
            <h2>Welcome</h2>
            
            <!-- Google Sign-In -->
            <div id="g_id_onload"
                data-client_id="YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com"
                data-callback="handleGoogle">
            </div>
            <div class="g_id_signin" data-type="standard"></div>
            
            <div class="divider">OR</div>
            
            <!-- Email Form -->
            <form id="emailForm">
                <input type="email" placeholder="Email" required>
                <input type="password" placeholder="Password" required>
                <button type="submit">Continue</button>
            </form>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>""",

    "styles.css": """body {
    font-family: Arial, sans-serif;
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: #f0f2f5;
}

.modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    justify-content: center;
    align-items: center;
}

.modal-content {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    width: 400px;
    position: relative;
}

.g_id_signin { 
    margin: 1rem 0;
}

.divider {
    text-align: center;
    margin: 1.5rem 0;
    color: #666;
}""",

    "script.js": """// Modal Logic
const modal = document.getElementById('authModal');
const openBtn = document.getElementById('openModal');
const closeBtn = document.querySelector('.close');

openBtn.onclick = () => modal.style.display = "flex";
closeBtn.onclick = () => modal.style.display = "none";

window.onclick = (e) => {
    if(e.target === modal) modal.style.display = "none";
}

// Google Auth Handler
function handleGoogle(response) {
    console.log('Google response:', response);
    alert('Google authentication successful!');
    modal.style.display = "none";
}

// Email Form Handler
document.getElementById('emailForm').onsubmit = (e) => {
    e.preventDefault();
    alert('Email authentication submitted!');
    modal.style.display = "none";
}"""
}

# Create folder structure
folder_name = "auth_modal"
os.makedirs(folder_name, exist_ok=True)

# Create files
for filename, content in files.items():
    with open(f"{folder_name}/{filename}", "w") as f:
        f.write(content)

# Create ZIP file
with zipfile.ZipFile("auth_modal.zip", "w") as zipf:
    for file in files:
        zipf.write(f"{folder_name}/{file}", arcname=file)

print("✅ Files created successfully!")
print(f"📁 Folder: {folder_name}")
print(f"📦 ZIP archive: auth_modal.zip")
