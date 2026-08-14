# AI Fake News Detection & Verification System

A production-grade, college AI/ML project that detects fake news in text and image formats using **TF-IDF Vectorization** and **Logistic Regression**, with explainability features, OCR extraction, independent live news verification, and prediction history analytics.

---

## 🌟 Key Features

1. **Dual Input Mode**:
   - 📝 **Verify Text**: Paste full news articles for instant analysis.
   - 🖼️ **Verify Image**: Upload screenshots or news graphics (JPG, PNG) with automated **Tesseract OCR** text extraction.
2. **Machine Learning Pipeline**:
   - **Text Preprocessing**: URL removal, special symbol filtering, lowercase normalization.
   - **TF-IDF Vectorizer**: Converts article text into weighted n-gram numerical vectors.
   - **Logistic Regression**: Primary binary classifier predicting `FAKE` (0) or `REAL` (1) with probability confidence score.
3. **Model Explainability ("Why did the AI make this prediction?")**:
   - Analyzes Logistic Regression feature coefficients $\beta$ multiplied by TF-IDF values $x_i$ to output the top positive/negative influential vocabulary signals.
4. **News Category Classification**:
   - Predicts category (`Politics`, `Sports`, `Technology`, `Health`, `Business`, `Entertainment`).
5. **Trusted Source Verification**:
   - Extracts key search terms from the article and queries live **News API** indices (Reuters, BBC, AP, The Hindu) for corroborating reporting.
6. **Analytics Dashboard**:
   - Persists prediction history in a local **SQLite** database (`data/history.db`).
   - Tracks total predictions, Real/Fake breakdown, average confidence, and recent logs table.

---

## 🛠️ Project Structure

```
project/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── endpoints.py
│   │   ├── services/
│   │   │   ├── model_service.py
│   │   │   ├── ocr_service.py
│   │   │   ├── verify_service.py
│   │   │   └── db_service.py
│   │   ├── main.py
│   │   └── config.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── Hero.jsx
│   │   │   ├── HowItWorks.jsx
│   │   │   ├── VerifySection.jsx
│   │   │   ├── ResultCard.jsx
│   │   │   ├── ExplainabilityCard.jsx
│   │   │   ├── SourceVerification.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   └── Footer.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   └── index.css
│   └── package.json
├── models/
│   ├── fake_news_model.joblib
│   └── tfidf_vectorizer.joblib
├── data/
│   ├── training_data.csv
│   └── history.db
├── scripts/
│   └── train_model.py
├── .env.example
└── README.md
```

---

## 🚀 Setup & Installation Instructions

### 1. Environment & Dependencies

#### Backend (Python)
```bash
# Navigate to backend directory
cd backend

# Install Python requirements
pip install -r requirements.txt
```

#### Tesseract OCR Setup
- **Windows**: Download and install [Tesseract-OCR for Windows](https://github.com/UB-Mannheim/tesseract/wiki). Ensure `tesseract.exe` is added to system `PATH`.
- **Linux/Ubuntu**: `sudo apt-get install tesseract-ocr`
- **macOS**: `brew install tesseract`

---

### 2. Model Training

Train the TF-IDF Vectorizer and Logistic Regression classifier on your CSV dataset:

```bash
# Run training pipeline from project root
python scripts/train_model.py
```

- **Dataset CSV format (`data/training_data.csv`)**:
  - Columns: `title`, `text`, `category`, `label`
  - Labels: `0` = Fake, `1` = Real
- Outputs saved to `models/fake_news_model.joblib` and `models/tfidf_vectorizer.joblib`.

---

### 3. Environment Variables (News API Setup)

Create a `.env` file in the project root based on `.env.example`:

```env
NEWS_API_KEY=your_actual_news_api_key_here
```
*Note: If no API key is provided, the system gracefully informs the user that live source verification is unconfigured without breaking or faking data.*

---

### 4. Running the Application

#### Start FastAPI Backend
```bash
# From project root directory
python backend/app/main.py
```
Backend API will start at: `http://localhost:8000` (Docs available at `http://localhost:8000/docs`).

#### Start React Frontend
```bash
# Open a new terminal tab and navigate to frontend
cd frontend

# Install npm packages
npm install

# Start Vite development server
npm run dev
```
Frontend web app will open at: `http://localhost:5173`.

---

## 📊 Evaluation & Machine Learning Workflow

The Logistic Regression model uses TF-IDF features to optimize log-loss:

$$P(Y=1|X) = \frac{1}{1 + e^{-(\beta_0 + \sum \beta_i x_i)}}$$

Training logs display:
- **Accuracy**
- **Precision**
- **Recall**
- **F1 Score**
- **Confusion Matrix**
