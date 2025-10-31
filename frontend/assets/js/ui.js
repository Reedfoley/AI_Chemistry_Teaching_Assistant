/**
 * UI 工具模块
 * 处理所有 UI 操作和交互
 */

const UIService = {
    // DOM 元素缓存
    elements: {},
    
    /**
     * 初始化 UI 元素引用
     */
    init() {
        try {
            this.elements = {
                // 容器
                apiKeyContainer: document.getElementById('api-key-container'),
                mainContent: document.getElementById('main-content'),
                
                // API Key 输入
                apiKeyInput: document.getElementById('api-key-input'),
                saveApiKeyBtn: document.getElementById('save-api-key'),
                
                // 标签页
                tabs: document.querySelectorAll('.tab'),
                tabContents: document.querySelectorAll('.tab-content'),
                
                // 化学反应讲解
                reactionInput: document.getElementById('reaction-input'),
                generateReactionExplainBtn: document.getElementById('generate-reaction-explain'),
                clearReactionExplainBtn: document.getElementById('clear-reaction-explain'),
                reactionExplainLoading: document.getElementById('reaction-explain-loading'),
                reactionExplainResult: document.getElementById('reaction-explain-result'),
                reactionExplainContent: document.getElementById('reaction-explain-content'),
                
                // 方程式配平
                equationInput: document.getElementById('equation-input'),
                balanceEquationBtn: document.getElementById('balance-equation'),
                clearEquationBtn: document.getElementById('clear-equation'),
                equationBalanceLoading: document.getElementById('equation-balance-loading'),
                equationBalanceResult: document.getElementById('equation-balance-result'),
                equationBalanceContent: document.getElementById('equation-balance-content'),
                
                // 反应现象图像
                imagePromptInput: document.getElementById('image-prompt-input'),
                generateImageBtn: document.getElementById('generate-image'),
                clearImageBtn: document.getElementById('clear-image'),
                imageGenerationLoading: document.getElementById('image-generation-loading'),
                imageGenerationResult: document.getElementById('image-generation-result'),
                generatedImage: document.getElementById('generated-image'),
                
                // 物质识别
                materialImageInput: document.getElementById('material-image-input'),
                fileNameDisplay: document.getElementById('file-name'),
                recognizeMaterialBtn: document.getElementById('recognize-material'),
                clearMaterialBtn: document.getElementById('clear-material'),
                materialRecognitionLoading: document.getElementById('material-recognition-loading'),
                materialRecognitionResult: document.getElementById('material-recognition-result'),
                materialRecognitionContent: document.getElementById('material-recognition-content'),
                materialImagePreview: document.getElementById('material-image-preview'),
                materialImagePlaceholder: document.getElementById('material-image-placeholder'),
                
                // 消息提示
                errorMessage: document.getElementById('error-message'),
                successMessage: document.getElementById('success-message')
            };
            
            // 检查是否有缺失的元素
            const missingElements = [];
            for (const [key, value] of Object.entries(this.elements)) {
                if (value === null && !['tabs', 'tabContents'].includes(key)) {
                    missingElements.push(key);
                }
            }
            
            if (missingElements.length > 0) {
                console.warn('[UIService] 缺失的DOM元素:', missingElements);
                throw new Error(`缺失的DOM元素: ${missingElements.join(', ')}`);
            }
            
            console.log('[UIService] UI 初始化完成');
        } catch (error) {
            console.error('[UIService] 初始化失败:', error);
            throw error;
        }
    },
    
    /**
     * 显示主内容区域
     */
    showMainContent() {
        try {
            if (!this.elements) {
                console.error('[UIService] 元素未初始化');
                return;
            }
            if (this.elements.apiKeyContainer) {
                this.elements.apiKeyContainer.style.display = 'none';
            }
            if (this.elements.mainContent) {
                this.elements.mainContent.style.display = 'block';
            }
        } catch (error) {
            console.error('[UIService] showMainContent 失败:', error);
        }
    },
    
    /**
     * 显示 API Key 容器
     */
    showApiKeyContainer() {
        if (!this.elements || !this.elements.apiKeyContainer || !this.elements.mainContent) {
            console.error('[UIService] apiKeyContainer 或 mainContent 元素不存在');
            return;
        }
        this.elements.apiKeyContainer.style.display = 'block';
        this.elements.mainContent.style.display = 'none';
        // 自动聚焦到输入框
        if (this.elements.apiKeyInput) {
            this.elements.apiKeyInput.focus();
        }
    },
    
    /**
     * 隐藏 API Key 容器
     */
    hideApiKeyContainer() {
        if (!this.elements || !this.elements.apiKeyContainer) {
            return;
        }
        this.elements.apiKeyContainer.style.display = 'none';
    },
    
    /**
     * 获取 API Key 输入值
     */
    getApiKey() {
        if (!this.elements || !this.elements.apiKeyInput) {
            return '';
        }
        return this.elements.apiKeyInput.value || '';
    },
    
    /**
     * 设置 API Key 输入值
     */
    setApiKey(key) {
        if (!this.elements || !this.elements.apiKeyInput) {
            return;
        }
        this.elements.apiKeyInput.value = key;
    },
    
    /**
     * 清空 API Key
     */
    clearApiKey() {
        if (!this.elements || !this.elements.apiKeyInput) {
            return;
        }
        this.elements.apiKeyInput.value = '';
    },
    
    // ==================== 标签页操作 ====================
    
    /**
     * 切换标签页
     */
    switchTab(tabId) {
        // 移除所有选项卡的 active 类
        this.elements.tabs.forEach(t => t.classList.remove('active'));
        this.elements.tabContents.forEach(c => c.classList.remove('active'));
        
        // 添加当前选项卡的 active 类
        const activeTab = Array.from(this.elements.tabs).find(t => t.getAttribute('data-tab') === tabId);
        if (activeTab) {
            activeTab.classList.add('active');
        }
        
        const activeContent = document.getElementById(tabId);
        if (activeContent) {
            activeContent.classList.add('active');
        }
    },
    
    // ==================== 化学反应讲解 ====================
    
    getReactionInput() {
        return this.elements.reactionInput.value.trim();
    },
    
    setReactionExplainResult(content) {
        this.elements.reactionExplainContent.innerHTML = `<pre>${content}</pre>`;
        this.elements.reactionExplainResult.style.display = 'block';
    },
    
    clearReactionExplanation() {
        this.elements.reactionInput.value = '';
        this.elements.reactionExplainContent.innerHTML = '';
        this.elements.reactionExplainResult.style.display = 'none';
    },
    
    // ==================== 方程式配平 ====================
    
    getEquationInput() {
        return this.elements.equationInput.value.trim();
    },
    
    setEquationBalanceResult(content) {
        this.elements.equationBalanceContent.innerHTML = `<pre>${content}</pre>`;
        this.elements.equationBalanceResult.style.display = 'block';
    },
    
    clearEquation() {
        this.elements.equationInput.value = '';
        this.elements.equationBalanceContent.innerHTML = '';
        this.elements.equationBalanceResult.style.display = 'none';
    },
    
    // ==================== 反应现象图像 ====================
    
    getImagePromptInput() {
        return this.elements.imagePromptInput.value.trim();
    },
    
    setGeneratedImage(imageUrl) {
        this.elements.generatedImage.src = imageUrl;
        this.elements.generatedImage.style.display = 'block';
        this.elements.imageGenerationResult.style.display = 'block';
    },
    
    clearImage() {
        this.elements.imagePromptInput.value = '';
        this.elements.generatedImage.src = '';
        this.elements.generatedImage.style.display = 'none';
        this.elements.imageGenerationResult.style.display = 'none';
    },
    
    // ==================== 物质识别 ====================
    
    getMaterialImageFile() {
        return this.elements.materialImageInput.files[0];
    },
    
    setMaterialRecognitionResult(content) {
        this.elements.materialRecognitionContent.innerHTML = `<pre>${content}</pre>`;
        this.elements.materialRecognitionResult.style.display = 'block';
    },
    
    // 设置图片预览
    setMaterialImagePreview(file) {
        if (!file) {
            this.elements.materialImagePreview.style.display = 'none';
            this.elements.materialImagePlaceholder.style.display = 'block';
            return;
        }
        
        const reader = new FileReader();
        reader.onload = (e) => {
            this.elements.materialImagePreview.src = e.target.result;
            this.elements.materialImagePreview.style.display = 'block';
            this.elements.materialImagePlaceholder.style.display = 'none';
        };
        reader.readAsDataURL(file);
    },
    
    clearMaterial() {
        this.elements.materialImageInput.value = '';
        this.elements.fileNameDisplay.textContent = '未选择文件';
        this.elements.materialRecognitionContent.innerHTML = '';
        this.elements.materialRecognitionResult.style.display = 'none';
        this.elements.materialImagePreview.src = '';
        this.elements.materialImagePreview.style.display = 'none';
        this.elements.materialImagePlaceholder.style.display = 'block';
    },
    
    // ==================== 加载状态 ====================
    
    showLoading(loadingElement) {
        loadingElement.style.display = 'flex';
    },
    
    hideLoading(loadingElement) {
        loadingElement.style.display = 'none';
    },
    
    /**
     * 快捷方法：显示加载状态
     */
    showReactionExplainLoading() {
        this.showLoading(this.elements.reactionExplainLoading);
    },
    
    hideReactionExplainLoading() {
        this.hideLoading(this.elements.reactionExplainLoading);
    },
    
    showEquationBalanceLoading() {
        this.showLoading(this.elements.equationBalanceLoading);
    },
    
    hideEquationBalanceLoading() {
        this.hideLoading(this.elements.equationBalanceLoading);
    },
    
    showImageGenerationLoading() {
        this.showLoading(this.elements.imageGenerationLoading);
    },
    
    hideImageGenerationLoading() {
        this.hideLoading(this.elements.imageGenerationLoading);
    },
    
    showMaterialRecognitionLoading() {
        this.showLoading(this.elements.materialRecognitionLoading);
    },
    
    hideMaterialRecognitionLoading() {
        this.hideLoading(this.elements.materialRecognitionLoading);
    },
    
    // ==================== 消息提示 ====================
    
    showError(message) {
        if (!this.elements || !this.elements.errorMessage || !this.elements.successMessage) {
            console.error('[UIService] errorMessage 或 successMessage 元素不存在');
            console.error('[Error]', message);
            return;
        }
        this.elements.errorMessage.textContent = message;
        this.elements.errorMessage.style.display = 'block';
        this.elements.successMessage.style.display = 'none';
        console.error('[Error]', message);
    },
    
    hideError() {
        if (!this.elements || !this.elements.errorMessage) return;
        this.elements.errorMessage.style.display = 'none';
    },
    
    showSuccess(message) {
        if (!this.elements || !this.elements.successMessage || !this.elements.errorMessage) {
            console.log('[UIService] successMessage 或 errorMessage 元素不存在');
            console.log('[Success]', message);
            return;
        }
        this.elements.successMessage.textContent = message;
        this.elements.successMessage.style.display = 'block';
        this.elements.errorMessage.style.display = 'none';
        console.log('[Success]', message);
        
        // 3秒后自动隐藏
        setTimeout(() => {
            this.hideSuccess();
        }, 3000);
    },
    
    hideSuccess() {
        if (!this.elements || !this.elements.successMessage) return;
        this.elements.successMessage.style.display = 'none';
    },
    
    /**
     * 清除所有消息提示
     */
    clearMessages() {
        this.hideError();
        this.hideSuccess();
    },
    
    // ==================== 工具方法 ====================
    
    /**
     * 防抖函数
     */
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    /**
     * 节流函数
     */
    throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
};

// 导出 UI 服务
if (typeof module !== 'undefined' && module.exports) {
    module.exports = UIService;
}
