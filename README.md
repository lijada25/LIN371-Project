# LIN371-Project
Code for LIN371 Final Project

The goal of the current project was to develop a binary classification pipeline that accurately detects Wernicke’s aphasia from other subtypes of aphasia using transcribed patient speech data. This project compares the performance of two classification models: Logistic Regression and Support Vector Machine (SVM). Towards the end of our research inquiry, we also conducted an ablation study to compare the performance of models trained on text-only linguistic features and a combination of clinical and textual features. We found that clinical features significantly improve classification performance; however, the models may overrely on clinically derived proxies (e.g., WAB scores), raising concerns about feature confounding between clinical severity measures and linguistic signal. 

* To isolate the Cinderella task in the patient CLAN transcriptions, run cinderella_isolation.py
* To extract patient-only speech, run patient speech.py
* clinical+text_jada.ipynb contains code training our models on a combination of clinical and textual features.
* text-only_jada.ipynb contains code training our models on text-only features. 
