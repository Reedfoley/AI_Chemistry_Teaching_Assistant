/**
 * API 工具模块
 * 处理 Python 后端 API 请求
 */

const APIService = {
    /**
     * 化学反应智能讲解
     * @param {string} reaction - 化学反应描述
     * @param {string} level - 教学阶段 (junior/senior)
     * @param {string} apiKey - API Key
     * @returns {Promise<string>} 反应讲解
     */
    async explainReaction(reaction, level, apiKey) {
        return this._explainReactionPython(reaction, level, apiKey);
    },
    
    /**
     * 配平化学方程式
     * @param {string} equation - 未配平的方程式
     * @param {string} apiKey - API Key
     * @returns {Promise<string>} 配平结果
     */
    async balanceEquation(equation, apiKey) {
        return this._balanceEquationPython(equation, apiKey);
    },
    
    /**
     * 生成反应现象图像
     * @param {string} prompt - 反应现象描述
     * @param {string} apiKey - API Key
     * @returns {Promise<string>} 图像 URL
     */
    async generateReactionImage(prompt, apiKey) {
        return this._generateReactionImagePython(prompt, apiKey);
    },
    
    /**
     * 识别实验物质
     * @param {string} imageUrl - 图片URL地址
     * @param {string} apiKey - API Key
     * @returns {Promise<string>} 物质识别结果
     */
    async recognizeMaterial(imageUrl, apiKey) {
        return this._recognizeMaterialPython(imageUrl, apiKey);
    },
    
    // ==================== Python 后端实现 ====================
    
    async _explainReactionPython(reaction, level, apiKey) {
        return this._fetchPythonAPI(
            CONFIG.PYTHON_BACKEND.ENDPOINTS.REACTION_EXPLAIN,
            {
                reaction: reaction,
                level: level,
                api_key: apiKey
            }
        );
    },
    
    async _balanceEquationPython(equation, apiKey) {
        return this._fetchPythonAPI(
            CONFIG.PYTHON_BACKEND.ENDPOINTS.EQUATION_BALANCE,
            {
                equation: equation,
                api_key: apiKey
            }
        );
    },
    
    async _generateReactionImagePython(prompt, apiKey) {
        const result = await this._fetchPythonAPI(
            CONFIG.PYTHON_BACKEND.ENDPOINTS.REACTION_IMAGE,
            {
                prompt: prompt,
                api_key: apiKey
            }
        );
        return result;
    },
    
    async _recognizeMaterialPython(imageUrl, apiKey) {
        return this._fetchPythonAPI(
            CONFIG.PYTHON_BACKEND.ENDPOINTS.MATERIAL_RECOGNIZE,
            {
                image_url: imageUrl,
                api_key: apiKey
            }
        );
    },
    
    async _fetchPythonAPI(endpoint, data) {
        try {
            const response = await fetch(
                CONFIG.PYTHON_BACKEND.BASE_URL + endpoint,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                }
            );
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            // 尝试读取为 JSON
            let result;
            try {
                result = await response.json();
            } catch (e) {
                // 如果 JSON 解析失败，返回文本
                const text = await response.text();
                result = { success: true, data: text };
            }
            
            if (result.success || result.status === 'success') {
                // 提取数据，优先使用 result.data
                const data = result.result || result.data || '';
                
                // 如果是对象，转换为JSON字符串
                if (typeof data === 'object') {
                    return JSON.stringify(data, null, 2);
                }
                
                return data || '';
            } else {
                throw new Error(result.error || '请求失败');
            }
        } catch (error) {
            throw new Error(`Python 后端请求失败: ${error.message}`);
        }
    },
    

};

// 导出 API 服务
if (typeof module !== 'undefined' && module.exports) {
    module.exports = APIService;
}
