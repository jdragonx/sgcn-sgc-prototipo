// Demo Script para presentación a directivos
class SGCN_Demo {
    constructor() {
        this.demoSteps = [
            {
                title: "🏢 Bienvenida al Sistema SGCN-SGC",
                description: "Sistema Integrado de Gestión de Calidad y Continuidad del Negocio",
                action: () => this.showWelcome()
            },
            {
                title: "🔐 Autenticación Segura",
                description: "Sistema de login con roles diferenciados",
                action: () => this.demoLogin()
            },
            {
                title: "📊 Dashboard Ejecutivo",
                description: "Métricas en tiempo real y estado del sistema",
                action: () => this.demoDashboard()
            },
            {
                title: "📄 Gestión de Documentos",
                description: "Control de versiones y aprobación de documentos",
                action: () => this.demoDocuments()
            },
            {
                title: "🚨 Gestión de Incidentes",
                description: "Manejo de eventos críticos con prioridades",
                action: () => this.demoIncidents()
            },
            {
                title: "⚠️ No Conformidades",
                description: "Registro y seguimiento de problemas",
                action: () => this.demoNonConformities()
            },
            {
                title: "🔍 Auditorías Internas",
                description: "Programación y documentación de auditorías",
                action: () => this.demoAudits()
            },
            {
                title: "📈 KPIs y Métricas",
                description: "Indicadores de desempeño del sistema",
                action: () => this.demoKPIs()
            },
            {
                title: "🔄 Continuidad del Negocio",
                description: "Planes y simulaciones de emergencia",
                action: () => this.demoBusinessContinuity()
            },
            {
                title: "🎯 Resumen y Beneficios",
                description: "Impacto en la organización y próximos pasos",
                action: () => this.showSummary()
            }
        ];
        
        this.currentStep = 0;
        this.isDemoMode = false;
    }

    startDemo() {
        this.isDemoMode = true;
        this.showDemoControls();
        this.executeStep(0);
    }

    showDemoControls() {
        const controls = document.createElement('div');
        controls.id = 'demoControls';
        controls.innerHTML = `
            <div style="position: fixed; top: 20px; right: 20px; z-index: 1000; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); min-width: 300px;">
                <h3 style="margin: 0 0 15px 0; color: #2563eb;">🎯 Demo SGCN-SGC</h3>
                <div style="margin-bottom: 15px;">
                    <div style="font-size: 14px; color: #666;">Paso ${this.currentStep + 1} de ${this.demoSteps.length}</div>
                    <div style="font-weight: 600; margin: 5px 0;">${this.demoSteps[this.currentStep].title}</div>
                    <div style="font-size: 12px; color: #888;">${this.demoSteps[this.currentStep].description}</div>
                </div>
                <div style="display: flex; gap: 10px;">
                    <button onclick="demo.prevStep()" style="padding: 8px 16px; background: #64748b; color: white; border: none; border-radius: 5px; cursor: pointer;">← Anterior</button>
                    <button onclick="demo.nextStep()" style="padding: 8px 16px; background: #2563eb; color: white; border: none; border-radius: 5px; cursor: pointer;">Siguiente →</button>
                </div>
                <div style="margin-top: 10px;">
                    <button onclick="demo.exitDemo()" style="padding: 6px 12px; background: #ef4444; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 12px;">Salir Demo</button>
                </div>
            </div>
        `;
        document.body.appendChild(controls);
    }

    nextStep() {
        if (this.currentStep < this.demoSteps.length - 1) {
            this.currentStep++;
            this.executeStep(this.currentStep);
        }
    }

    prevStep() {
        if (this.currentStep > 0) {
            this.currentStep--;
            this.executeStep(this.currentStep);
        }
    }

    executeStep(stepIndex) {
        const step = this.demoSteps[stepIndex];
        this.updateDemoControls();
        step.action();
    }

    updateDemoControls() {
        const controls = document.getElementById('demoControls');
        if (controls) {
            const step = this.demoSteps[this.currentStep];
            controls.innerHTML = `
                <div style="position: fixed; top: 20px; right: 20px; z-index: 1000; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); min-width: 300px;">
                    <h3 style="margin: 0 0 15px 0; color: #2563eb;">🎯 Demo SGCN-SGC</h3>
                    <div style="margin-bottom: 15px;">
                        <div style="font-size: 14px; color: #666;">Paso ${this.currentStep + 1} de ${this.demoSteps.length}</div>
                        <div style="font-weight: 600; margin: 5px 0;">${step.title}</div>
                        <div style="font-size: 12px; color: #888;">${step.description}</div>
                    </div>
                    <div style="display: flex; gap: 10px;">
                        <button onclick="demo.prevStep()" ${this.currentStep === 0 ? 'disabled' : ''} style="padding: 8px 16px; background: ${this.currentStep === 0 ? '#ccc' : '#64748b'}; color: white; border: none; border-radius: 5px; cursor: pointer;">← Anterior</button>
                        <button onclick="demo.nextStep()" ${this.currentStep === this.demoSteps.length - 1 ? 'disabled' : ''} style="padding: 8px 16px; background: ${this.currentStep === this.demoSteps.length - 1 ? '#ccc' : '#2563eb'}; color: white; border: none; border-radius: 5px; cursor: pointer;">Siguiente →</button>
                    </div>
                    <div style="margin-top: 10px;">
                        <button onclick="demo.exitDemo()" style="padding: 6px 12px; background: #ef4444; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 12px;">Salir Demo</button>
                    </div>
                </div>
            `;
        }
    }

    exitDemo() {
        this.isDemoMode = false;
        const controls = document.getElementById('demoControls');
        if (controls) {
            controls.remove();
        }
        // Volver al dashboard
        if (window.app) {
            window.app.loadModule('dashboard');
        }
    }

    showWelcome() {
        // Mostrar página de login
        if (window.app) {
            window.app.showLogin();
        }
        
        // Mostrar mensaje de bienvenida
        this.showNotification(`
            <div style="text-align: center; padding: 20px;">
                <h2 style="color: #2563eb; margin-bottom: 10px;">🏢 Bienvenido al Sistema SGCN-SGC</h2>
                <p style="color: #666; margin-bottom: 15px;">Sistema Integrado de Gestión de Calidad y Continuidad del Negocio</p>
                <div style="background: #f0f9ff; padding: 15px; border-radius: 8px; margin: 15px 0;">
                    <h4 style="color: #1e40af; margin: 0 0 10px 0;">✨ Características Principales</h4>
                    <ul style="text-align: left; margin: 0; padding-left: 20px; color: #374151;">
                        <li>Gestión completa de documentos ISO 9001/22301</li>
                        <li>Dashboard ejecutivo en tiempo real</li>
                        <li>Sistema de roles y permisos</li>
                        <li>API REST para integraciones</li>
                        <li>Interfaz responsive y moderna</li>
                    </ul>
                </div>
            </div>
        `, 'info', 8000);
    }

    demoLogin() {
        // Mostrar usuarios de prueba
        this.showNotification(`
            <div style="text-align: center; padding: 15px;">
                <h3 style="color: #2563eb; margin-bottom: 15px;">👥 Usuarios de Prueba</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; text-align: left;">
                    <div style="background: #f8fafc; padding: 10px; border-radius: 5px;">
                        <strong>admin / admin</strong><br>
                        <small>Administrador</small>
                    </div>
                    <div style="background: #f8fafc; padding: 10px; border-radius: 5px;">
                        <strong>auditor1 / auditor</strong><br>
                        <small>Auditor Interno</small>
                    </div>
                    <div style="background: #f8fafc; padding: 10px; border-radius: 5px;">
                        <strong>gestor1 / gestor</strong><br>
                        <small>Gestor de Procesos</small>
                    </div>
                    <div style="background: #f8fafc; padding: 10px; border-radius: 5px;">
                        <strong>operador1 / operador</strong><br>
                        <small>Operador Crítico</small>
                    </div>
                </div>
                <p style="margin-top: 15px; color: #666; font-size: 14px;">
                    💡 <strong>Tip:</strong> Usa admin/admin para acceso completo
                </p>
            </div>
        `, 'info', 10000);
    }

    demoDashboard() {
        // Auto-login como admin
        if (window.app && !window.app.token) {
            this.autoLogin();
        }
        
        setTimeout(() => {
            if (window.app) {
                window.app.loadModule('dashboard');
            }
            
            this.showNotification(`
                <div style="text-align: center; padding: 15px;">
                    <h3 style="color: #2563eb; margin-bottom: 10px;">📊 Dashboard Ejecutivo</h3>
                    <p style="color: #666; margin-bottom: 15px;">Métricas en tiempo real del sistema</p>
                    <div style="background: #f0f9ff; padding: 15px; border-radius: 8px;">
                        <h4 style="color: #1e40af; margin: 0 0 10px 0;">🎯 Características del Dashboard</h4>
                        <ul style="text-align: left; margin: 0; padding-left: 20px; color: #374151; font-size: 14px;">
                            <li>Estadísticas de documentos, incidentes y no conformidades</li>
                            <li>Actividades recientes en tiempo real</li>
                            <li>Estado del sistema con indicadores</li>
                            <li>Acceso rápido a funciones principales</li>
                        </ul>
                    </div>
                </div>
            `, 'info', 8000);
        }, 1000);
    }

    async autoLogin() {
        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'username=admin&password=admin'
            });

            if (response.ok) {
                const data = await response.json();
                window.app.token = data.access_token;
                window.app.user = data.user;
                localStorage.setItem('token', window.app.token);
                localStorage.setItem('user', JSON.stringify(window.app.user));
                window.app.showApp();
                window.app.updateUserInfo();
            }
        } catch (error) {
            console.error('Auto-login failed:', error);
        }
    }

    demoDocuments() {
        if (window.app) {
            window.app.loadModule('documents');
        }
        
        this.showNotification(`
            <div style="text-align: center; padding: 15px;">
                <h3 style="color: #2563eb; margin-bottom: 10px;">📄 Gestión de Documentos</h3>
                <p style="color: #666; margin-bottom: 15px;">Control de versiones y aprobación de documentos</p>
                <div style="background: #f0f9ff; padding: 15px; border-radius: 8px;">
                    <h4 style="color: #1e40af; margin: 0 0 10px 0;">🔧 Funcionalidades</h4>
                    <ul style="text-align: left; margin: 0; padding-left: 20px; color: #374151; font-size: 14px;">
                        <li>Creación y edición de documentos</li>
                        <li>Control de versiones automático</li>
                        <li>Flujo de aprobación configurable</li>
                        <li>Estados: Draft, Pending Review, Approved</li>
                        <li>Tipos: Manual, Policy, Procedure, Form</li>
                    </ul>
                </div>
            </div>
        `, 'info', 8000);
    }

    demoIncidents() {
        if (window.app) {
            window.app.loadModule('incidents');
        }
        
        this.showNotification(`
            <div style="text-align: center; padding: 15px;">
                <h3 style="color: #2563eb; margin-bottom: 10px;">🚨 Gestión de Incidentes</h3>
                <p style="color: #666; margin-bottom: 15px;">Manejo de eventos críticos con prioridades</p>
                <div style="background: #fef2f2; padding: 15px; border-radius: 8px;">
                    <h4 style="color: #dc2626; margin: 0 0 10px 0;">⚡ Sistema de Prioridades</h4>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; text-align: left; font-size: 14px;">
                        <div><span style="color: #dc2626;">🔴 CRITICAL</span> - Acción inmediata</div>
                        <div><span style="color: #f59e0b;">🟡 HIGH</span> - Acción urgente</div>
                        <div><span style="color: #3b82f6;">🔵 MEDIUM</span> - Acción normal</div>
                        <div><span style="color: #10b981;">🟢 LOW</span> - Acción programada</div>
                    </div>
                </div>
            </div>
        `, 'info', 8000);
    }

    demoNonConformities() {
        if (window.app) {
            window.app.loadModule('non-conformities');
        }
        
        this.showNotification(`
            <div style="text-align: center; padding: 15px;">
                <h3 style="color: #2563eb; margin-bottom: 10px;">⚠️ No Conformidades</h3>
                <p style="color: #666; margin-bottom: 15px;">Registro y seguimiento de problemas</p>
                <div style="background: #fffbeb; padding: 15px; border-radius: 8px;">
                    <h4 style="color: #d97706; margin: 0 0 10px 0;">🔍 Análisis de Causa Raíz</h4>
                    <ul style="text-align: left; margin: 0; padding-left: 20px; color: #374151; font-size: 14px;">
                        <li>Registro detallado del problema</li>
                        <li>Análisis de causa raíz integrado</li>
                        <li>Acciones correctivas y preventivas</li>
                        <li>Seguimiento hasta cierre completo</li>
                        <li>Métricas de resolución automáticas</li>
                    </ul>
                </div>
            </div>
        `, 'info', 8000);
    }

    demoAudits() {
        if (window.app) {
            window.app.loadModule('audits');
        }
        
        this.showNotification(`
            <div style="text-align: center; padding: 15px;">
                <h3 style="color: #2563eb; margin-bottom: 10px;">🔍 Auditorías Internas</h3>
                <p style="color: #666; margin-bottom: 15px;">Programación y documentación de auditorías</p>
                <div style="background: #f0fdf4; padding: 15px; border-radius: 8px;">
                    <h4 style="color: #16a34a; margin: 0 0 10px 0;">📋 Tipos de Auditoría</h4>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; text-align: left; font-size: 14px;">
                        <div><strong>Interna</strong> - Auditorías del sistema</div>
                        <div><strong>Externa</strong> - Auditorías de terceros</div>
                        <div><strong>Seguimiento</strong> - Verificación de acciones</div>
                        <div><strong>Especial</strong> - Auditorías específicas</div>
                    </div>
                </div>
            </div>
        `, 'info', 8000);
    }

    demoKPIs() {
        if (window.app) {
            window.app.loadModule('kpis');
        }
        
        this.showNotification(`
            <div style="text-align: center; padding: 15px;">
                <h3 style="color: #2563eb; margin-bottom: 10px;">📈 KPIs y Métricas</h3>
                <p style="color: #666; margin-bottom: 15px;">Indicadores de desempeño del sistema</p>
                <div style="background: #f8fafc; padding: 15px; border-radius: 8px;">
                    <h4 style="color: #374151; margin: 0 0 10px 0;">📊 Categorías de KPIs</h4>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; text-align: left; font-size: 14px;">
                        <div><strong>Calidad</strong> - Indicadores ISO 9001</div>
                        <div><strong>Continuidad</strong> - Indicadores ISO 22301</div>
                        <div><strong>Rendimiento</strong> - Eficiencia operativa</div>
                        <div><strong>Cumplimiento</strong> - Conformidad normativa</div>
                    </div>
                </div>
            </div>
        `, 'info', 8000);
    }

    demoBusinessContinuity() {
        if (window.app) {
            window.app.loadModule('business-continuity');
        }
        
        this.showNotification(`
            <div style="text-align: center; padding: 15px;">
                <h3 style="color: #2563eb; margin-bottom: 10px;">🔄 Continuidad del Negocio</h3>
                <p style="color: #666; margin-bottom: 15px;">Planes y simulaciones de emergencia</p>
                <div style="background: #fef3c7; padding: 15px; border-radius: 8px;">
                    <h4 style="color: #d97706; margin: 0 0 10px 0;">🎯 Objetivos RTO/RPO</h4>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; text-align: left; font-size: 14px;">
                        <div><strong>RTO</strong> - Tiempo de Recuperación Objetivo</div>
                        <div><strong>RPO</strong> - Punto de Recuperación Objetivo</div>
                        <div><strong>Simulaciones</strong> - Pruebas de emergencia</div>
                        <div><strong>Planes</strong> - Documentación de continuidad</div>
                    </div>
                </div>
            </div>
        `, 'info', 8000);
    }

    showSummary() {
        this.showNotification(`
            <div style="text-align: center; padding: 20px;">
                <h2 style="color: #2563eb; margin-bottom: 15px;">🎯 Resumen del Sistema SGCN-SGC</h2>
                <div style="background: #f0f9ff; padding: 20px; border-radius: 10px; margin: 15px 0;">
                    <h3 style="color: #1e40af; margin: 0 0 15px 0;">✅ Beneficios Implementados</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; text-align: left;">
                        <div>
                            <h4 style="color: #1e40af; margin: 0 0 10px 0;">🏢 Para la Organización</h4>
                            <ul style="margin: 0; padding-left: 20px; color: #374151; font-size: 14px;">
                                <li>Cumplimiento ISO 9001/22301</li>
                                <li>Trazabilidad completa</li>
                                <li>Reportes ejecutivos</li>
                                <li>Reducción de tiempo</li>
                            </ul>
                        </div>
                        <div>
                            <h4 style="color: #1e40af; margin: 0 0 10px 0;">👥 Para los Usuarios</h4>
                            <ul style="margin: 0; padding-left: 20px; color: #374151; font-size: 14px;">
                                <li>Interfaz intuitiva</li>
                                <li>Acceso móvil</li>
                                <li>Notificaciones automáticas</li>
                                <li>Dashboard personalizado</li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div style="background: #f0fdf4; padding: 15px; border-radius: 8px; margin: 15px 0;">
                    <h4 style="color: #16a34a; margin: 0 0 10px 0;">🚀 Próximos Pasos</h4>
                    <p style="color: #374151; margin: 0; font-size: 14px;">
                        Desarrollo de funcionalidades adicionales, integración con sistemas existentes, 
                        migración a producción y capacitación de usuarios.
                    </p>
                </div>
            </div>
        `, 'success', 15000);
    }

    showNotification(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} fixed top-4 left-4 z-50 max-w-md`;
        notification.innerHTML = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, duration);
    }
}

// Initialize demo when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.demo = new SGCN_Demo();
    
    // Add demo button to login page
    setTimeout(() => {
        const loginCard = document.querySelector('.login-card');
        if (loginCard) {
            const demoButton = document.createElement('button');
            demoButton.innerHTML = '🎯 Iniciar Demo para Directivos';
            demoButton.className = 'btn btn-primary w-full mt-3';
            demoButton.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
            demoButton.onclick = () => window.demo.startDemo();
            loginCard.appendChild(demoButton);
        }
    }, 1000);
});

