import re
import nltk
from pdfminer.high_level import extract_text
from nltk.corpus import stopwords
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def text_summarizer(text, num_sentences=3):
    # Tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)

    # Combine the sentences into a single string
    text = ' '.join(sentences)

    # Initialize a parser
    parser = PlaintextParser.from_string(text, Tokenizer("english"))

    # Initialize an LSA summarizer
    summarizer = LsaSummarizer()

    # Summarize the text
    summary = summarizer(parser.document, num_sentences)

    # Combine the summarized sentences into a single string
    summarized_text = ' '.join([str(sentence) for sentence in summary])

    return summarized_text

def main():
    # Extract text from PDF
    pdf_path = input("Enter the path to the PDF file: ")
    text = extract_text(pdf_path)

    # Set the number of sentences for the summary
    num_sentences = int(input("Enter the number of sentences for the summary (default is 3): ") or 3)

    # Summarize the text
    summarized_text = text_summarizer(text, num_sentences)

    # Print the summarized text
    print("Summarized Text:")
    print(summarized_text)

if _name_ == "_main_":
    main()
