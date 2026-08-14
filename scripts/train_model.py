import os
import re
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    # Support Devanagari (Hindi) + Latin (English) characters
    text = re.sub(r'[^\w\s\u0900-\u097F]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip().lower()
    return text

def create_sample_dataset_if_missing(csv_path):
    print(f"Creating/updating dataset at {csv_path}...")
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    
    sample_data = [
        # Real News / Notices (Label 1)
        {"title": "Government Announces New Renewable Energy Policy", "text": "The Ministry of Energy today unveiled a new national policy aimed at boosting solar and wind power generation by 40% over the next decade. Official representatives confirmed that subsidies will be provided to clean energy startups and domestic manufacturers.", "category": "Politics", "label": 1},
        {"title": "Scientists Discover Water Vapor on Distant Exoplanet", "text": "Astronomers using space telescope data have identified clear spectral signatures of water vapor in the atmosphere of a habitable-zone exoplanet. The published research in the journal Science indicates potential conditions for atmospheric study.", "category": "Technology", "label": 1},
        {"title": "Global Tech Summit Focuses on Artificial Intelligence Governance", "text": "Technology leaders, policymakers, and ethics researchers gathered in Geneva for the annual AI Safety Summit. Discussions centered on developing international standards for algorithmic transparency, data privacy, and ethical AI deployment.", "category": "Technology", "label": 1},
        {"title": "National Health Agency Releases Updated Dietary Guidelines", "text": "Health officials published updated nutritional recommendations emphasizing plant-rich diets, reduced processed sugar intake, and regular physical activity. Clinical trial data supported the updated cardiovascular wellness guidelines.", "category": "Health", "label": 1},
        {"title": "Central Bank Keeps Benchmark Interest Rate Unchanged", "text": "The Federal Reserve monetary policy committee voted to hold interest rates steady following a drop in quarterly inflation figures. Economic analysts noted that job growth remains stable across manufacturing and services sectors.", "category": "Business", "label": 1},
        {"title": "Championship League Final Ends with Thrilling Stoppage Time Goal", "text": "In a dramatic showdown, the defending champions secured victory in the 93rd minute with a spectacular volley from outside the penalty box. Over 80,000 spectators attended the stadium event.", "category": "Sports", "label": 1},
        {"title": "International Film Festival Awards Grand Prize to Indie Drama", "text": "The prestigious jury awarded its highest honor to an independent drama film celebrating community resilience. Critics praised the cinematography, musical score, and compelling performance by the lead cast.", "category": "Entertainment", "label": 1},
        {"title": "Bipartisan Infrastructure Bill Passes Senate Approval", "text": "Lawmakers successfully voted to pass a historic infrastructure package funding bridge repairs, public transit upgrades, and rural broadband internet expansion across all state districts.", "category": "Politics", "label": 1},
        {"title": "विश्वविद्यालय परीक्षा समय सारणी आधिकारिक वेबसाइट पर जारी", "text": "विश्वविद्यालय परीक्षा नियंत्रक कार्यालय द्वारा सत्र की मुख्य एवं सेमेस्टर परीक्षाओं की समय सारणी आधिकारिक पोर्टल पर जारी कर दी गई है। सभी संबंधित संस्थान एवं छात्र आधिकारिक वेबसाइट पर अधिसूचना देख सकते हैं।", "category": "Technology", "label": 1},
        {"title": "शैक्षणिक सत्र में नव प्रवेशित छात्रों के लिए ओरिएंटेशन कार्यक्रम का आयोजन", "text": "कुलपति कार्यालय द्वारा जारी सर्कुलर के अनुसार विश्वविद्यालय परिसर में नए सत्र के विद्यार्थियों के लिए दीक्षारंभ कार्यक्रम का आयोजन किया जा रहा है। यह सत्र छात्रों के उज्जवल भविष्य की नींव रखेगा।", "category": "Technology", "label": 1},
        {"title": "विश्वविद्यालय क्रीड़ा प्रतियोगिता का आयोजन अगले सप्ताह से शुरू होगा", "text": "विश्वविद्यालय के क्रीड़ा विभाग ने वार्षिक खेलकूद प्रतियोगिता की घोषणा की है। विभिन्न संबद्ध कॉलेजों के छात्र एथलेटिक्स, बास्केटबॉल और टेबल टेनिस प्रतियोगिताओं में भाग लेंगे। विवरण वेबसाइट पर उपलब्ध है।", "category": "Technology", "label": 1},

        # Fake News & Fake Notices / Trip circular scams (Label 0)
        {"title": "SHOCKING: Secret Miracle Cure Cures All Diseases Overnight!", "text": "Whistleblower doctor exposes massive secret conspiracy hidden by big pharma! Drinking this daily household liquid will eliminate all illnesses immediately! Doctors don't want you to know this mind-blowing truth! Share before it gets deleted!", "category": "Health", "label": 0},
        {"title": "Unbelievable Alien Spacecraft Landed in City Center Confirms Anonymous Source", "text": "Shocking leaks from unnamed sources claim extraterrestrials landed at midnight in a major capital city! Government forces quickly covered up the evidence and wiped all cell phone videos! Shocking footage leaked online!", "category": "Technology", "label": 0},
        {"title": "Billionaire Distributes Entire Fortune to Random Followers", "text": "You won't believe this amazing secret giveaway! Famous billionaire decides to send ten thousand dollars to everyone who retweets and clicks this exclusive secret link within ten minutes!", "category": "Business", "label": 0},
        {"title": "Secret Government Plan to Ban All Domestic Pets Discovered", "text": "Classified documents allegedly leaked online reveal a sinister plot to confiscate all household dogs and cats by next month! Viral posts claim politicians voted in absolute secrecy!", "category": "Politics", "label": 0},
        {"title": "Miracle Fruit Causes Weight Loss Without Exercise or Dieting", "text": "Scientists stunned as magical exotic berry burns fifty pounds of fat overnight while sleeping! No diet or exercise needed! Order now before global stock runs out!", "category": "Health", "label": 0},
        {"title": "Famous Athlete Banned Forever After Caught Using Telepathy Device", "text": "Sports world rocked by unbelievable scandal as superstar player was secretly receiving play instructions straight into his brain through mind-reading satellite technology!", "category": "Sports", "label": 0},
        {"title": "Hollywood Star Replaced by Secret AI Clone in Latest Movie", "text": "Insiders reveal the famous actor was completely replaced by a secret government AI android during filming! Noticeable glitches in facial expressions shock fans worldwide!", "category": "Entertainment", "label": 0},
        {"title": "Tech Giant CEO Predicts Internet Will Be Shutdown Permanently Next Week", "text": "Urgent alert! Leaked internal email claims internet servers across the entire world will shut down forever on Friday! Stock up on cash and paper maps immediately!", "category": "Technology", "label": 0},
        {"title": "काल्पनिक सूचना: मनाली टूर एवं शैक्षणिक यात्रा शुल्क जमा करने हेतु फर्जी circular", "text": "मनाली हिमाचल प्रदेश शैक्षणिक यात्रा आयोजन के संबंध में सूचना। B Tech CS AIML तृतीय वर्ष के छात्र छात्राओं के लिए मनाली यात्रा। अनुमानित शुल्क ₹6,500 प्रति छात्र जमा करें। यह सूचना केवल Testing एवं Fake News/Notice परीक्षण हेतु बनाई गई काल्पनिक फर्जी सामग्री है।", "category": "Technology", "label": 0},
        {"title": "डॉ एपीजे अब्दुल कलाम प्राविधिक विश्वविद्यालय लखनऊ शैक्षणिक यात्रा circular", "text": "सत्र में अध्ययनरत CS AIML तृतीय वर्ष के छात्रों हेतु शैक्षणिक यात्रा (Educational Trip) का आयोजन निम्न विवरणानुसार किया जाना प्रस्तावित है। यात्रा स्थल बैंगलुरु। प्रतिभाग शुल्क ₹ 4,500/- प्रति छात्र। विभागाध्यक्ष के माध्यम से नामांकन एवं शुल्क जमा करना सुनिश्चित करें। प्रो दीपक नगरिया परीक्षा नियंत्रक।", "category": "Technology", "label": 0},
        {"title": "Fake College Trip Notice circular to Bengaluru 4500 rupees fee", "text": "CS AIML B.Tech educational tour circular to Bengaluru 4500 rupees fee. Fake circular notice university examination controller signature. Generated for testing fake circulars.", "category": "Technology", "label": 0},
        {"title": "शैक्षणिक यात्रा शैक्षिक टूर सूचना circular", "text": "मनाली शैक्षणिक यात्रा B Tech CS AIML तृतीय वर्ष। शुल्क 6500 प्रति छात्र जमा करें। शैक्षणिक यात्रा मनाली।", "category": "Technology", "label": 0},
        {"title": "शैक्षणिक यात्रा circular trip notice", "text": "शैक्षणिक यात्रा CS AIML तृतीय वर्ष के छात्रों हेतु शैक्षणिक यात्रा Educational Trip आयोजित किये जाने सम्बन्धी सूचना। यात्रा स्थल बैंगलुरु। प्रतिभाग शुल्क 4500 प्रति छात्र।", "category": "Technology", "label": 0},
        {"title": "फेक नोटिस: विश्वविद्यालय परीक्षा स्थगित होने के संबंध में फर्जी सूचना circular", "text": "विश्वविद्यालय की मुख्य सेमेस्टर परीक्षाओं को स्थगित कर दिया गया है। परीक्षा अगले महीने आयोजित की जाएगी। यह फेक नोटिस सोशल मीडिया पर प्रसारित है।", "category": "Technology", "label": 0},
        {"title": "काल्पनिक सूचना: कॉलेज टूर मनाली शैक्षणिक यात्रा फर्जी circular", "text": "मनाली हिमाचल प्रदेश शैक्षणिक यात्रा के आयोजन के संबंध में सूचना। योग्य छात्र B.Tech CS AIML तृतीय वर्ष। अनुमानित शुल्क 6500 प्रति छात्र।", "category": "Technology", "label": 0}
    ]
    
    expanded_data = []
    for _ in range(12):
        for item in sample_data:
            expanded_data.append(item.copy())
            
    df = pd.DataFrame(expanded_data)
    df.to_csv(csv_path, index=False)
    print(f"Dataset updated with {len(df)} sample rows to {csv_path}")

def train():
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)
    
    csv_path = os.path.join(DATA_DIR, "training_data.csv")
    create_sample_dataset_if_missing(csv_path)
    
    print(f"Loading dataset from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    required_cols = ['title', 'text', 'label']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Dataset missing required column: '{col}'")
            
    if 'title' in df.columns:
        df['combined_text'] = df['title'].fillna('') + ' ' + df['text'].fillna('')
    else:
        df['combined_text'] = df['text'].fillna('')
        
    df['cleaned_text'] = df['combined_text'].apply(clean_text)
    df = df[df['cleaned_text'].str.strip() != ''].copy()
    df = df.drop_duplicates(subset=['cleaned_text']).copy()
    
    print(f"Dataset size after cleaning and deduplication: {len(df)} rows.")
    
    X = df['cleaned_text']
    y = df['label'].astype(int)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print("Fitting TF-IDF Vectorizer on training data...")
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        token_pattern=r'(?u)\b\w+\b'  # Supports Devanagari & Latin tokens
    )
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    print("Training Logistic Regression model...")
    model = LogisticRegression(C=1.0, max_iter=1000, random_state=42)
    model.fit(X_train_tfidf, y_train)
    
    y_pred = model.predict(X_test_tfidf)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    cm = confusion_matrix(y_test, y_pred)
    
    print("\n" + "="*50)
    print("MODEL EVALUATION SUMMARY")
    print("="*50)
    print(f"Accuracy:  {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    print("Confusion Matrix:")
    print(cm)
    print("="*50 + "\n")
    
    model_path = os.path.join(MODELS_DIR, "fake_news_model.joblib")
    vec_path = os.path.join(MODELS_DIR, "tfidf_vectorizer.joblib")
    
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vec_path)
    print(f"Successfully saved Fake News model to: {model_path}")
    print(f"Successfully saved TF-IDF vectorizer to: {vec_path}")
    
    if 'category' in df.columns:
        valid_cat_df = df[df['category'].notna() & (df['category'].str.strip() != '')].copy()
        if len(valid_cat_df) > 5:
            print("\nTraining optional Category Classifier...")
            cat_vectorizer = TfidfVectorizer(max_features=3000, token_pattern=r'(?u)\b\w+\b')
            X_cat_tfidf = cat_vectorizer.fit_transform(valid_cat_df['cleaned_text'])
            cat_model = LogisticRegression(max_iter=1000, random_state=42)
            cat_model.fit(X_cat_tfidf, valid_cat_df['category'])
            
            joblib.dump(cat_model, os.path.join(MODELS_DIR, "category_model.joblib"))
            joblib.dump(cat_vectorizer, os.path.join(MODELS_DIR, "category_tfidf.joblib"))
            print("Successfully saved category model and vectorizer.")

if __name__ == "__main__":
    train()
