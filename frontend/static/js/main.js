// ====================================
// FILE: frontend/static/js/main.js
// ====================================

// ====================================
// TAB AND FORM SWITCHING
// ====================================

function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(tabName + '-tab').classList.add('active');
    event.target.classList.add('active');
}

function showForm(formType) {
    const container = event.target.closest('.auth-forms');
    
    // Hide all forms
    container.querySelectorAll('.auth-form').forEach(form => {
        form.classList.remove('active');
    });
    
    // Remove active class from all toggle buttons
    container.querySelectorAll('.toggle-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected form
    document.getElementById(formType + '-form').classList.add('active');
    event.target.classList.add('active');
}

// ====================================
// AUTHENTICATION HANDLERS
// ====================================

async function handleStudentRegister(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const messageDiv = document.getElementById('student-register-message');
    
    try {
        const response = await fetch('/student/register', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage(messageDiv, data.message, 'success');
            form.reset();
            setTimeout(() => {
                showForm('student-login');
            }, 1500);
        } else {
            showMessage(messageDiv, data.message, 'error');
        }
    } catch (error) {
        showMessage(messageDiv, 'Registration failed. Please try again.', 'error');
    }
}

async function handleStudentLogin(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const messageDiv = document.getElementById('student-login-message');
    
    try {
        const response = await fetch('/student/login', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage(messageDiv, 'Login successful! Redirecting...', 'success');
            setTimeout(() => {
                window.location.href = data.redirect;
            }, 1000);
        } else {
            showMessage(messageDiv, data.message, 'error');
        }
    } catch (error) {
        showMessage(messageDiv, 'Login failed. Please try again.', 'error');
    }
}

async function handleStaffRegister(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const messageDiv = document.getElementById('staff-register-message');
    
    try {
        const response = await fetch('/staff/register', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage(messageDiv, data.message, 'success');
            form.reset();
            setTimeout(() => {
                showForm('staff-login');
            }, 1500);
        } else {
            showMessage(messageDiv, data.message, 'error');
        }
    } catch (error) {
        showMessage(messageDiv, 'Registration failed. Please try again.', 'error');
    }
}

async function handleStaffLogin(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const messageDiv = document.getElementById('staff-login-message');
    
    try {
        const response = await fetch('/staff/login', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage(messageDiv, 'Login successful! Redirecting...', 'success');
            setTimeout(() => {
                window.location.href = data.redirect;
            }, 1000);
        } else {
            showMessage(messageDiv, data.message, 'error');
        }
    } catch (error) {
        showMessage(messageDiv, 'Login failed. Please try again.', 'error');
    }
}

// ====================================
// REPORT ITEM HANDLERS
// ====================================

async function handleReportLost(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const messageDiv = document.getElementById('form-message');
    
    try {
        const response = await fetch('/student/report-lost', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage(messageDiv, data.message, 'success');
            form.reset();
            document.getElementById('image-preview').innerHTML = '';
            
            setTimeout(() => {
                window.location.href = '/student/dashboard';
            }, 2000);
        } else {
            showMessage(messageDiv, data.message, 'error');
        }
    } catch (error) {
        showMessage(messageDiv, 'Failed to report item. Please try again.', 'error');
    }
}

async function handleReportFound(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const messageDiv = document.getElementById('form-message');
    
    try {
        const response = await fetch('/student/report-found', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage(messageDiv, data.message, 'success');
            form.reset();
            document.getElementById('image-preview').innerHTML = '';
            
            setTimeout(() => {
                window.location.href = '/student/dashboard';
            }, 2000);
        } else {
            showMessage(messageDiv, data.message, 'error');
        }
    } catch (error) {
        showMessage(messageDiv, 'Failed to report item. Please try again.', 'error');
    }
}

// ====================================
// IMAGE PREVIEW
// ====================================

function previewImage(event) {
    const file = event.target.files[0];
    const preview = document.getElementById('image-preview');
    
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
        };
        reader.readAsDataURL(file);
    } else {
        preview.innerHTML = '';
    }
}

function previewProofImage(event) {
    const file = event.target.files[0];
    const preview = document.getElementById('proof-preview');
    
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.innerHTML = `<img src="${e.target.result}" alt="Proof Preview">`;
        };
        reader.readAsDataURL(file);
    } else {
        preview.innerHTML = '';
    }
}

// ====================================
// CLAIM ITEM HANDLERS
// ====================================

function openClaimModal(foundId, itemName) {
    document.getElementById('claim-found-id').value = foundId;
    document.getElementById('claim-item-name').textContent = `Claiming: ${itemName}`;
    document.getElementById('claim-modal').classList.add('show');
}

function closeClaimModal() {
    document.getElementById('claim-modal').classList.remove('show');
    document.getElementById('claim-form').reset();
    document.getElementById('proof-preview').innerHTML = '';
}

async function handleClaim(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const messageDiv = document.getElementById('claim-message');
    
    try {
        const response = await fetch('/student/claim-item', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage(messageDiv, data.message, 'success');
            setTimeout(() => {
                closeClaimModal();
                window.location.reload();
            }, 2000);
        } else {
            showMessage(messageDiv, data.message, 'error');
        }
    } catch (error) {
        showMessage(messageDiv, 'Failed to submit claim. Please try again.', 'error');
    }
}

// ====================================
// STAFF CLAIM VERIFICATION
// ====================================

async function verifyClaim(claimId, action) {
    const confirmed = confirm(`Are you sure you want to ${action} this claim?`);
    
    if (!confirmed) return;
    
    try {
        const response = await fetch(`/staff/verify-claim/${claimId}/${action}`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert(data.message);
            window.location.reload();
        } else {
            alert(data.message);
        }
    } catch (error) {
        alert('Failed to process claim. Please try again.');
    }
}

// ====================================
// IMAGE MODAL
// ====================================

function openImageModal(src) {
    const modal = document.getElementById('image-modal');
    const modalImg = document.getElementById('modal-img');
    modal.style.display = 'block';
    modalImg.src = src;
}

function closeImageModal() {
    document.getElementById('image-modal').style.display = 'none';
}

// ====================================
// UTILITY FUNCTIONS
// ====================================

function showMessage(element, message, type) {
    element.textContent = message;
    element.className = `message ${type} show`;
    
    setTimeout(() => {
        element.classList.remove('show');
    }, 5000);
}

// ====================================
// SET DEFAULT DATE TO TODAY
// ====================================

document.addEventListener('DOMContentLoaded', function() {
    // Set max date to today for date inputs
    const dateInputs = document.querySelectorAll('input[type="date"]');
    const today = new Date().toISOString().split('T')[0];
    
    dateInputs.forEach(input => {
        input.max = today;
        if (!input.value) {
            input.value = today;
        }
    });
    
    // Close modal when clicking outside
    window.onclick = function(event) {
        const claimModal = document.getElementById('claim-modal');
        const imageModal = document.getElementById('image-modal');
        
        if (event.target === claimModal) {
            closeClaimModal();
        }
        
        if (event.target === imageModal) {
            closeImageModal();
        }
    };
});

// ====================================
// NOTIFICATIONS AUTO-REFRESH (Optional)
// ====================================

function refreshNotifications() {
    fetch('/api/notifications')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.notifications) {
                // Update notification badge or list
                console.log('Notifications refreshed');
            }
        })
        .catch(error => console.error('Error refreshing notifications:', error));
}

// Refresh notifications every 30 seconds (if on dashboard)
if (window.location.pathname.includes('dashboard')) {
    setInterval(refreshNotifications, 30000);
}