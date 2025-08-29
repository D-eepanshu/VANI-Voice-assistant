# VANI-Voice-assistant
This project is an Intent Classification System built using Machine Learning (Naive Bayes) and TF-IDF Vectorization. It classifies user inputs into predefined categories (intents) such as greetings, farewells, or requests.

# 🎙️ Intent Classification using Machine Learning  

This project implements an **Intent Classification System** for Natural Language Processing (NLP) tasks.  
It uses **TF-IDF (Term Frequency–Inverse Document Frequency)** for feature extraction and a **Naive Bayes Classifier** for training the model on extended intents dataset.  

The trained model can classify user queries into predefined **intents** and can be used in **chatbots, voice assistants, or AI applications**.  

---

## 🚀 Features  

- 📂 Loads intents dataset from `intents.json`  
- 🔤 Text preprocessing with **TF-IDF Vectorizer**  
- 🧠 Intent classification using **Multinomial Naive Bayes**  
- 📊 Model evaluation with **accuracy, confusion matrix, precision, recall, F1-score**  
- 🎨 Visualization of confusion matrix using **Seaborn Heatmap**  
- 💾 Saves trained model (`intent_model.pkl`) and vectorizer (`vectorizer.pkl`) for reuse  

---

## 📁 Project Structure  

ML option/
│── intents.json # Dataset of intents with examples
│── intent_model.pkl # Trained Naive Bayes model
│── vectorizer.pkl # TF-IDF vectorizer
│── train_intent_model.py # Main training script

---

## ⚙️ Installation  

1. Clone the repository:  
   ```bash
   git clone https://github.com/your-username/intent-classification.git
   cd intent-classification

