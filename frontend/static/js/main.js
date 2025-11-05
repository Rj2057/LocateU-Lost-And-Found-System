function showTab(tabName) {
    
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    
    document.getElementById(tabName + '-tab').classList.add('active');
    event.target.classList.add('active');
}

function showForm(formType) {
    const container = event.target.closest('.auth-forms');
    
    
    container.querySelectorAll('.auth-form').forEach(form => {
        form.classList.remove('active');
    });
    
    
    container.querySelectorAll('.toggle-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    
    document.getElementById(formType + '-form').classList.add('active');
    event.target.classList.add('active');
}


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


document.addEventListener('DOMContentLoaded', function() {
    const FOUND_ITEMS = window.FOUND_ITEMS || [];

    function openModal() {
        document.getElementById('matchModal').style.display = 'block';
    }
    function closeModal() {
        document.getElementById('matchModal').style.display = 'none';
    }

    document.querySelectorAll('.btn-open-match').forEach(btn => {
        btn.addEventListener('click', function() {
            const lostId = this.dataset.lostId;
            const lostName = this.dataset.lostName || 'Selected lost item';
            document.getElementById('modalTitle').textContent = 'Match Lost Item';
            document.getElementById('modalLostName').textContent = `Lost: ${lostName} (ID ${lostId})`;

            const sel = document.getElementById('foundSelect');
            sel.innerHTML = '<option value="">-- choose found item --</option>';
            FOUND_ITEMS.forEach(fi => {
                if (fi.status && fi.status.toLowerCase() !== 'unclaimed') return;
                const opt = document.createElement('option');
                opt.value = fi.f_i_id;
                opt.textContent = `${fi.item_name} — ${fi.found_loc} (${fi.found_date})`;
                sel.appendChild(opt);
            });
            document.getElementById('confirmMatchBtn').dataset.lostId = lostId;
            openModal();
        });
    });

    document.getElementById('cancelMatch').addEventListener('click', e => {
        e.preventDefault();
        closeModal();
    });

    document.getElementById('confirmMatchBtn').addEventListener('click', async e => {
        e.preventDefault();
        const lostId = e.target.dataset.lostId;
        const foundId = document.getElementById('foundSelect').value;
        if (!foundId) return alert('Please choose a found item.');

        try {
            const resp = await fetch('/staff/confirm-match', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({lost_item_id: lostId, found_item_id: foundId})
            });
            const data = await resp.json();
            if (resp.ok && data.success) {
                alert('✅ Match recorded successfully!');
                location.reload();
            } else alert(data.message || 'Failed to record match');
        } catch (err) {
            console.error(err);
            alert('Server error.');
        } finally {
            closeModal();
        }
    });
});


function openImageModal(src) {
    const modal = document.getElementById('image-modal');
    const modalImg = document.getElementById('modal-img');
    modal.style.display = 'block';
    modalImg.src = src;
}

function closeImageModal() {
    document.getElementById('image-modal').style.display = 'none';
}


function showMessage(element, message, type) {
    element.textContent = message;
    element.className = `message ${type} show`;
    
    setTimeout(() => {
        element.classList.remove('show');
    }, 5000);
}


document.addEventListener('DOMContentLoaded', function() {
    const dateInputs = document.querySelectorAll('input[type="date"]');
    const today = new Date().toISOString().split('T')[0];
    dateInputs.forEach(input => {
        input.max = today;
        if (!input.value) input.value = today;
    });

    window.onclick = function(event) {
        const claimModal = document.getElementById('claim-modal');
        const imageModal = document.getElementById('image-modal');
        const matchModal = document.getElementById('matchModal');
        if (event.target === claimModal) closeClaimModal();
        if (event.target === imageModal) closeImageModal();
        if (event.target === matchModal) matchModal.style.display = 'none';
    };
});


function refreshNotifications() {
    fetch('/api/notifications')
        .then(res => res.json())
        .then(data => {
            if (data.success && data.notifications)
                console.log('Notifications refreshed');
        })
        .catch(err => console.error('Notification refresh error:', err));
}

if (window.location.pathname.includes('dashboard'))
    setInterval(refreshNotifications, 30000);
