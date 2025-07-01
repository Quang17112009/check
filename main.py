const express = require('express');
const axios = require('axios');
const app = express();
const port = process.env.PORT || 3000;

const externalApiUrls = {
    LUCKYWIN: 'https://apiluck2.onrender.com/predict',
    LUCKYWIN (MD5): 'https://apiluckmd5.onrender.com/predict',
    // Thêm các URL API khác vào đây khi bạn có
};

const gameConfigurations = {
    "LUCKYWIN": {
        "initial_total_predictions": 80, 
        "initial_incorrect_predictions": 20, 
        "api_key": "LUCKYWIN"
    },
    "LUCKYWIN (MD5)": {
        "initial_total_predictions": 90,
        "initial_incorrect_predictions": 54,
        "api_key": null
    },
    "SUNWIN": {
        "initial_total_predictions": 90,
        "initial_incorrect_predictions": 54,
        "api_key": null
    },
    "B52": {
        "initial_total_predictions": 90,
        "initial_incorrect_predictions": 54,
        "api_key": null
    },
    "HITCLUB (Xanh)": {
        "initial_total_predictions": 90,
        "initial_incorrect_predictions": 54,
        "api_key": null
    },
    "Hit (đỏ)": {
        "initial_total_predictions": 90,
        "initial_incorrect_predictions": 54,
        "api_key": null
    }
};

app.get('/api/games', async (req, res) => {
    const finalResponseData = {};

    for (const gameName in gameConfigurations) {
        const config = gameConfigurations[gameName];
        const apiUrl = config.api_key ? externalApiUrls[config.api_key] : null;

        let totalPredictions = config.initial_total_predictions;
        let incorrectPredictions = config.initial_incorrect_predictions;
        let correctPredictions = totalPredictions - incorrectPredictions;

        let currentPredictionDetails = "Chưa có dữ liệu";

        if (apiUrl) {
            try {
                const apiResponse = await axios.get(apiUrl);
                if (apiResponse.data) {
                    const fullExternalData = apiResponse.data;
                    
                    // Lấy các phần dữ liệu cần thiết
                    const predictedValue = fullExternalData.du_doan;
                    const actualResultArray = fullExternalData.matches;
                    const phienMoi = fullExternalData.Phien_moi;
                    const phienDuDoan = fullExternalData.phien_du_doan;

                    currentPredictionDetails = {
                        "Phien_moi": phienMoi,
                        "phien_du_doan": phienDuDoan,
                        "du_doan": predictedValue,
                        "matches": actualResultArray
                    };

                    if (predictedValue && Array.isArray(actualResultArray) && actualResultArray.length > 0) {
                        const lastActualChar = actualResultArray[actualResultArray.length - 1];
                        let actualValue = null;

                        if (lastActualChar && typeof lastActualChar === 'string') {
                            const normalizedChar = lastActualChar.toLowerCase();
                            if (normalizedChar === 't') {
                                actualValue = 'Tài';
                            } else if (normalizedChar === 'x') {
                                actualValue = 'Xỉu';
                            }
                        }
                        
                        if (actualValue) {
                            totalPredictions += 1; 

                            if (predictedValue === actualValue) {
                                correctPredictions += 1;
                            } else {
                                incorrectPredictions += 1;
                            }
                        }
                    }
                }
            } catch (error) {
                console.error(`Lỗi khi lấy dữ liệu cho ${gameName} từ ${apiUrl}:`, error.message);
                currentPredictionDetails = "Lỗi khi lấy dữ liệu";
            }
        }

        finalResponseData[gameName] = {
            "Tong_phien_du_doan": totalPredictions,
            "du_doan_sai": incorrectPredictions,
            "du_doan_dung": correctPredictions,
            "current_prediction": currentPredictionDetails
        };
    }

    res.json(finalResponseData);
});

app.get('/', (req, res) => {
    res.send('API dự đoán game đang chạy!');
});

app.listen(port, () => {
    console.log(`Server đang lắng nghe tại http://localhost:${port}`);
});
