/**
 * 项目配置文件
 * 存储 Python 后端配置
 */

const CONFIG = {
    // Python 后端配置
    PYTHON_BACKEND: {
        BASE_URL: 'http://localhost:5000',
        ENDPOINTS: {
            REACTION_EXPLAIN: '/api/reaction/explain',
            EQUATION_BALANCE: '/api/equation/balance',
            REACTION_IMAGE: '/api/reaction/image',
            MATERIAL_RECOGNIZE: '/api/material/recognize'
        }
    },
    
    // 教学阶段
    EDUCATION_LEVELS: {
        JUNIOR: 'junior',
        SENIOR: 'senior',
        JUNIOR_NAME: '初中',
        SENIOR_NAME: '高中'
    },
    
    // 超时时间
    TIMEOUTS: {
        SHORT: 5000,    // 5秒
        MEDIUM: 120000,  // 120秒（2分钟），足以应对大模型长时间生成
        LONG: 300000    // 300秒（5分钟）
    },
    
    // 功能特性标记
    FEATURES: {
        DEBUG_MODE: false  // 调试模式
    }
};

// 导出配置
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}
