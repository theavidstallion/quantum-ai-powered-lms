// Login page functionality

let stream = null;
const video = document.getElementById('video');
const statusMsg = document.getElementById('statusMsg');
const loginBtn = document.getElementById('loginBtn');
const quantumModal = document.getElementById('quantumModal');
const quantumKeyDisplay = document.getElementById('quantumKeyDisplay');
const keyInput = document.getElementById('keyInput');
const verifyBtn = document.getElementById('verifyBtn');
const camBox = document.getElementById('camBox');

// Start webcam
async function startCamera() {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
    camBox.classList.add('verified');
  } catch (error) {
    statusMsg.textContent = 'Camera access denied. Please enable camera.';
    statusMsg.style.color = '#ef4444';
    camBox.classList.add('locked');
  }
}

// Capture image from video
function captureImage() {
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0);
  return canvas.toDataURL('image/jpeg');
}

// Handle login
async function handleLogin() {
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value.trim();
  
  if (!username || !password) {
    statusMsg.textContent = 'Please enter username and password';
    statusMsg.style.color = '#ef4444';
    return;
  }
  
  loginBtn.disabled = true;
  loginBtn.textContent = 'Authenticating...';
  statusMsg.textContent = 'Verifying face and credentials...';
  statusMsg.style.color = '#00e5ff';
  
  const image = captureImage();
  
  try {
    const response = await fetch('/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password, image })
    });
    
    const data = await response.json();
    
    if (data.success) {
      statusMsg.textContent = 'Face verified! Generating quantum key...';
      statusMsg.style.color = '#22c55e';
      setTimeout(() => showQuantumModal(data.quantum_key), 1000);
    } else {
      statusMsg.textContent = data.message;
      statusMsg.style.color = '#ef4444';
      camBox.classList.add('locked');
      setTimeout(() => camBox.classList.remove('locked'), 3000);
      loginBtn.disabled = false;
      loginBtn.textContent = 'LOGIN';
    }
  } catch (error) {
    statusMsg.textContent = 'Connection error. Please try again.';
    statusMsg.style.color = '#ef4444';
    loginBtn.disabled = false;
    loginBtn.textContent = 'LOGIN';
  }
}

// Show quantum verification modal
function showQuantumModal(key) {
  quantumKeyDisplay.textContent = key;
  quantumModal.style.display = 'flex';
  keyInput.focus();
}

// Verify quantum key
async function verifyQuantumKey() {
  const enteredKey = keyInput.value.trim();
  
  if (!enteredKey) {
    alert('Please enter the quantum key');
    return;
  }
  
  verifyBtn.disabled = true;
  verifyBtn.textContent = 'Verifying...';
  
  try {
    const response = await fetch('/quantum_verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ key: enteredKey })
    });
    
    const data = await response.json();
    
    if (data.success) {
      quantumModal.style.display = 'none';
      statusMsg.textContent = 'Quantum verification successful! Redirecting...';
      statusMsg.style.color = '#22c55e';
      setTimeout(() => window.location.href = '/dashboard', 1000);
    } else {
      alert('Invalid quantum key. Please try again.');
      keyInput.value = '';
      keyInput.focus();
      verifyBtn.disabled = false;
      verifyBtn.textContent = 'VERIFY';
    }
  } catch (error) {
    alert('Verification error. Please try again.');
    verifyBtn.disabled = false;
    verifyBtn.textContent = 'VERIFY';
  }
}

// Event listeners
loginBtn.addEventListener('click', handleLogin);
verifyBtn.addEventListener('click', verifyQuantumKey);
keyInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') verifyQuantumKey();
});

// Start camera on load
startCamera();
