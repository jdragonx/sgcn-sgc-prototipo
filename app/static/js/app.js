// SGCN-SGC Frontend JavaScript
class SGCNApp {
    constructor() {
        this.apiBase = '/api';
        this.token = localStorage.getItem('token');
        this.user = JSON.parse(localStorage.getItem('user') || 'null');
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.checkAuth();
        this.loadDashboard();
    }

    setupEventListeners() {
        // Login form
        const loginForm = document.getElementById('loginForm');
        if (loginForm) {
            loginForm.addEventListener('submit', (e) => this.handleLogin(e));
        }

        // Logout button
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => this.logout());
        }

        // Navigation
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleNavigation(e);
            });
        });

        // Module buttons
        const moduleBtns = document.querySelectorAll('[data-module]');
        moduleBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                this.loadModule(e.target.dataset.module);
            });
        });
    }

    checkAuth() {
        if (!this.token) {
            this.showLogin();
            return;
        }
        this.showApp();
    }

    async handleLogin(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const username = formData.get('username');
        const password = formData.get('password');

        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `username=${username}&password=${password}`
            });

            if (response.ok) {
                const data = await response.json();
                this.token = data.access_token;
                this.user = data.user;
                localStorage.setItem('token', this.token);
                localStorage.setItem('user', JSON.stringify(this.user));
                this.showApp();
                this.showNotification('Login exitoso', 'success');
            } else {
                const error = await response.json();
                this.showNotification(error.detail || 'Error de autenticación', 'error');
            }
        } catch (error) {
            this.showNotification('Error de conexión', 'error');
        }
    }

    logout() {
        this.token = null;
        this.user = null;
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        this.showLogin();
        this.showNotification('Sesión cerrada', 'info');
    }

    showLogin() {
        document.getElementById('loginPage').classList.remove('hidden');
        document.getElementById('appPage').classList.add('hidden');
    }

    showApp() {
        document.getElementById('loginPage').classList.add('hidden');
        document.getElementById('appPage').classList.remove('hidden');
        this.updateUserInfo();
    }

    updateUserInfo() {
        const userInfo = document.getElementById('userInfo');
        if (userInfo && this.user) {
            userInfo.innerHTML = `
                <span class="text-sm text-gray-600">${this.user.full_name}</span>
                <span class="badge badge-info">${this.user.role}</span>
            `;
        }
    }

    handleNavigation(e) {
        const module = e.target.dataset.module;
        if (module) {
            // Update active nav link
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
            });
            e.target.classList.add('active');
            
            // Load module
            this.loadModule(module);
        }
    }

    async loadDashboard() {
        if (!this.token) return;

        try {
            const response = await fetch('/api/dashboard/stats', {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                this.renderDashboard(data);
            }
        } catch (error) {
            console.error('Error loading dashboard:', error);
        }
    }

    renderDashboard(data) {
        const statsContainer = document.getElementById('statsContainer');
        if (!statsContainer) return;

        statsContainer.innerHTML = `
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">${data.total_documents}</div>
                    <div class="stat-label">Documentos</div>
                    <div class="stat-change positive">${data.pending_documents} pendientes</div>
                </div>
                <div class="stat-card warning">
                    <div class="stat-value">${data.open_incidents}</div>
                    <div class="stat-label">Incidentes Abiertos</div>
                    <div class="stat-change">${data.total_incidents} total</div>
                </div>
                <div class="stat-card danger">
                    <div class="stat-value">${data.open_non_conformities}</div>
                    <div class="stat-label">No Conformidades</div>
                    <div class="stat-change">${data.total_non_conformities} total</div>
                </div>
                <div class="stat-card info">
                    <div class="stat-value">${data.planned_audits}</div>
                    <div class="stat-label">Auditorías Planificadas</div>
                    <div class="stat-change">${data.total_audits} total</div>
                </div>
            </div>
        `;

        // Render recent activities
        this.renderRecentActivities(data.recent_activities);
    }

    renderRecentActivities(activities) {
        const activitiesContainer = document.getElementById('activitiesContainer');
        if (!activitiesContainer) return;

        if (activities.length === 0) {
            activitiesContainer.innerHTML = '<p class="text-gray-500 text-center">No hay actividades recientes</p>';
            return;
        }

        const activitiesHTML = activities.map(activity => `
            <div class="flex items-center justify-between p-3 bg-white rounded-lg border">
                <div class="flex items-center gap-3">
                    <div class="w-2 h-2 rounded-full bg-${this.getActivityColor(activity.type)}"></div>
                    <div>
                        <div class="font-medium">${activity.title}</div>
                        <div class="text-sm text-gray-500">${activity.user}</div>
                    </div>
                </div>
                <div class="text-sm text-gray-400">
                    ${this.formatDate(activity.date)}
                </div>
            </div>
        `).join('');

        activitiesContainer.innerHTML = activitiesHTML;
    }

    getActivityColor(type) {
        const colors = {
            'document': 'blue',
            'incident': 'red',
            'non_conformity': 'orange',
            'audit': 'green'
        };
        return colors[type] || 'gray';
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffTime = Math.abs(now - date);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
        if (diffDays === 1) return 'Hoy';
        if (diffDays === 2) return 'Ayer';
        if (diffDays <= 7) return `Hace ${diffDays - 1} días`;
        
        return date.toLocaleDateString();
    }

    async loadModule(moduleName) {
        const dashboardContent = document.getElementById('dashboardContent');
        const mainContent = document.getElementById('mainContent');
        
        if (moduleName === 'dashboard') {
            dashboardContent.classList.remove('hidden');
            mainContent.classList.add('hidden');
            this.loadDashboard();
            return;
        }

        // Hide dashboard, show module content
        dashboardContent.classList.add('hidden');
        mainContent.classList.remove('hidden');
        mainContent.innerHTML = '<div class="loading"><div class="spinner"></div>Cargando...</div>';

        try {
            switch (moduleName) {
                case 'documents':
                    await this.loadDocuments();
                    break;
                case 'incidents':
                    await this.loadIncidents();
                    break;
                case 'non-conformities':
                    await this.loadNonConformities();
                    break;
                case 'audits':
                    await this.loadAudits();
                    break;
                case 'kpis':
                    await this.loadKPIs();
                    break;
                case 'business-continuity':
                    await this.loadBusinessContinuity();
                    break;
                default:
                    this.loadDashboard();
            }
        } catch (error) {
            mainContent.innerHTML = '<div class="alert alert-danger">Error al cargar el módulo</div>';
        }
    }

    async loadDocuments() {
        const response = await this.apiCall('/documents/');
        const content = document.getElementById('mainContent');
        
        content.innerHTML = `
            <div class="card">
                <div class="card-header">
                    <div class="flex justify-between items-center">
                        <h2 class="card-title">Gestión de Documentos</h2>
                        <button class="btn btn-primary" onclick="app.showDocumentForm()">
                            <span>+</span> Nuevo Documento
                        </button>
                    </div>
                </div>
                <div class="card-body">
                    <div class="table-container">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Título</th>
                                    <th>Tipo</th>
                                    <th>Versión</th>
                                    <th>Estado</th>
                                    <th>Fecha</th>
                                    <th>Acciones</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${response.map(doc => `
                                    <tr>
                                        <td>${doc.title}</td>
                                        <td><span class="badge badge-info">${doc.document_type}</span></td>
                                        <td>${doc.version}</td>
                                        <td><span class="badge badge-${this.getStatusColor(doc.status)}">${doc.status}</span></td>
                                        <td>${this.formatDate(doc.created_at)}</td>
                                        <td>
                                            <button class="btn btn-sm btn-secondary" onclick="app.viewDocument(${doc.id})">Ver</button>
                                            <button class="btn btn-sm btn-primary" onclick="app.editDocument(${doc.id})">Editar</button>
                                        </td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        `;
    }

    async loadIncidents() {
        const response = await this.apiCall('/incidents/');
        const content = document.getElementById('mainContent');
        
        content.innerHTML = `
            <div class="card">
                <div class="card-header">
                    <div class="flex justify-between items-center">
                        <h2 class="card-title">Gestión de Incidentes</h2>
                        <button class="btn btn-primary" onclick="app.showIncidentForm()">
                            <span>+</span> Nuevo Incidente
                        </button>
                    </div>
                </div>
                <div class="card-body">
                    <div class="table-container">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Título</th>
                                    <th>Tipo</th>
                                    <th>Prioridad</th>
                                    <th>Estado</th>
                                    <th>Fecha</th>
                                    <th>Acciones</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${response.map(incident => `
                                    <tr>
                                        <td>${incident.title}</td>
                                        <td><span class="badge badge-info">${incident.incident_type}</span></td>
                                        <td><span class="priority-${incident.priority}">${incident.priority.toUpperCase()}</span></td>
                                        <td><span class="badge badge-${this.getStatusColor(incident.status)}">${incident.status}</span></td>
                                        <td>${this.formatDate(incident.created_at)}</td>
                                        <td>
                                            <button class="btn btn-sm btn-secondary" onclick="app.viewIncident(${incident.id})">Ver</button>
                                            <button class="btn btn-sm btn-primary" onclick="app.editIncident(${incident.id})">Editar</button>
                                        </td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        `;
    }

    async loadNonConformities() {
        const response = await this.apiCall('/non-conformities/');
        const content = document.getElementById('mainContent');
        
        content.innerHTML = `
            <div class="card">
                <div class="card-header">
                    <div class="flex justify-between items-center">
                        <h2 class="card-title">No Conformidades</h2>
                        <button class="btn btn-primary" onclick="app.showNonConformityForm()">
                            <span>+</span> Nueva No Conformidad
                        </button>
                    </div>
                </div>
                <div class="card-body">
                    <div class="table-container">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Título</th>
                                    <th>Severidad</th>
                                    <th>Estado</th>
                                    <th>Ubicación</th>
                                    <th>Fecha</th>
                                    <th>Acciones</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${response.map(nc => `
                                    <tr>
                                        <td>${nc.title}</td>
                                        <td><span class="priority-${nc.severity}">${nc.severity.toUpperCase()}</span></td>
                                        <td><span class="badge badge-${this.getStatusColor(nc.status)}">${nc.status}</span></td>
                                        <td>${nc.location || 'N/A'}</td>
                                        <td>${this.formatDate(nc.created_at)}</td>
                                        <td>
                                            <button class="btn btn-sm btn-secondary" onclick="app.viewNonConformity(${nc.id})">Ver</button>
                                            <button class="btn btn-sm btn-primary" onclick="app.editNonConformity(${nc.id})">Editar</button>
                                        </td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        `;
    }

    async loadAudits() {
        const response = await this.apiCall('/audits/');
        const content = document.getElementById('mainContent');
        
        content.innerHTML = `
            <div class="card">
                <div class="card-header">
                    <div class="flex justify-between items-center">
                        <h2 class="card-title">Auditorías Internas</h2>
                        <button class="btn btn-primary" onclick="app.showAuditForm()">
                            <span>+</span> Nueva Auditoría
                        </button>
                    </div>
                </div>
                <div class="card-body">
                    <div class="table-container">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Título</th>
                                    <th>Tipo</th>
                                    <th>Estado</th>
                                    <th>Fecha Inicio</th>
                                    <th>Hallazgos</th>
                                    <th>Acciones</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${response.map(audit => `
                                    <tr>
                                        <td>${audit.title}</td>
                                        <td><span class="badge badge-info">${audit.audit_type}</span></td>
                                        <td><span class="badge badge-${this.getStatusColor(audit.status)}">${audit.status}</span></td>
                                        <td>${audit.planned_start_date ? this.formatDate(audit.planned_start_date) : 'N/A'}</td>
                                        <td>${audit.findings_count}</td>
                                        <td>
                                            <button class="btn btn-sm btn-secondary" onclick="app.viewAudit(${audit.id})">Ver</button>
                                            <button class="btn btn-sm btn-primary" onclick="app.editAudit(${audit.id})">Editar</button>
                                        </td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        `;
    }

    async loadKPIs() {
        const response = await this.apiCall('/kpis/');
        const content = document.getElementById('mainContent');
        
        content.innerHTML = `
            <div class="card">
                <div class="card-header">
                    <div class="flex justify-between items-center">
                        <h2 class="card-title">KPIs y Métricas</h2>
                        <button class="btn btn-primary" onclick="app.showKPIForm()">
                            <span>+</span> Nuevo KPI
                        </button>
                    </div>
                </div>
                <div class="card-body">
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        ${response.map(kpi => `
                            <div class="card">
                                <div class="card-body">
                                    <h3 class="font-semibold mb-2">${kpi.name}</h3>
                                    <p class="text-sm text-gray-600 mb-3">${kpi.description || 'Sin descripción'}</p>
                                    <div class="flex justify-between items-center">
                                        <span class="text-2xl font-bold text-primary">${kpi.target_value || 'N/A'}</span>
                                        <span class="badge badge-info">${kpi.measurement_unit}</span>
                                    </div>
                                    <div class="mt-2">
                                        <button class="btn btn-sm btn-secondary" onclick="app.viewKPI(${kpi.id})">Ver Detalles</button>
                                    </div>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }

    async loadBusinessContinuity() {
        const plansResponse = await this.apiCall('/business-continuity/plans/');
        const simulationsResponse = await this.apiCall('/business-continuity/simulations/');
        const content = document.getElementById('mainContent');
        
        content.innerHTML = `
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="card">
                    <div class="card-header">
                        <div class="flex justify-between items-center">
                            <h3 class="card-title">Planes de Continuidad</h3>
                            <button class="btn btn-primary btn-sm" onclick="app.showPlanForm()">
                                <span>+</span> Nuevo Plan
                            </button>
                        </div>
                    </div>
                    <div class="card-body">
                        ${plansResponse.map(plan => `
                            <div class="border rounded-lg p-4 mb-3">
                                <h4 class="font-semibold">${plan.title}</h4>
                                <p class="text-sm text-gray-600 mb-2">${plan.description || 'Sin descripción'}</p>
                                <div class="flex justify-between items-center">
                                    <span class="badge badge-${this.getStatusColor(plan.status)}">${plan.status}</span>
                                    <span class="text-sm text-gray-500">RTO: ${plan.rto_hours}h</span>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <div class="flex justify-between items-center">
                            <h3 class="card-title">Simulaciones de Emergencia</h3>
                            <button class="btn btn-primary btn-sm" onclick="app.showSimulationForm()">
                                <span>+</span> Nueva Simulación
                            </button>
                        </div>
                    </div>
                    <div class="card-body">
                        ${simulationsResponse.map(sim => `
                            <div class="border rounded-lg p-4 mb-3">
                                <h4 class="font-semibold">${sim.title}</h4>
                                <p class="text-sm text-gray-600 mb-2">${sim.scenario || 'Sin escenario'}</p>
                                <div class="flex justify-between items-center">
                                    <span class="badge badge-${this.getStatusColor(sim.status)}">${sim.status}</span>
                                    ${sim.success_rate ? `<span class="text-sm text-gray-500">${sim.success_rate}% éxito</span>` : ''}
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }

    getStatusColor(status) {
        const colors = {
            'open': 'warning',
            'closed': 'success',
            'completed': 'success',
            'approved': 'success',
            'pending_review': 'warning',
            'in_progress': 'info',
            'draft': 'gray',
            'active': 'success',
            'planned': 'info'
        };
        return colors[status] || 'gray';
    }

    async apiCall(endpoint, options = {}) {
        const url = endpoint.startsWith('http') ? endpoint : `${this.apiBase}${endpoint}`;
        const config = {
            headers: {
                'Authorization': `Bearer ${this.token}`,
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        const response = await fetch(url, config);
        
        if (!response.ok) {
            if (response.status === 401) {
                this.logout();
                throw new Error('No autorizado');
            }
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }

        return await response.json();
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} fixed top-4 right-4 z-50 max-w-sm`;
        notification.innerHTML = `
            <div class="flex justify-between items-center">
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" class="ml-4 text-lg">&times;</button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
    }

    // Placeholder methods for forms and detailed views
    showDocumentForm() { this.showNotification('Formulario de documento - En desarrollo', 'info'); }
    showIncidentForm() { this.showNotification('Formulario de incidente - En desarrollo', 'info'); }
    showNonConformityForm() { this.showNotification('Formulario de no conformidad - En desarrollo', 'info'); }
    showAuditForm() { this.showNotification('Formulario de auditoría - En desarrollo', 'info'); }
    showKPIForm() { this.showNotification('Formulario de KPI - En desarrollo', 'info'); }
    showPlanForm() { this.showNotification('Formulario de plan - En desarrollo', 'info'); }
    showSimulationForm() { this.showNotification('Formulario de simulación - En desarrollo', 'info'); }
    
    viewDocument(id) { this.showNotification(`Ver documento ${id} - En desarrollo`, 'info'); }
    editDocument(id) { this.showNotification(`Editar documento ${id} - En desarrollo`, 'info'); }
    viewIncident(id) { this.showNotification(`Ver incidente ${id} - En desarrollo`, 'info'); }
    editIncident(id) { this.showNotification(`Editar incidente ${id} - En desarrollo`, 'info'); }
    viewNonConformity(id) { this.showNotification(`Ver no conformidad ${id} - En desarrollo`, 'info'); }
    editNonConformity(id) { this.showNotification(`Editar no conformidad ${id} - En desarrollo`, 'info'); }
    viewAudit(id) { this.showNotification(`Ver auditoría ${id} - En desarrollo`, 'info'); }
    editAudit(id) { this.showNotification(`Editar auditoría ${id} - En desarrollo`, 'info'); }
    viewKPI(id) { this.showNotification(`Ver KPI ${id} - En desarrollo`, 'info'); }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new SGCNApp();
});
