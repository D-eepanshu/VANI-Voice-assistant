import json
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# Load extended intents dataset
with open('ML option/intents.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

texts = []
labels = []

# Prepare data
for intent in data:
    for example in intent['examples']:
        texts.append(example.lower().strip())
        labels.append(intent['intent'])

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42, stratify=labels)

# Convert text to TF-IDF 
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test) 

# Train Naive Bayes model
model = MultinomialNB()
model.fit(X_train_tfidf, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test_tfidf)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred, target_names=model.classes_)

print(f"✅ Training complete. Model saved as 'intent_model.pkl' and 'vectorizer.pkl'")
print(f"📊 Accuracy on the test set: {accuracy:.2f}")
print("\n🔥 Confusion Matrix:")
print(conf_matrix)

print("\nDetailed Classification Report:")
print(class_report)

# Visualize the confusion matrix
plt.figure(figsize=(10, 8))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues',
            xticklabels=model.classes_, yticklabels=model.classes_)
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix')
plt.show()

# Save trained model and vectorizer
joblib.dump(model, 'ML option/intent_model.pkl')
joblib.dump(vectorizer, 'ML option/vectorizer.pkl')