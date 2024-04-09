import re
from pdfminer.high_level import extract_text
import datetime


def split_into_sentences(text):
    # Split text into sentences using regex
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    return sentences


def create_daily_schedule(text_sections, daily_study_time):
    # Calculate time per section (assuming 60 minutes per hour)
    time_per_section = int(daily_study_time * 60)

    # Initialize start time
    start_time = datetime.datetime.now()

    # Format schedule
    schedule = ""
    for i, section in enumerate(text_sections, start=1):
        section_start = start_time.strftime("%H:%M")
        start_time += datetime.timedelta(minutes=time_per_section)  # Update start time for the next section
        section_end = start_time.strftime("%H:%M")
        schedule += f"Section {i}: {section_start} - {section_end}\n{section.strip()}\n\n"

    return schedule.rstrip()  # Remove trailing newline


def create_study_plan(text, num_days=7, sections_per_day=3):
    # Set daily study time (handle potential errors)
    while True:
        try:
            daily_study_time = float(input("Enter the daily study time (in hours): "))
            if daily_study_time <= 0:
                raise ValueError("Daily study time must be positive.")
            break
        except ValueError:
            print("Invalid input. Please enter a positive number.")

    # Split the text into sentences
    sentences = split_into_sentences(text)

    # Split the sentences into sections
    sections = [sentences[i:i + sections_per_day] for i in range(0, len(sentences), sections_per_day)]

    # Create the study plan
    study_plan = {}
    for day in range(num_days):
        start_date = (datetime.date.today() + datetime.timedelta(days=day)).strftime('%A, %B %d')  # Format date
        daily_schedule = create_daily_schedule(sections[day % len(sections)], daily_study_time)
        study_plan[start_date] = daily_schedule

    return study_plan


def print_study_plan(study_plan):
    print("Study Plan:")
    for date, schedule in study_plan.items():
        print(f"\nDate: {date}")
        print(schedule)
        print("-" * 50)


def main():
    # Take input from the user for the PDF file path
    pdf_path = input("Enter the path to the PDF file: ")

    # Extract text from PDF
    text = extract_text(pdf_path)

    # Perform additional processing on the extracted text if needed
    pattern = re.compile(r"[a-zA-Z]+,\s")
    matches = pattern.findall(text)
    names = [n.strip(", ") for n in matches]
    print(names)

    # Create the study plan using the extracted text
    study_plan = create_study_plan(text)

    # Print the study plan
    print_study_plan(study_plan)


if _name_ == "_main_":
    main()
