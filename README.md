# Invoice Similarity Matcher

## Overview
Invoice Similarity Matcher is a system that categorizes incoming invoices by matching them to existing templates or previously processed invoices. The program extracts text content from PDFs, processes relevant features, and calculates similarity metrics to find the most similar invoice in the database.

## Features
- Extract text from PDF invoices using PyPDF2 and Tika.
- Extract relevant features such as invoice numbers, dates, amounts, and keywords.
- Store extracted invoice data in MongoDB.
- Calculate cosine similarity between feature vectors to find the most similar invoice.
- Automatically process multiple test invoices and compare them with the training data.

## Requirements
- Python 3.x
- PyPDF2
- Tika
- scikit-learn
- pymongo

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/invoice-similarity-matcher.git
    cd invoice-similarity-matcher
    ```

2. Install the required Python packages:
    ```bash
    pip install PyPDF2 tika scikit-learn pymongo
    ```

3. Set up Tika:
    - Download and install Apache Tika from [Tika Download](https://tika.apache.org/download.html).
    - Start the Tika server:
      ```bash
      java -jar tika-server-1.24.jar
      ```

4. Configure MongoDB:
    - Create a MongoDB Atlas cluster and get the connection string.
    - Replace `Your MongoDB URL` in the `connect_to_mongodb` function with your actual MongoDB connection string.

## Usage
1. Place your training PDF invoices in a directory (e.g., `train_directory`).
2. Place your test PDF invoices in another directory (e.g., `test_directory`).
3. Run the program:
    ```bash
    python main.py
    ```

## Code Structure
- `main.py`: Main script to run the program.
- `connect_to_mongodb()`: Connects to the MongoDB database.
- `insert_training_data(db, file_path)`: Inserts training data into MongoDB.
- `get_training_data(db)`: Retrieves training data from MongoDB.
- `calculate_similarity(features1, features2)`: Calculates cosine similarity between two feature sets.
- `find_most_similar_invoice(input_features, database)`: Finds the most similar invoice.
- `get_pdf_files_from_directory(directory_path)`: Retrieves PDF files from a specified directory.
- `extract_text_pypdf2(file_path)`: Extracts text from PDF using PyPDF2.
- `extract_text_tika(file_path)`: Extracts text from PDF using Tika.
- `extract_features(text)`: Extracts relevant features from text.

