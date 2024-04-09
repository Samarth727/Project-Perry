import re
import random
import string
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.util import ngrams
from nltk.corpus import stopwords
from pdfminer.high_level import extract_text

def generate_multiple_choice_question(bigram):
    options = [f"{bigram[0]} {bigram[1]}"]
    for _ in range(3):  # Generate 3 distractors
        distractor = ''.join(random.choices(string.ascii_lowercase, k=len(bigram[0]))) + ' ' + ''.join(random.choices(string.ascii_lowercase, k=len(bigram[1])))
        options.append(distractor)
    random.shuffle(options)
    return f"What is {bigram[0]} {bigram[1]}?\n" + '\n'.join([f"{i}. {option}" for i, option in enumerate(options, start=1)])

def generate_one_word_question(bigram):
    question_word = random.choice(bigram)
    return f"What is {question_word}?"

def generate_descriptive_question(bigram):
    return f"Describe {bigram[0]} {bigram[1]}."

def generate_questions(text, num_questions, question_type):
    sentences = sent_tokenize(text)
    questions = []

    for sentence in sentences:
        # Tokenize the sentence
        words = word_tokenize(sentence)

        # Remove stopwords and punctuation
        words = [word.lower() for word in words if word.lower() not in stopwords.words('english') and word not in string.punctuation]

        # Create bigrams from the words
        bigrams = list(ngrams(words, 2))

        # Generate questions based on the selected type
        for bigram in bigrams:
            if question_type == 'm':
                question = generate_multiple_choice_question(bigram)
                questions.append(question)
            elif question_type == 't':
                question = generate_one_word_question(bigram)
                questions.append(question)
            elif question_type == 'd':
                question = generate_descriptive_question(bigram)
                questions.append(question)

    return questions[:num_questions]

def main():
    pdf_path = input("Enter the path to the PDF file: ")
    text = extract_text(pdf_path)
    num_questions = int(input("Enter the number of questions to generate: "))
    question_type = input("Enter the type of questions to generate (m for multiple-choice, t for one-word, d for descriptive): ")

    if question_type.lower() not in ['m', 't', 'd']:
        print("Invalid question type.")
        return

    questions = generate_questions(text, num_questions, question_type)
    for i, question in enumerate(questions, start=1):
        print(f"Question {i}:")
        print(question)
        print()

if _name_ == "_main_":
    main()
