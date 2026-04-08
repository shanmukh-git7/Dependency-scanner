const API_URL = 'http://localhost:8000';
let currentScanHistory = [];
let selectedFile = null;

// ================= UTILS =================
function getToken() { return localStorage.getItem('token'); }
function getRole() { return localStorage.getItem('role'); }
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    window.location.href = '/login.html';
}

async function apiRequest(endpoint, method = 'GET', body = null, isFile = false) {
    const headers = {};
    const token = getToken();
    if (token) headers['Authorization'] = `Bearer ${token}`;
    if (!isFile) headers['Content-Type'] = 'application/json';

    const config = { method, headers };
    if (body) config.body = isFile ? body : JSON.stringify(body);

    try {
        const response = await fetch(`${API_URL}${endpoint}`, config);
        if (response.status === 401) { logout(); return null; }
        return response;
    } catch (error) {
        console.error('API Request Failed:', error);
        alert('API Connection Failed');
        return null;
    }
}

// ================= PAGE LOGIC =================

document.addEventListener('DOMContentLoaded', () => {
    initMatrixEffect();
    // Theme Init
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    const themeBtn = document.getElementById('theme-toggle');
    if (themeBtn) {
        themeBtn.innerText = savedTheme === 'dark' ? '☀️' : '🌙';
        themeBtn.onclick = () => {
            const current = document.documentElement.getAttribute('data-theme');
            const next = current === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem('theme', next);
            themeBtn.innerText = next === 'dark' ? '☀️' : '🌙';
            // Trigger chart update if on dashboard
            if (window.location.pathname.endsWith('dashboard.html') && currentScanHistory.length > 0) {
                const latest = currentScanHistory[0];
                renderChart(latest.total_dependencies, latest.vulnerabilities_count);
            }
        };
    }

    // Login Page
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.onsubmit = async (e) => {
            e.preventDefault();
            const formData = new FormData(loginForm);
            const data = new URLSearchParams(formData);

            const res = await fetch(`${API_URL}/token`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: data
            });

            if (res.ok) {
                const json = await res.json();
                localStorage.setItem('token', json.access_token);
                localStorage.setItem('role', json.role); // Server sends role
                window.location.href = json.role === 'admin' ? '/admin.html' : '/dashboard.html';
            } else {
                alert('Login failed. Check credentials.');
            }
        };
    }

    // Register Page
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.onsubmit = async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            const res = await fetch(`${API_URL}/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password })
            });

            if (res.ok) {
                alert('Registration successful! Please login.');
                window.location.href = '/login.html';
            } else {
                const err = await res.json();
                alert('Registration failed: ' + err.detail);
            }
        };
    }

    // Dashboard Page
    if (window.location.pathname.endsWith('dashboard.html')) {
        if (!getToken()) window.location.href = '/login.html';
        loadDashboard();

        const uploadArea = document.getElementById('upload-area');
        const fileInput = document.getElementById('file-input');
        const scanBtn = document.getElementById('scan-btn');
        const cancelBtn = document.getElementById('cancel-upload');

        uploadArea.onclick = () => fileInput.click();
        fileInput.onchange = handleFileSelection;
        scanBtn.onclick = performScan;
        cancelBtn.onclick = cancelSelection;
    }

    // Forgot Password Page
    const forgotForm = document.getElementById('forgot-password-form');
    if (forgotForm) {
        forgotForm.onsubmit = async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const res = await fetch(`${API_URL}/forgot-password`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email })
            });
            const data = await res.json();
            const msgEl = document.getElementById('recovery-message');
            msgEl.innerText = data.message;
            msgEl.style.display = 'block';

            const proceedArea = document.getElementById('proceed-area');
            if (proceedArea) {
                proceedArea.style.display = 'block';
            }
        };
    }

    // Reset Password Page
    const resetForm = document.getElementById('reset-password-form');
    if (resetForm) {
        resetForm.onsubmit = async (e) => {
            e.preventDefault();
            const otp = document.getElementById('otp-input').value;
            const newPassword = document.getElementById('new-password').value;
            const confirmPassword = document.getElementById('confirm-password').value;

            if (newPassword !== confirmPassword) {
                alert("Passwords do not match!");
                return;
            }

            const res = await fetch(`${API_URL}/reset-password`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ otp: otp, new_password: newPassword })
            });

            if (res.ok) {
                alert("Password updated successfully! Please login.");
                window.location.href = '/login.html';
            } else {
                const err = await res.json();
                alert("Reset failed: " + err.detail);
            }
        };
    }

    // Admin Page
    if (window.location.pathname.endsWith('admin.html')) {
        if (!getToken()) window.location.href = '/login.html';
        // Simple client-side role check, server enforces real security
        if (getRole() !== 'admin') {
            alert('Access Denied');
            window.location.href = '/dashboard.html';
        }
        loadAdmin();
    }

    // Modal Close Logic
    const modal = document.getElementById('details-modal');
    const closeBtn = document.querySelector('.close-modal');
    if (modal && closeBtn) {
        closeBtn.onclick = () => modal.style.display = 'none';
        window.onclick = (e) => {
            if (e.target == modal) modal.style.display = 'none';
        };
    }
});

// ================= DASHBOARD FUNCTIONS =================

async function handleFileSelection(e) {
    const file = e.target.files[0];
    if (!file) return;

    selectedFile = file;
    document.getElementById('selected-filename').innerText = file.name;
    document.getElementById('file-actions').style.display = 'block';
    document.getElementById('upload-area').style.display = 'none';
}

function cancelSelection() {
    selectedFile = null;
    document.getElementById('file-input').value = '';
    document.getElementById('file-actions').style.display = 'none';
    document.getElementById('upload-area').style.display = 'block';
}

async function performScan() {
    if (!selectedFile) {
        alert("No file selected!");
        return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    const btn = document.getElementById('scan-btn');
    const originalText = btn.innerText;
    btn.innerText = "Scanning...";
    btn.disabled = true;

    const res = await apiRequest('/scan', 'POST', formData, true);

    btn.innerText = originalText;
    btn.disabled = false;

    if (res && res.ok) {
        alert('Scan Complete!');
        loadDashboard(); // Refresh data
        cancelSelection(); // Reset UI
    } else if (res) {
        const err = await res.json();
        alert('Scan failed: ' + (err.detail || 'Internal Server Error'));
    } else {
        alert('Scan failed: Could not connect to server.');
    }
}

async function loadDashboard() {
    const res = await apiRequest('/history');
    if (res && res.ok) {
        const history = await res.json();
        currentScanHistory = history;
        renderHistoryTable(history);
        updateStats(history);
    }
}

function updateStats(history) {
    if (!history.length) return;
    const latest = history[0]; // Assuming sorted by date desc

    document.getElementById('total-deps').innerText = latest.total_dependencies;
    document.getElementById('vuln-found').innerText = latest.vulnerabilities_count;

    renderChart(latest.total_dependencies, latest.vulnerabilities_count);
}

// Global theme change listener for chart refresh
window.addEventListener('storage', (e) => {
    if (e.key === 'theme') {
        const history = currentScanHistory[0];
        if (history) renderChart(history.total_dependencies, history.vulnerabilities_count);
    }
});

function renderHistoryTable(history) {
    const tbody = document.getElementById('history-body');
    tbody.innerHTML = '';

    history.forEach(scan => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${new Date(scan.scan_date).toLocaleDateString()}</td>
            <td>${scan.filename}</td>
            <td>${scan.total_dependencies}</td>
            <td>
                <span class="badge ${scan.vulnerabilities_count > 0 ? 'badge-danger' : 'badge-success'}">
                    ${scan.vulnerabilities_count} Issues
                </span>
            </td>
            <td>
                <button onclick="viewDetails(${scan.id})" class="btn-sm btn-info" style="margin-right: 0.5rem;">Details</button>
                <button onclick="downloadPDF(${scan.id}, '${scan.filename}')" class="btn-sm btn-primary">PDF</button>
                <button onclick="deleteScan(${scan.id})" class="btn-sm btn-danger">Delete</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function deleteScan(id) {
    if (!confirm('Delete this scan?')) return;
    const res = await apiRequest(`/history/${id}`, 'DELETE');
    if (res.ok) loadDashboard();
}

async function downloadPDF(id, filename) {
    const token = getToken();
    const res = await fetch(`${API_URL}/scan/${id}/pdf`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    if (res.ok) {
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `report_${filename}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    } else {
        alert('Failed to download PDF');
    }
}

function viewDetails(id) {
    const scan = currentScanHistory.find(s => s.id === id);
    if (!scan) return;

    const modal = document.getElementById('details-modal');
    const tbody = document.getElementById('details-body');
    tbody.innerHTML = '';

    let details = [];
    try {
        details = JSON.parse(scan.details);
    } catch (e) {
        console.error("Failed to parse details", e);
    }

    if (details.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;">No vulnerabilities found. safe!</td></tr>';
    } else {
        details.forEach(vuln => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${vuln.artifact_id}</td>
                <td style="color: var(--danger); font-weight: bold;">${vuln.type || 'Unknown'}</td>
                <td><span class="badge badge-danger">${vuln.severity}</span></td>
                <td>${vuln.description}</td>
            `;
            tbody.appendChild(tr);
        });
    }

    modal.style.display = 'block';
}

let scanChart = null;

function renderChart(total, vulns) {
    const ctx = document.getElementById('scanChart');
    if (!ctx) return;

    if (scanChart) {
        scanChart.destroy();
    }

    const safe = Math.max(0, total - vulns);

    const style = getComputedStyle(document.documentElement);
    const primary = style.getPropertyValue('--primary-color').trim();
    const danger = style.getPropertyValue('--danger').trim();
    const textMuted = style.getPropertyValue('--text-muted').trim();

    scanChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Safe', 'Vulnerabilities'],
            datasets: [{
                data: [safe, vulns],
                backgroundColor: [
                    primary + '33', // Add alpha (0.2 approx in hex)
                    danger + '80'    // Add alpha (0.5 approx in hex)
                ],
                borderColor: [
                    primary,
                    danger
                ],
                borderWidth: 2,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: textMuted,
                        font: {
                            family: "'JetBrains Mono', monospace"
                        }
                    }
                }
            },
            elements: {
                arc: {
                    shadowBlur: 10,
                    shadowColor: primary
                }
            }
        }
    });
}


// ================= ADMIN FUNCTIONS =================

async function loadAdmin() {
    loadUsers();
    loadAllScans();
}

async function loadUsers() {
    const res = await apiRequest('/admin/users');
    if (res && res.ok) {
        const users = await res.json();
        const tbody = document.getElementById('users-body');
        tbody.innerHTML = '';
        users.forEach(user => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${user.id}</td>
                <td>${user.username}</td>
                <td>${user.email}</td>
                <td>${user.role}</td>
                <td><button onclick="deleteUser(${user.id})" class="btn-sm btn-danger">Delete</button></td>
            `;
            tbody.appendChild(tr);
        });
    }
}

async function deleteUser(id) {
    if (!confirm('Delete this user?')) return;
    const res = await apiRequest(`/admin/users/${id}`, 'DELETE');
    if (res.ok) loadUsers();
}

async function loadAllScans() {
    const res = await apiRequest('/admin/scans');
    if (res && res.ok) {
        const scans = await res.json();
        const tbody = document.getElementById('all-scans-body');
        tbody.innerHTML = '';
        scans.forEach(scan => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${scan.id}</td>
                <td>User ID: ${scan.user_id}</td>
                <td>${scan.filename}</td>
                <td>${scan.vulnerabilities_count}</td>
                <td><button onclick="deleteScanAdmin(${scan.id})" class="btn-sm btn-danger">Delete</button></td>
            `;
            tbody.appendChild(tr);
        });
    }
}

async function deleteScanAdmin(id) {
    if (!confirm('Delete this scan?')) return;
    const res = await apiRequest(`/admin/scans/${id}`, 'DELETE');
    if (res.ok) loadAllScans();
}

// ================= VISUAL EFFECTS =================

function initMatrixEffect() {
    const canvas = document.createElement('canvas');
    canvas.id = 'matrix-canvas';
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.zIndex = '-1';
    canvas.style.opacity = '0.3'; // Adjust visibility
    canvas.style.pointerEvents = 'none';
    document.body.appendChild(canvas);

    const ctx = canvas.getContext('2d');
    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;

    const columns = Math.floor(width / 20);
    const drops = Array(columns).fill(1);

    const chars = '01'; // Binary

    const getThemeColors = () => {
        const style = getComputedStyle(document.documentElement);
        return {
            bg: style.getPropertyValue('--bg-color').trim(),
            text: style.getPropertyValue('--primary-color').trim()
        };
    };

    function draw() {
        const colors = getThemeColors();

        // Trail effect
        ctx.globalAlpha = 0.05;
        ctx.fillStyle = colors.bg;
        ctx.fillRect(0, 0, width, height);
        ctx.globalAlpha = 1.0;

        ctx.fillStyle = colors.text; // Use primary theme color
        ctx.font = '15px "JetBrains Mono", monospace';

        for (let i = 0; i < drops.length; i++) {
            const text = chars.charAt(Math.floor(Math.random() * chars.length));
            ctx.fillText(text, i * 20, drops[i] * 20);

            if (drops[i] * 20 > height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    }

    window.addEventListener('resize', () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    });

    setInterval(draw, 50);
}
