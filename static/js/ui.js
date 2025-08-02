function createLearningPathCard(path, isMyPath = false) {
    const card = document.createElement('div');
    card.className = 'col';
    
    const difficultyColor = {
        'beginner': 'success',
        'intermediate': 'warning',
        'advanced': 'danger'
    };
    
    card.innerHTML = `
        <div class="card h-100 shadow-sm">
            <div class="card-body d-flex flex-column">
                <div class="mb-3">
                    <h5 class="card-title mb-2">${path.title}</h5>
                    <p class="card-text text-muted small">${path.description.length > 100 ? path.description.substring(0, 100) + '...' : path.description}</p>
                </div>
                <div class="mt-auto">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <span class="badge bg-${difficultyColor[path.difficulty_level] || 'primary'}">${path.difficulty_level}</span>
                        <small class="text-muted">
                            <i class="fas fa-clock me-1"></i>${path.estimated_duration_hours || 0}h
                        </small>
                    </div>
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">
                            <i class="fas fa-user me-1"></i>by ${path.creator?.username || 'Unknown'}
                        </small>
                        <a href="/learning-paths/${path.id}/" class="btn btn-sm btn-primary">
                            View Details
                        </a>
                    </div>
                </div>
            </div>
        </div>
    `;
    return card.outerHTML;
}

function createCourseCard(course, isMyCourse = false) {
    const card = document.createElement('div');
    card.className = 'col';
    
    const difficultyColor = {
        'beginner': 'success',
        'intermediate': 'warning',
        'advanced': 'danger'
    };
    
    const typeIcons = {
        'video': 'fas fa-play-circle',
        'text': 'fas fa-file-alt',
        'interactive': 'fas fa-laptop-code',
        'project': 'fas fa-project-diagram',
        'book': 'fas fa-book',
        'article': 'fas fa-newspaper',
        'tutorial': 'fas fa-chalkboard-teacher',
        'workshop': 'fas fa-users'
    };
    
    card.innerHTML = `
        <div class="card h-100 shadow-sm">
            <div class="card-body d-flex flex-column">
                <div class="mb-3">
                    <div class="d-flex align-items-center mb-2">
                        <i class="${typeIcons[course.course_type] || 'fas fa-book'} text-primary me-2"></i>
                        <h5 class="card-title mb-0">${course.title}</h5>
                    </div>
                    <p class="card-text text-muted small">${course.short_description}</p>
                </div>
                <div class="mt-auto">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <span class="badge bg-${difficultyColor[course.difficulty_level] || 'primary'}">${course.difficulty_level}</span>
                        <small class="text-muted">
                            <i class="fas fa-clock me-1"></i>${course.duration_hours || 0}h
                        </small>
                    </div>
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <small class="text-muted">
                            <i class="fas fa-graduation-cap me-1"></i>${course.platform || 'Platform'}
                        </small>
                        ${course.price > 0 ? 
                            `<span class="badge bg-info">$${course.price}</span>` : 
                            `<span class="badge bg-success">Free</span>`
                        }
                    </div>
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">
                            <i class="fas fa-user me-1"></i>by ${course.creator?.username || course.instructor || 'Unknown'}
                        </small>
                        <a href="/courses/${course.id}/" class="btn btn-sm btn-primary">
                            View Details
                        </a>
                    </div>
                </div>
            </div>
        </div>
    `;
    return card.outerHTML;
}

function createDashboardCard(title, value, icon, color = 'primary') {
    return `
        <div class="col-md-3 mb-4">
            <div class="card text-center h-100 shadow-sm">
                <div class="card-body">
                    <div class="mb-3">
                        <i class="${icon} fa-2x text-${color}"></i>
                    </div>
                    <h3 class="display-6 fw-bold">${value}</h3>
                    <p class="text-muted mb-0">${title}</p>
                </div>
            </div>
        </div>
    `;
}
