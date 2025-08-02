// Authentication JavaScript for Learning Path Generator

class AuthManager {
    constructor() {
        this.baseURL = '/api';
        this.token = localStorage.getItem('access_token');
        this.refreshToken = localStorage.getItem('refresh_token');
        this.user = JSON.parse(localStorage.getItem('user') || 'null');
        
        // Set up axios defaults
        if (this.token) {
            axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`;
        }
        
        // Set up axios interceptors for token refresh
        this.setupAxiosInterceptors();
        
        // Initialize auth state
        this.updateAuthUI();
    }
    
    setupAxiosInterceptors() {
        // Request interceptor
        axios.interceptors.request.use(
            (config) => {
                if (this.token) {
                    config.headers.Authorization = `Bearer ${this.token}`;
                }
                return config;
            },
            (error) => {
                return Promise.reject(error);
            }
        );
        
        // Response interceptor for token refresh
        axios.interceptors.response.use(
            (response) => response,
            async (error) => {
                const originalRequest = error.config;
                
                if (error.response?.status === 401 && !originalRequest._retry) {
                    originalRequest._retry = true;
                    
                    try {
                        await this.refreshAccessToken();
                        originalRequest.headers.Authorization = `Bearer ${this.token}`;
                        return axios(originalRequest);
                    } catch (refreshError) {
                        this.logout();
                        return Promise.reject(refreshError);
                    }
                }
                
                return Promise.reject(error);
            }
        );
    }
    
    async login(username, password) {
        try {
            const response = await axios.post(`${this.baseURL}/auth/login/`, {
                username,
                password
            });
            
            const { access, refresh, user, first_login } = response.data;
            
            this.token = access;
            this.refreshToken = refresh;
            this.user = user;
            
            // Store in localStorage
            localStorage.setItem('access_token', access);
            localStorage.setItem('refresh_token', refresh);
            localStorage.setItem('user', JSON.stringify(user));
            
            // Update axios default headers
            axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;
            
            this.updateAuthUI();
            
            return { success: true, user, first_login };
        } catch (error) {
            console.error('Login error:', error);
            return { 
                success: false, 
                error: error.response?.data?.detail || 'Login failed' 
            };
        }
    }
    
    async register(userData) {
        try {
            const response = await axios.post(`${this.baseURL}/auth/register/`, userData);
            return { success: true, data: response.data };
        } catch (error) {
            console.error('Registration error:', error);
            return { 
                success: false, 
                error: error.response?.data || 'Registration failed' 
            };
        }
    }
    
    async refreshAccessToken() {
        if (!this.refreshToken) {
            throw new Error('No refresh token available');
        }
        
        try {
            const response = await axios.post(`${this.baseURL}/auth/refresh/`, {
                refresh: this.refreshToken
            });
            
            this.token = response.data.access;
            localStorage.setItem('access_token', this.token);
            axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`;
            
            return this.token;
        } catch (error) {
            console.error('Token refresh error:', error);
            throw error;
        }
    }
    
    logout() {
        this.token = null;
        this.refreshToken = null;
        this.user = null;
        
        // Clear localStorage
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        
        // Clear axios default headers
        delete axios.defaults.headers.common['Authorization'];
        
        this.updateAuthUI();
        
        // Redirect to home page
        window.location.href = '/';
    }
    
    isAuthenticated() {
        return !!this.token && !!this.user;
    }
    
    getUser() {
        return this.user;
    }
    
    updateAuthUI() {
        const navbarAuth = document.getElementById('navbar-auth');
        if (!navbarAuth) return;
        
        if (this.isAuthenticated()) {
            navbarAuth.innerHTML = `
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown">
                        <i class="fas fa-user me-1"></i>${this.user.username}
                    </a>
                    <ul class="dropdown-menu dropdown-menu-end">
                        <li><a class="dropdown-item" href="/dashboard/"><i class="fas fa-tachometer-alt me-2"></i>Dashboard</a></li>
                        <li><a class="dropdown-item" href="/profile/"><i class="fas fa-user-edit me-2"></i>Profile</a></li>
                        <li><a class="dropdown-item" href="/my-learning-paths/"><i class="fas fa-route me-2"></i>My Learning Paths</a></li>
                        <li><a class="dropdown-item" href="/my-courses/"><i class="fas fa-book me-2"></i>My Courses</a></li>
                        <li><hr class="dropdown-divider"></li>
                        <li><a class="dropdown-item" href="#" onclick="auth.logout()"><i class="fas fa-sign-out-alt me-2"></i>Logout</a></li>
                    </ul>
                </li>
            `;
        } else {
            navbarAuth.innerHTML = `
                <li class="nav-item">
                    <a class="nav-link" href="/login/">
                        <i class="fas fa-sign-in-alt me-1"></i>Login
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/register/">
                        <i class="fas fa-user-plus me-1"></i>Register
                    </a>
                </li>
            `;
        }
    }
    
    async getDashboard() {
        try {
            const response = await axios.get(`${this.baseURL}/auth/dashboard/`);
            return { success: true, data: response.data };
        } catch (error) {
            console.error('Dashboard error:', error);
            return { success: false, error: error.response?.data || 'Failed to load dashboard' };
        }
    }
    
    async updateProfile(profileData) {
        try {
            const response = await axios.patch(`${this.baseURL}/profiles/update_me/`, profileData);
            return { success: true, data: response.data };
        } catch (error) {
            console.error('Profile update error:', error);
            return { success: false, error: error.response?.data || 'Failed to update profile' };
        }
    }
    
    async changePassword(passwordData) {
        try {
            const response = await axios.post(`${this.baseURL}/profiles/change_password/`, passwordData);
            return { success: true, data: response.data };
        } catch (error) {
            console.error('Password change error:', error);
            return { success: false, error: error.response?.data || 'Failed to change password' };
        }
    }
}

// Initialize auth manager
const auth = new AuthManager();

// Login form handler
function handleLogin(event) {
    event.preventDefault();
    
    const form = event.target;
    const username = form.username.value;
    const password = form.password.value;
    
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Logging in...';
    submitBtn.disabled = true;
    
    auth.login(username, password).then(result => {
        if (result.success) {
            showAlert('Login successful! Redirecting...', 'success');
            
            // Check if there's a next parameter in the URL
            const urlParams = new URLSearchParams(window.location.search);
            const nextUrl = urlParams.get('next');
            
            setTimeout(() => {
                if (nextUrl) {
                    window.location.href = nextUrl;
                } else if (result.first_login) {
                    window.location.href = '/';
                } else {
                    window.location.href = '/dashboard/';
                }
            }, 1000);
        } else {
            showAlert(result.error, 'danger');
        }
    }).finally(() => {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    });
}

// Register form handler
function handleRegister(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const userData = Object.fromEntries(formData.entries());
    
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Creating account...';
    submitBtn.disabled = true;
    
    auth.register(userData).then(result => {
        if (result.success) {
            showAlert('Account created successfully! Please login.', 'success');
            setTimeout(() => {
                window.location.href = '/login/';
            }, 2000);
        } else {
            let errorMessage = 'Registration failed';
            if (typeof result.error === 'object') {
                errorMessage = Object.values(result.error).flat().join(' ');
            } else {
                errorMessage = result.error;
            }
            showAlert(errorMessage, 'danger');
        }
    }).finally(() => {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    });
}

// Utility function to show alerts
function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alert-container') || document.body;
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    if (alertContainer === document.body) {
        alertDiv.style.position = 'fixed';
        alertDiv.style.top = '100px';
        alertDiv.style.left = '50%';
        alertDiv.style.transform = 'translateX(-50%)';
        alertDiv.style.zIndex = '9999';
        alertDiv.style.minWidth = '300px';
    }
    
    alertContainer.appendChild(alertDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Require authentication for certain pages
function requireAuth() {
    if (!auth.isAuthenticated()) {
        showAlert('Please login to access this page.', 'warning');
        setTimeout(() => {
            window.location.href = '/login/';
        }, 2000);
        return false;
    }
    return true;
}
