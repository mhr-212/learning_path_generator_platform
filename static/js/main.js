// Main JavaScript for Learning Path Generator

class APIClient {
    constructor() {
        this.baseURL = '/api';
    }
    
    // Learning Paths API
    async getLearningPaths(params = {}) {
        try {
            const response = await axios.get(`${this.baseURL}/learning-paths/`, { params });
            return { success: true, data: response.data };
        } catch (error) {
            console.error('Error fetching learning paths:', error);
            return { success: false, error: error.response?.data || 'Failed to fetch learning paths' };
        }
    }
    
    async getLearningPath(id) {
        try {
            const response = await axios.get(`${this.baseURL}/learning-paths/${id}/`);
            return { success: true, data: response.data };
        } catch (error) {
            console.error('Error fetching learning path:', error);
            return { success: false, error: error.response?.data || 'Failed to fetch learning path' };
        }
    }
    
    async createLearningPath(data) {
        try {
            const response = await axios.post(`${this.baseURL}/learning-paths/`, data);
            return { success: true, data: response.data };
        } catch (error) {
            console.error('Error creating learning path:', error);
            return { success: false, error: error.response?.data || 'Failed to create learning path' };
        }
    }
    
    async updateLearningPath(id, data) {
        try {
            const response = await axios.patch(`${this.baseURL}/learning-paths/${id}/`, data);
            return { success: true, data: response.data };
        } catch (error) {
            console.error('Error updating learning path:', error);
            return { success: false, error: error.response?.data || 'Failed to update learning path' };
        }
    }
    
    async deleteLearningPath(id) {
        try {
            await axios.delete(`${this.baseURL}/learning-paths/${id}/`);
            return { success: true };
        } catch (error) {
            console.error('Error deleting learning path:', error);
            return { success: false, error: error.response?.data || 'Failed to delete learning path' };
        }
    }
    
    async startLearningPath(id) {
        try {
            const response = await axios.post(`${this.baseURL}/learning-paths/${id}/start_learning/`);
            return { success: true, data: response.data };
        } catch (error) {
            console.error('Error starting learning path:', error);
            return { success: false, error: error.response?.data || 'Failed to start learning path' };
        }
    }
    
    // Courses API
    async getCourses(params = {}) {
        try {
            const response = await axios.get(`${this.baseURL}/courses/`, { params });
            return { success: true, data: response.data };
        } catch (error) {
            console.error('Error fetching courses:', error);
            return { success: false, error: error.response?.data || 'Failed to fetch courses' };
        }
    }
    
    async getCourse(id) {
        try {
            const response = await axios.get(`${this.baseURL}/courses/${id}/`);
            return { success: true, data: response.data };
        } catch (error) {
            console.error('Error fetching course:', error);
            return { success: false, error: error.response?.data || 'Failed to fetch course' };
        }
    }
    
    async createCourse(data) {
        try {
            const response = await axios.post(`${this.baseURL}/courses/`, data);
            return { success: true, data: response.data };
        } catch (error) {
            console.error('Error creating course:', error);
            return { success: false, error: error.response?.data || 'Failed to create course' };
        }
    }
    
    async startCourse(id) {
        try {
            const response = await axios.post(`${this.baseURL}/courses/${id}/start_course/`);
            return { success: true, data: response.data };
        } catch (error) {
            console.error('Error starting course:', error);
            return { success: false, error: error.response?.data || 'Failed to start course' };
        }
    }
    
    // Categories API
    async getCategories() {
        try {
            const response = await axios.get(`${this.baseURL}/categories/`);
            return { success: true, data: response.data };
        } catch (error) {
            console.error('Error fetching categories:', error);
            return { success: false, error: error.response?.data || 'Failed to fetch categories' };
        }
    
    
    }
    // Fixed API endpoint
    async getMyLearningPaths(params = {}) {
        const response = await axios.get(`${this.baseURL}/learning-paths/my_paths/`, { params });
        // ...
    }

    // Stats API
    async getPublicStats() {
        try {
            const response = await axios.get(`${this.baseURL}/stats/`);
            return { success: true, data: response.data };
        } catch (error) {
            console.error('Error fetching stats:', error);
            return { success: false, error: error.response?.data || 'Failed to fetch stats' };
        }
    }
}

// Initialize API client
const api = new APIClient();

// Utility functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatDuration(hours) {
    if (hours < 1) {
        return `${Math.round(hours * 60)} minutes`;
    } else if (hours < 24) {
        return `${hours} hour${hours !== 1 ? 's' : ''}`;
    } else {
        const days = Math.floor(hours / 24);
        const remainingHours = hours % 24;
        let result = `${days} day${days !== 1 ? 's' : ''}`;
        if (remainingHours > 0) {
            result += ` ${remainingHours} hour${remainingHours !== 1 ? 's' : ''}`;
        }
        return result;
    }
}

function getDifficultyBadgeClass(difficulty) {
    switch (difficulty) {
        case 'beginner':
            return 'difficulty-beginner';
        case 'intermediate':
            return 'difficulty-intermediate';
        case 'advanced':
            return 'difficulty-advanced';
        default:
            return 'difficulty-beginner';
    }
}

function createLearningPathCard(learningPath) {
    const difficultyClass = getDifficultyBadgeClass(learningPath.difficulty_level);
    
    return `
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="card learning-path-card h-100">
                <div class="card-header">
                    <h5 class="card-title mb-0">${learningPath.title}</h5>
                    <small class="text-light opacity-75">by ${learningPath.creator.username}</small>
                </div>
                <div class="card-body">
                    <p class="card-text">${learningPath.description.substring(0, 150)}${learningPath.description.length > 150 ? '...' : ''}</p>
                    
                    <div class="mb-3">
                        <span class="difficulty-badge ${difficultyClass}">${learningPath.difficulty_level}</span>
                        <span class="badge bg-secondary ms-2">${learningPath.total_courses} courses</span>
                    </div>
                    
                    <div class="mb-3">
                        <small class="text-muted">
                            <i class="fas fa-clock me-1"></i>${formatDuration(learningPath.estimated_duration_hours)}
                        </small>
                    </div>
                    
                    ${learningPath.tag_list.length > 0 ? `
                        <div class="mb-3">
                            ${learningPath.tag_list.slice(0, 3).map(tag => `<span class="tag">${tag}</span>`).join('')}
                        </div>
                    ` : ''}
                    
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">${formatDate(learningPath.created_at)}</small>
                        <div>
                            <a href="/learning-paths/${learningPath.id}/" class="btn btn-primary btn-sm">View</a>
                            ${auth.isAuthenticated() ? `
                                <button class="btn btn-outline-primary btn-sm ms-1" onclick="startLearningPath(${learningPath.id})">
                                    <i class="fas fa-play"></i>
                                </button>
                            ` : ''}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function createCourseCard(course) {
    const difficultyClass = getDifficultyBadgeClass(course.difficulty_level);
    const priceClass = course.is_free ? 'free' : 'paid';
    const priceText = course.is_free ? 'Free' : `$${course.price}`;
    
    return `
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="card course-card h-100">
                <div class="card-body">
                    <h5 class="card-title">${course.title}</h5>
                    <p class="card-text">${course.short_description}</p>
                    
                    <div class="mb-3">
                        <span class="difficulty-badge ${difficultyClass}">${course.difficulty_level}</span>
                        <span class="course-type-badge ms-2">${course.course_type}</span>
                    </div>
                    
                    <div class="mb-3">
                        <small class="text-muted">
                            <i class="fas fa-clock me-1"></i>${formatDuration(course.duration_hours)}
                        </small>
                        ${course.instructor ? `
                            <br><small class="text-muted">
                                <i class="fas fa-user me-1"></i>${course.instructor}
                            </small>
                        ` : ''}
                        ${course.platform ? `
                            <br><small class="text-muted">
                                <i class="fas fa-external-link-alt me-1"></i>${course.platform}
                            </small>
                        ` : ''}
                    </div>
                    
                    ${course.rating ? `
                        <div class="mb-3">
                            <small class="text-warning">
                                ${'★'.repeat(Math.floor(course.rating))}${'☆'.repeat(5 - Math.floor(course.rating))}
                                ${course.rating.toFixed(1)} (${course.total_ratings} reviews)
                            </small>
                        </div>
                    ` : ''}
                    
                    <div class="d-flex justify-content-between align-items-center">
                        <span class="price-tag ${priceClass}">${priceText}</span>
                        <div>
                            <a href="/courses/${course.id}/" class="btn btn-primary btn-sm">View</a>
                            ${auth.isAuthenticated() ? `
                                <button class="btn btn-outline-primary btn-sm ms-1" onclick="startCourse(${course.id})">
                                    <i class="fas fa-play"></i>
                                </button>
                            ` : ''}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Action functions
async function startLearningPath(id) {
    if (!auth.isAuthenticated()) {
        showAlert('Please login to start learning paths.', 'warning');
        return;
    }
    
    const result = await api.startLearningPath(id);
    if (result.success) {
        showAlert('Learning path started successfully!', 'success');
    } else {
        showAlert(result.error.detail || 'Failed to start learning path', 'danger');
    }
}

async function startCourse(id) {
    if (!auth.isAuthenticated()) {
        showAlert('Please login to start courses.', 'warning');
        return;
    }
    
    const result = await api.startCourse(id);
    if (result.success) {
        showAlert('Course started successfully!', 'success');
    } else {
        showAlert(result.error.detail || 'Failed to start course', 'danger');
    }
}

// Search and filter functionality
function setupSearch(searchInputId, resultsContainerId, searchFunction) {
    const searchInput = document.getElementById(searchInputId);
    const resultsContainer = document.getElementById(resultsContainerId);
    
    if (!searchInput || !resultsContainer) return;
    
    let searchTimeout;
    
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            const query = this.value.trim();
            if (query.length >= 2) {
                searchFunction(query, resultsContainer);
            } else if (query.length === 0) {
                searchFunction('', resultsContainer);
            }
        }, 300);
    });
}

// Loading state management
function showLoading(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="loading-spinner">
                <div class="spinner-border" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
        `;
    }
}

function hideLoading(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        const spinner = container.querySelector('.loading-spinner');
        if (spinner) {
            spinner.remove();
        }
    }
}

// Initialize page-specific functionality
document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in animation to main content
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        mainContent.classList.add('fade-in');
    }
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});