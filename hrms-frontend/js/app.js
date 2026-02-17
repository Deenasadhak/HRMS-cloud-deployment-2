const API_BASE_URL = "http://127.0.0.1:8000";

// --- State Management ---
const state = {
    currentView: 'dashboard',
    theme: localStorage.getItem('theme') || 'light'
};

// --- DOM Elements ---
const contentArea = document.getElementById('content-area');
const pageTitle = document.getElementById('page-title');
const themeToggle = document.getElementById('theme-toggle');
const sidebarItems = document.querySelectorAll('.menu-item');
const addEmployeeBtn = document.getElementById('add-employee-btn');
const modalContainer = document.getElementById('modal-container');
const modalTitle = document.getElementById('modal-title');
const modalBody = document.getElementById('modal-body');
const closeModalBtn = document.getElementById('close-modal');
const toast = document.getElementById('toast');

// --- Initialization ---
document.addEventListener('DOMContentLoaded', () => {
    applyTheme();
    loadView('dashboard');

    themeToggle.addEventListener('click', toggleTheme);
    closeModalBtn.addEventListener('click', closeModal);
    
    sidebarItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            // Remove active class from all
            sidebarItems.forEach(i => i.classList.remove('active'));
            // Add active to clicked (or parent if icon clicked)
            const target = e.currentTarget;
            target.classList.add('active');
            
            const view = target.getAttribute('data-target');
            loadView(view);
        });
    });

    addEmployeeBtn.addEventListener('click', () => {
        openEmployeeModal();
    });
});

// --- Theme Handling ---
function toggleTheme() {
    state.theme = state.theme === 'light' ? 'dark' : 'light';
    localStorage.setItem('theme', state.theme);
    applyTheme();
}

function applyTheme() {
    document.documentElement.setAttribute('data-theme', state.theme);
    const icon = themeToggle.querySelector('ion-icon');
    icon.setAttribute('name', state.theme === 'light' ? 'moon-outline' : 'sunny-outline');
}

// --- Navigation & Router ---
async function loadView(view) {
    state.currentView = view;
    
    // Reset Header Actions
    addEmployeeBtn.style.display = 'none';

    // Show Loading
    renderLoading();

    try {
        switch(view) {
            case 'dashboard':
                pageTitle.textContent = 'Dashboard';
                await renderDashboard();
                break;
            case 'employees':
                pageTitle.textContent = 'Employees';
                addEmployeeBtn.style.display = 'inline-flex';
                await renderEmployees();
                break;
            case 'attendance':
                pageTitle.textContent = 'Attendance';
                contentArea.innerHTML = '<div class="card"><h3>Coming Soon</h3><p>Attendance module implementation needed.</p></div>';
                break;
            case 'leaves':
                pageTitle.textContent = 'Leaves';
                contentArea.innerHTML = '<div class="card"><h3>Coming Soon</h3><p>Leaves management implementation needed.</p></div>';
                break;
            case 'payroll':
                pageTitle.textContent = 'Payroll';
                contentArea.innerHTML = '<div class="card"><h3>Coming Soon</h3><p>Payroll module implementation needed.</p></div>';
                break;
            case 'settings':
                pageTitle.textContent = 'Settings';
                contentArea.innerHTML = '<div class="card"><h3>App Settings</h3><p>Theme: ' + state.theme + '</p></div>';
                break;
            default:
                renderDashboard();
        }
    } catch (error) {
        console.error("Error loading view:", error);
        showToast("Error loading data", "error");
        contentArea.innerHTML = `<div class="card" style="border-color: var(--danger-color); color: var(--danger-color);">
            <h3>Error</h3>
            <p>Could not connect to the backend. Is it running?</p>
            <small>${error.message}</small>
        </div>`;
    }
}

// --- API Service ---
async function fetchData(endpoint) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`);
    if (!response.ok) throw new Error(`API Error: ${response.status}`);
    return await response.json();
}

async function postData(endpoint, data) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || 'Failed to submit');
    }
    return await response.json();
}

// --- View Renderers ---

function renderLoading() {
    contentArea.innerHTML = `
        <div class="loading-state">
            <div class="spinner"></div>
            <p>Loading data...</p>
        </div>
    `;
}

async function renderDashboard() {
    // Ideally fetch stats from a dashboard API
    // For now, we'll fetch basic counts manually
    const employees = await fetchData('/employees/');
    
    const stats = [
        { label: 'Total Employees', value: employees.length, icon: 'people-outline' },
        { label: 'On Leave Today', value: '0', icon: 'airplane-outline' }, // Placeholder
        { label: 'Present Today', value: employees.length, icon: 'checkmark-circle-outline' }, // Placeholder
        { label: 'New Hires (Month)', value: '2', icon: 'trending-up-outline' } // Placeholder
    ];

    let cardsHtml = '<div class="grid-cards">';
    stats.forEach(stat => {
        cardsHtml += `
            <div class="card stat-card">
                <div>
                    <div class="stat-value">${stat.value}</div>
                    <div class="stat-label">${stat.label}</div>
                </div>
                <div class="stat-icon">
                    <ion-icon name="${stat.icon}"></ion-icon>
                </div>
            </div>
        `;
    });
    cardsHtml += '</div>';
    
    cardsHtml += `
        <div class="card">
            <h3>Recent Activity</h3>
            <p style="color: var(--text-secondary); margin-top: 10px;">System initialized successfully.</p>
        </div>
    `;

    contentArea.innerHTML = cardsHtml;
}

async function renderEmployees() {
    const employees = await fetchData('/employees/');
    
    if (employees.length === 0) {
        contentArea.innerHTML = `
            <div class="loading-state">
                <ion-icon name="people-outline" style="font-size: 4rem; color: var(--text-secondary); margin-bottom: 1rem;"></ion-icon>
                <h3>No Employees Found</h3>
                <p>Click "Add Employee" to get started.</p>
            </div>
        `;
        return;
    }

    let tableHtml = `
        <div class="table-container">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Designation</th>
                        <th>Department</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
    `;

    employees.forEach(emp => {
        tableHtml += `
            <tr>
                <td>#${emp.id}</td>
                <td>
                    <div style="font-weight: 500;">${emp.first_name} ${emp.last_name}</div>
                    <div style="font-size: 0.75rem; color: var(--text-secondary);">${emp.phone || '-'}</div>
                </td>
                <td>${emp.designation || 'N/A'}</td>
                <td><span class="badge badge-neutral">Engineering</span></td> <!-- Placeholder for Dept -->
                <td><span class="badge badge-success">Active</span></td>
                <td>
                    <button class="icon-btn" style="width: 28px; height: 28px;" title="View Details">
                        <ion-icon name="eye-outline"></ion-icon>
                    </button>
                </td>
            </tr>
        `;
    });

    tableHtml += `
                </tbody>
            </table>
        </div>
    `;

    contentArea.innerHTML = tableHtml;
}

// --- Modals & Forms ---
function closeModal() {
    modalContainer.classList.remove('open');
}

function openEmployeeModal() {
    modalTitle.textContent = "Add New Employee";
    modalBody.innerHTML = `
        <form id="add-employee-form">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div class="form-group">
                    <label class="form-label">First Name</label>
                    <input type="text" name="first_name" class="form-input" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Last Name</label>
                    <input type="text" name="last_name" class="form-input" required>
                </div>
            </div>
            
            <div class="form-group">
                <label class="form-label">Designation</label>
                <input type="text" name="designation" class="form-input">
            </div>

            <div class="form-group">
                <label class="form-label">Phone</label>
                <input type="tel" name="phone" class="form-input">
            </div>

            <div class="form-group">
                <label class="form-label">Address</label>
                <textarea name="address" class="form-input" rows="2"></textarea>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div class="form-group">
                    <label class="form-label">Date of Joining</label>
                    <input type="date" name="date_of_joining" class="form-input" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Basic Salary</label>
                    <input type="number" name="salary" class="form-input" required>
                </div>
            </div>

            <!-- Temporary hidden user_id until we implement auth dropdown -->
            <input type="hidden" name="user_id" value="1"> 
            
            <div style="display: flex; justify-content: flex-end; gap: 1rem; margin-top: 1rem;">
                <button type="button" class="btn" style="background: var(--bg-body);" onclick="closeModal()">Cancel</button>
                <button type="submit" class="btn btn-primary">Save Employee</button>
            </div>
        </form>
        <div class="alert" style="margin-top: 10px; font-size: 0.8rem; color: var(--warning-color);">
            Note: For this demo, User ID is hardcoded to 1. Ensure User ID 1 exists in backend or update code.
        </div>
    `;
    
    modalContainer.classList.add('open');

    document.getElementById('add-employee-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData.entries());
        
        // Convert numbers
        data.user_id = parseInt(data.user_id); 
        data.salary = parseFloat(data.salary);

        try {
            await postData('/employees/', data);
            showToast('Employee added successfully!');
            closeModal();
            loadView('employees'); // Refresh list
        } catch (error) {
            console.error(error);
            showToast(error.message, 'error');
        }
    });
}

// --- Toast ---
function showToast(message, type = 'success') {
    const toastMsg = document.getElementById('toast-message');
    const toastIcon = toast.querySelector('ion-icon');
    
    toastMsg.textContent = message;
    if (type === 'error') {
        toastIcon.setAttribute('name', 'alert-circle-outline');
        toast.style.color = '#ef4444'; // Red text for error
    } else {
        toastIcon.setAttribute('name', 'checkmark-circle-outline');
        toast.style.color = 'var(--bg-surface)'; // Default
    }

    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}
