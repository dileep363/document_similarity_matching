import os
from pymongo import MongoClient
from PyPDF2 import PdfReader
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from tika import parser

def connect_to_mongodb():
    connection_string = "Your MongoDB URL"
    client = MongoClient(connection_string)
    return client['mydatabase']['invoices']  

def insert_training_data(db, file_path):
    text = extract_text_pypdf2(file_path)
    features = extract_features(text)
    keywords = ' '.join(features['keywords'])
    db.insert_one({'file_path': file_path, 'keywords': keywords})

def get_training_data(db):
    return list(db.find())

def calculate_similarity(features1, features2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([features1, features2])
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return cosine_sim[0][0]

def find_most_similar_invoice(input_features, database):
    max_similarity = 0
    most_similar_invoice_path = None
    for record in database:
        db_features = record['keywords']
        file_path = record['file_path']
        similarity = calculate_similarity(input_features, db_features)
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_invoice_path = file_path
    return most_similar_invoice_path, max_similarity

def get_pdf_files_from_directory(directory_path):
    return [os.path.join(directory_path, file_name) for file_name in os.listdir(directory_path) if file_name.lower().endswith('.pdf')]

def extract_text_pypdf2(file_path):
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_tika(file_path):
    parsed = parser.from_file(file_path)
    return parsed['content']

def extract_features(text):
    invoice_number = re.findall(r'Invoice Number: (\d+)', text)
    dates = re.findall(r'\d{2}/\d{2}/\d{4}', text)
    amounts = re.findall(r'\d+\.\d{2}', text)
    
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform([text])
    keywords = vectorizer.get_feature_names_out()

    return {
        'invoice_number': invoice_number,
        'dates': dates,
        'amounts': amounts,
        'keywords': keywords
    }

def main(test_directory_path, train_directory_path):
    db = connect_to_mongodb()

    train_paths = get_pdf_files_from_directory(train_directory_path)
    for path in train_paths:
        insert_training_data(db, path)

    database = get_training_data(db)

    test_paths = get_pdf_files_from_directory(test_directory_path)
    for input_invoice_path in test_paths:
        input_text = extract_text_pypdf2(input_invoice_path)
        input_features = ' '.join(extract_features(input_text)['keywords'])
        print(f"Testing File: {input_invoice_path}")
        print(f"Input Features: {input_features}")

        most_similar_invoice_path, similarity_score = find_most_similar_invoice(input_features, database)
        print(f"Most similar invoice file path: {most_similar_invoice_path}")
        print(f"Similarity score: {similarity_score}")
        print("-" * 40)

if __name__ == "__main__":
    train_directory = r"Training Directory path"
    test_directory = r"Testing Directory path"
    
    main(test_directory, train_directory)
