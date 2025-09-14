class SpamBoxApp {
    constructor() {
        this.currentPath = '.';
        this.baseURL = '/api';
        this.isFirstVisit = false;
        this.hasShownSetupSuccess = false;
        this.init();
    }

    encodePath(path) {
        return encodeURIComponent(path).replace(/%2F/g, '/');
    }

    init() {
        this.setupEventListeners();
        this.checkFirstVisit();
    }

    updateCreateFolderAvailability(path) {
        const btn = document.getElementById('new-folder-btn');
        if (!btn) return;
        btn.disabled = false;
        btn.title = 'Новая папка в текущей папке';
    }

    async checkFirstVisit() {
        try {
            await this.navigateToPath('.');
        } catch (error) {
            if (error.response && error.response.status === 428) {
                this.isFirstVisit = true;
                this.startSetupAnimation();
            } else if (error.response && error.response.status === 403) {
                const errorMessage = (error.response.data && (error.response.data.error || error.response.data.message)) || '';
                this.showNotification('Ошибка доступа: ' + errorMessage, 'danger');
            } else {
                this.showNotification('Ошибка подключения к серверу', 'danger');
            }
        }
    }

    async startSetupAnimation() {
        this.openModal('setup-modal');
        
        const steps = [
            { id: 'step-1', duration: 2000, action: () => this.setupUser() },
            { id: 'step-2', duration: 1500, action: () => this.waitStep() },
            { id: 'step-3', duration: 1000, action: () => this.waitStep() },
            { id: 'step-4', duration: 1000, action: () => this.completeSetup() }
        ];

        for (let i = 0; i < steps.length; i++) {
            const step = steps[i];
            const stepElement = document.getElementById(step.id);
            const progressElement = document.getElementById(`progress-${i + 1}`);
            
            stepElement.classList.add('active');
            
            await step.action();
            
            await this.animateProgress(progressElement, step.duration);
            
            stepElement.classList.remove('active');
            stepElement.classList.add('completed');
        }

        setTimeout(() => {
            this.closeModal('setup-modal');
            this.isFirstVisit = false;
            this.checkFirstVisit();
            if (!this.hasShownSetupSuccess) {
                this.showNotification('SpamBox успешно настроен!', 'success');
                this.hasShownSetupSuccess = true;
            }
        }, 1500);
    }

    async setupUser() {
        try {
            await axios.post(`${this.baseURL}/setup`);
        } catch (error) {
            console.error('Setup error:', error);
        }
    }

    async waitStep() {
        return Promise.resolve();
    }

    async completeSetup() {
        return Promise.resolve();
    }

    async resetUser() {
        if (!confirm('Это удалит все ваши данные и сбросит настройки. Продолжить?')) {
            return;
        }

        this.showNotification('Сброс пользователя...', 'info');
        
        try {
            await axios.post(`${this.baseURL}/reset`);
            this.showNotification('Перенастройка почтового ящика прошла успешно!', 'success');
            
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } catch (error) {
            console.error('Reset error:', error);
            const errorMessage = error.response?.data?.error || 'Неизвестная ошибка';
            this.showNotification('Ошибка перенастройки: ' + errorMessage, 'danger');
        }
    }

    setupEventListeners() {
        document.getElementById('file-upload').addEventListener('change', (e) => {
            this.handleFileUpload(e.target.files);
        });

        const dropZone = document.getElementById('drop-zone');
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('dragover');
        });

        dropZone.addEventListener('dragleave', (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
        });

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
            this.handleFileUpload(e.dataTransfer.files);
        });

        document.getElementById('modal-close').addEventListener('click', () => {
            this.closeModal('file-preview-modal');
        });

        document.getElementById('modal-close-btn').addEventListener('click', () => {
            this.closeModal('file-preview-modal');
        });

        document.getElementById('new-folder-btn').addEventListener('click', () => {
            this.showCreateFolderDialog();
        });

        const resetBtn = document.getElementById('reset-btn');
        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                this.resetUser();
            });
        }
    }

    async animateProgress(element, duration) {
        return new Promise((resolve) => {
            element.style.width = '0%';
            element.style.transition = `width ${duration}ms ease-out`;
            
            setTimeout(() => {
                element.style.width = '100%';
                setTimeout(resolve, duration);
            }, 50);
        });
    }

    async loadFolders() {
        return this.loadSidebarFolders(this.currentPath || '.');
    }

    async loadFiles(path) {
        try {
            const encPath = this.encodePath(path);
            const response = await axios.get(`${this.baseURL}/files?path=${encPath}`);
            const body = response.data || {};
            const items = Array.isArray(body) ? body : (body.data || []);
            const files = items.filter(item => !item.is_directory && !item.name.startsWith('.'));
            
            this.updateBreadcrumb(path);
            this.renderFiles(files);
            this.currentPath = path;
            this.updateCreateFolderAvailability(this.currentPath);
        } catch (error) {
            if (error.response && error.response.status === 428) {
                this.startSetupAnimation();
                return;
            }
            console.error('Error loading files:', error);
            this.showNotification('Ошибка загрузки писем', 'danger');
        }
    }

    createFolderElement(folder) {
        const folderDiv = document.createElement('div');
        folderDiv.className = 'folder-item';
        folderDiv.innerHTML = `
            <span class="icon is-large">
                <i class="fas fa-folder fa-2x"></i>
            </span>
            <p class="folder-name">${folder.name}</p>
            <p class="folder-count">${folder.file_count || 0} ✉️</p>
            <button class="button is-small is-light delete-folder-btn" title="Удалить папку">
                <span class="icon is-small"><i class="fas fa-trash"></i></span>
            </button>
        `;
        
        folderDiv.addEventListener('click', () => {
            const targetPath = folder.path || folder.name;
            this.navigateToPath(targetPath);
        });
        
        const deleteBtn = folderDiv.querySelector('.delete-folder-btn');
        deleteBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            const targetPath = folder.path || folder.name;
            this.deleteFolderByPath(targetPath);
        });
        
        return folderDiv;
    }

    renderFiles(files) {
        const filesContainer = document.getElementById('files-container');
        filesContainer.innerHTML = '';
        
        if (files.length === 0) {
            filesContainer.innerHTML = `
                <div class="empty-state">
                    <span class="icon is-large">
                        <i class="fas fa-inbox fa-4x"></i>
                    </span>
                    <p class="title is-4">Папка пуста</p>
                    <p class="subtitle is-6">Перетащите файлы в область выше или используйте кнопку загрузки для добавления контента</p>
                </div>
            `;
            return;
        }
        
        files.forEach(file => {
            const fileElement = this.createFileElement(file);
            filesContainer.appendChild(fileElement);
        });
    }

    createFileElement(file) {
        const fileDiv = document.createElement('div');
        fileDiv.className = 'file-item';
        fileDiv.innerHTML = `
            <div class="file-icon">
                <span class="icon is-large">
                    <i class="fas ${this.getFileIcon(file.name)} fa-2x"></i>
                </span>
            </div>
            <div class="file-info">
                <p class="file-name">${file.name}</p>
                <p class="file-size">${this.formatFileSize(file.size)}</p>
                <p class="file-date">${this.formatDate(file.modified)}</p>
            </div>
            <div class="file-actions">
                <button class="button is-small is-info view-btn" title="Просмотр">
                    <span class="icon">
                        <i class="fas fa-eye"></i>
                    </span>
                </button>
                <button class="button is-small is-danger delete-btn" title="Удалить">
                    <span class="icon">
                        <i class="fas fa-trash"></i>
                    </span>
                </button>
            </div>
        `;
        
        const viewBtn = fileDiv.querySelector('.view-btn');
        const deleteBtn = fileDiv.querySelector('.delete-btn');
        
        viewBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.viewFile(file);
        });
        
        deleteBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.deleteFile(file);
        });
        
        return fileDiv;
    }

    async viewFile(file) {
        try {
            const filePath = this.currentPath === '.' ? file.name : `${this.currentPath}/${file.name}`;
            const encPath = this.encodePath(filePath);
            const response = await axios.get(`${this.baseURL}/content?path=${encPath}`);
            
            const body = response.data || {};
            const payload = body.data || body;

            document.getElementById('file-name').textContent = file.name;
            document.getElementById('file-content').textContent = payload.content;
            
            this.openModal('file-preview-modal');
        } catch (error) {
            if (error.response && error.response.status === 428) {
                this.startSetupAnimation();
                return;
            }
            console.error('Error viewing file:', error);
            this.showNotification('Ошибка открытия файла', 'danger');
        }
    }

    async deleteFile(file) {
        if (!confirm(`Удалить файл "${file.name}"?`)) {
            return;
        }
        
        try {
            const filePath = this.currentPath === '.' ? file.name : `${this.currentPath}/${file.name}`;
            const encPath = this.encodePath(filePath);
            await axios.delete(`${this.baseURL}/files?path=${encPath}`);
            this.showNotification('Файл удален', 'success');
            this.loadFiles(this.currentPath);
        } catch (error) {
            if (error.response && error.response.status === 428) {
                this.startSetupAnimation();
                return;
            }
            console.error('Error deleting file:', error);
            this.showNotification('Ошибка удаления файла', 'danger');
        }
    }

    async handleFileUpload(files) {
        if (files.length === 0) return;
        
        const formData = new FormData();
        
        for (let file of files) {
            formData.append('files', file);
        }
        
        formData.append('path', this.currentPath);
        
        try {
            await axios.post(`${this.baseURL}/files`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            
            this.showNotification('Файлы загружены', 'success');
            this.loadFiles(this.currentPath);
        } catch (error) {
            if (error.response && error.response.status === 428) {
                this.startSetupAnimation();
                return;
            }
            console.error('Error uploading files:', error);
            this.showNotification('Ошибка загрузки файлов', 'danger');
        }
    }

    async showCreateFolderDialog() {
        const folderName = prompt('Введите название папки:');
        if (!folderName) return;
        
        try {
            await axios.post(`${this.baseURL}/folder`, {
                name: folderName,
                path: this.currentPath
            });
            
            this.showNotification('Папка создана', 'success');
            await this.refreshCurrentView();
        } catch (error) {
            if (error.response && error.response.status === 428) {
                this.startSetupAnimation();
                return;
            }
            console.error('Error creating folder:', error);
            this.showNotification('Ошибка создания папки', 'danger');
        }
    }

    updateBreadcrumb(path) {
        const breadcrumb = document.getElementById('breadcrumb');
        breadcrumb.innerHTML = '';
        
        const parts = path === '.' ? [] : path.split('/');
        
        const homeItem = document.createElement('li');
        homeItem.innerHTML = '<a href="#" data-path=".">🏠 Главная</a>';
        homeItem.querySelector('a').addEventListener('click', (e) => {
            e.preventDefault();
            this.navigateToPath('.');
        });
        breadcrumb.appendChild(homeItem);
        
        let currentPath = '.';
        parts.forEach((part, index) => {
            currentPath = currentPath === '.' ? part : `${currentPath}/${part}`;
            const item = document.createElement('li');
            item.innerHTML = `<a href="#" data-path="${currentPath}">${part}</a>`;
            item.querySelector('a').addEventListener('click', (e) => {
                e.preventDefault();
                this.navigateToPath(currentPath);
            });
            breadcrumb.appendChild(item);
        });
    }

    async loadSidebarFolders(path) {
        try {
            const encPath = this.encodePath(path);
            const response = await axios.get(`${this.baseURL}/files?path=${encPath}`);
            const body = response.data || {};
            const items = Array.isArray(body) ? body : (body.data || []);
            const folders = items.filter(item => item.is_directory && !item.name.startsWith('.'));

            const foldersContainer = document.getElementById('folders-container');
            foldersContainer.innerHTML = '';

            folders.forEach(folder => {
                const folderElement = this.createFolderElement(folder);
                foldersContainer.appendChild(folderElement);
            });
        } catch (error) {
            if (error.response && error.response.status === 428) {
                this.startSetupAnimation();
                return;
            }
            console.error('Error loading folders:', error);
            this.showNotification('Ошибка загрузки папок', 'danger');
        }
    }

    async navigateToPath(path) {
        await this.loadFiles(path);
        await this.loadSidebarFolders(path);
    }

    async refreshCurrentView() {
        await this.navigateToPath(this.currentPath);
    }

    async deleteFolderByPath(path) {
        if (!confirm('Удалить папку и все её содержимое?')) {
            return;
        }
        try {
            const encPath = this.encodePath(path);
            await axios.delete(`${this.baseURL}/files?path=${encPath}`);
            this.showNotification('Папка удалена', 'success');
            await this.refreshCurrentView();
        } catch (error) {
            if (error.response && error.response.status === 428) {
                this.startSetupAnimation();
                return;
            }
            console.error('Error deleting folder:', error);
            this.showNotification('Ошибка удаления папки', 'danger');
        }
    }

    getFileIcon(fileName) {
        const ext = fileName.split('.').pop().toLowerCase();
        switch (ext) {
            case 'txt': return 'fa-file-alt';
            case 'pdf': return 'fa-file-pdf';
            case 'doc': case 'docx': return 'fa-file-word';
            case 'xls': case 'xlsx': return 'fa-file-excel';
            case 'jpg': case 'jpeg': case 'png': case 'gif': return 'fa-file-image';
            case 'zip': case 'rar': case '7z': return 'fa-file-archive';
            case 'mp3': case 'wav': case 'ogg': return 'fa-file-audio';
            case 'mp4': case 'avi': case 'mkv': return 'fa-file-video';
            case 'html': case 'htm': return 'fa-file-code';
            case 'eml': return 'fa-envelope';
            default: return 'fa-file';
        }
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    formatDate(value) {
        if (!value) return '';
        let date;
        if (typeof value === 'number') {
            date = new Date(value * 1000);
        } else {
            date = new Date(value);
        }
        return date.toLocaleDateString('ru-RU', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    openModal(modalId) {
        document.getElementById(modalId).classList.add('is-active');
    }

    closeModal(modalId) {
        document.getElementById(modalId).classList.remove('is-active');
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification is-${type}`;
        notification.innerHTML = `
            <button class="delete"></button>
            ${message}
        `;
        
        const container = document.getElementById('notifications');
        container.appendChild(notification);
        
        const deleteBtn = notification.querySelector('.delete');
        deleteBtn.addEventListener('click', () => {
            notification.remove();
        });
        
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new SpamBoxApp();
});
