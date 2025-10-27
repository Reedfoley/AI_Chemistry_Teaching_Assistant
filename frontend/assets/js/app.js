/**
 * 应用主模块
 * 处理应用逻辑、事件绑定和状态管理
 */

const App = {
    apiKey: '',  // 存储 API Key
    
    /**
     * 应用初始化
     */
    async init() {
        try {
            console.log('[App] 开始初始化...');
            
            // 初始化 UI 服务
            console.log('[App] 初始化 UIService...');
            UIService.init();
            console.log('[App] UIService 初始化完成');
            
            // 绑定事件
            console.log('[App] 绑定事件...');
            this.bindEvents();
            console.log('[App] 事件绑定完成');
            
            // 显示 API Key 输入界面
            console.log('[App] 显示 API Key 输入界面...');
            UIService.showApiKeyContainer();
            console.log('[App] API Key 输入界面显示完成');
            
            console.log('[App] 应用初始化完成');
        } catch (error) {
            console.error('[App] 初始化失败:', error);
            console.error('[App] 错误信息:', error.message);
            console.error('[App] 错误堆栈:', error.stack);
            if (UIService.elements.errorMessage) {
                UIService.showError('应用初始化失败，详情请查看控制台错误信息: ' + error.message);
            }
        }
    },

    
    // ==================== API Key 管理 ====================
    
    handleSaveApiKey() {
        const apiKey = UIService.getApiKey();
        
        if (!apiKey || apiKey.trim() === '') {
            UIService.showError('请输入 API Key');
            return;
        }
        
        // 保存 API Key
        this.apiKey = apiKey.trim();
        
        console.log('[App] API Key 已保存');
        UIService.showSuccess('API Key 已保存！');
        
        // 延迟 1 秒后显示主内容
        setTimeout(() => {
            UIService.hideApiKeyContainer();
            UIService.showMainContent();
        }, 1000);
    },
    
    // ==================== 事件绑定 ====================
    
    bindEvents() {
        try {
            console.log('[App] bindEvents: 开始绑定事件');
            
            // API Key 保存
            if (UIService.elements.saveApiKeyBtn) {
                UIService.elements.saveApiKeyBtn.addEventListener('click', () => {
                    this.handleSaveApiKey();
                });
            }
            
            // 支持在 API Key 输入框按 Enter 键提交
            if (UIService.elements.apiKeyInput) {
                UIService.elements.apiKeyInput.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') {
                        this.handleSaveApiKey();
                    }
                });
            }
            
            // 标签页切换
            if (UIService.elements.tabs && UIService.elements.tabs.length > 0) {
                UIService.elements.tabs.forEach(tab => {
                    tab.addEventListener('click', (e) => {
                        const tabId = e.target.getAttribute('data-tab');
                        UIService.switchTab(tabId);
                    });
                });
                console.log('[App] bindEvents: 标签页事件绑定完成');
            }
            
            // 化学反应讲解
            if (UIService.elements.generateReactionExplainBtn) {
                UIService.elements.generateReactionExplainBtn.addEventListener('click', () => this.handleGenerateReactionExplanation());
            }
            if (UIService.elements.clearReactionExplainBtn) {
                UIService.elements.clearReactionExplainBtn.addEventListener('click', () => {
                    UIService.clearReactionExplanation();
                    UIService.clearMessages();
                });
            }
            
            // 方程式配平
            if (UIService.elements.balanceEquationBtn) {
                UIService.elements.balanceEquationBtn.addEventListener('click', () => this.handleBalanceEquation());
            }
            if (UIService.elements.clearEquationBtn) {
                UIService.elements.clearEquationBtn.addEventListener('click', () => {
                    UIService.clearEquation();
                    UIService.clearMessages();
                });
            }
            
            // 反应现象图像
            if (UIService.elements.generateImageBtn) {
                UIService.elements.generateImageBtn.addEventListener('click', () => this.handleGenerateImage());
            }
            if (UIService.elements.clearImageBtn) {
                UIService.elements.clearImageBtn.addEventListener('click', () => {
                    UIService.clearImage();
                    UIService.clearMessages();
                });
            }
            
            // 物质识别
            if (UIService.elements.materialImageInput) {
                UIService.elements.materialImageInput.addEventListener('change', (e) => {
                    const file = e.target.files[0];
                    if (file) {
                        UIService.elements.fileNameDisplay.textContent = file.name;
                        // 设置图片预览
                        UIService.setMaterialImagePreview(file);
                    } else {
                        UIService.elements.fileNameDisplay.textContent = '未选择文件';
                        UIService.setMaterialImagePreview(null);
                    }
                });
            }
            
            if (UIService.elements.recognizeMaterialBtn) {
                UIService.elements.recognizeMaterialBtn.addEventListener('click', () => this.handleRecognizeMaterial());
            }
            if (UIService.elements.clearMaterialBtn) {
                UIService.elements.clearMaterialBtn.addEventListener('click', () => {
                    UIService.clearMaterial();
                    UIService.clearMessages();
                });
            }
            
            console.log('[App] bindEvents: 所有事件绑定完成');
        } catch (error) {
            console.error('[App] bindEvents: 事件绑定失败', error);
            throw error;
        }
    },
    
    // ==================== 化学反应讲解 ====================
    
    async handleGenerateReactionExplanation() {
        const reaction = UIService.getReactionInput();
        const level = UIService.getEducationLevel();
        
        if (!reaction) {
            UIService.showError('请输入化学反应描述');
            return;
        }
        
        try {
            UIService.showReactionExplainLoading();
            UIService.clearMessages();
            
            const result = await APIService.explainReaction(reaction, level, this.apiKey);
            UIService.setReactionExplainResult(result);
            UIService.showSuccess('反应讲解生成成功！');
        } catch (error) {
            UIService.showError(`生成反应讲解失败: ${error.message}`);
        } finally {
            UIService.hideReactionExplainLoading();
        }
    },
    
    // ==================== 方程式配平 ====================
    
    async handleBalanceEquation() {
        const equation = UIService.getEquationInput();
        
        if (!equation) {
            UIService.showError('请输入未配平的化学方程式');
            return;
        }
        
        try {
            UIService.showEquationBalanceLoading();
            UIService.clearMessages();
            
            const result = await APIService.balanceEquation(equation, this.apiKey);
            UIService.setEquationBalanceResult(result);
            UIService.showSuccess('方程式配平成功！');
        } catch (error) {
            UIService.showError(`配平方程式失败: ${error.message}`);
        } finally {
            UIService.hideEquationBalanceLoading();
        }
    },
    
    // ==================== 反应现象图像 ====================
    
    async handleGenerateImage() {
        const prompt = UIService.getImagePromptInput();
        
        if (!prompt) {
            UIService.showError('请输入反应现象描述');
            return;
        }
        
        try {
            UIService.showImageGenerationLoading();
            UIService.clearMessages();
            
            const imageUrl = await APIService.generateReactionImage(prompt, this.apiKey);
            
            if (!imageUrl) {
                throw new Error('未能生成图像');
            }
            
            UIService.setGeneratedImage(imageUrl);
            UIService.showSuccess('反应现象图像生成成功！');
        } catch (error) {
            UIService.showError(`生成图像失败: ${error.message}`);
        } finally {
            UIService.hideImageGenerationLoading();
        }
    },
    
    // ==================== 物质识别 ====================
    
    async handleRecognizeMaterial() {
        const file = UIService.getMaterialImageFile();
        
        if (!file) {
            UIService.showError('请选择要识别的图片');
            return;
        }
        
        try {
            UIService.showMaterialRecognitionLoading();
            UIService.clearMessages();
            
            // 转换为Data URL
            const imageUrl = await this.readFileAsDataURL(file);
            
            // 调用识别接口
            const result = await APIService.recognizeMaterial(imageUrl, this.apiKey);
            UIService.setMaterialRecognitionResult(result);
            UIService.showSuccess('物质识别成功！');
        } catch (error) {
            UIService.showError(`识别物质失败: ${error.message}`);
        } finally {
            UIService.hideMaterialRecognitionLoading();
        }
    },
    
    /**
     * 转换文件为Data URL
     */
    readFileAsDataURL(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            
            reader.onload = (e) => {
                resolve(e.target.result);
            };
            
            reader.onerror = (error) => {
                reject(error);
            };
            
            reader.readAsDataURL(file);
        });
    }
};

// 页面加载完成后初始化应用
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        console.log('[App] DOMContentLoaded 事件触发');
        App.init();
    });
} else {
    // 如果脚本加载时 DOM 已经准备好
    console.log('[App] DOM 已准备好，直接初始化');
    App.init();
}

// 导出应用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = App;
}
