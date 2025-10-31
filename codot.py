import time
import requests
from random import choice
from datetime import datetime
import uuid
import argparse
import hashlib
import sys
import os

# Fungsi clear screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Fungsi untuk menghasilkan device ID unik
def generate_device_id():
    return str(uuid.uuid4())

# Fungsi untuk membaca daftar pertanyaan dari file
def read_questions(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]

# Fungsi untuk mengirim pertanyaan ke NGL
def send_question(username, question, device_id, game_slug, session):
    url = f"https://ngl.link/{username}"
    headers = {
        "Referer": url,
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    data = {
        "username": username,
        "question": question,
        "deviceId": device_id,
        "gameSlug": game_slug,
        "referrer": ""
    }
    response = session.post("https://ngl.link/api/submit", headers=headers, data=data)
    return response

# Main program
def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="NGL Spammer")
    parser.add_argument("-u", "--username", required=True, help="Target NGL username")
    parser.add_argument("-n", "--num_questions", type=int, default=10, help="Number of questions to send (default: 10)")
    parser.add_argument("-d", "--delay", type=int, default=1, help="Delay between questions in seconds (default: 1)")
    args = parser.parse_args()

    # Load questions from files
    questions = read_questions("src/questions.txt")
    never_have_questions = read_questions("src/neverhave.txt")

    # Initialize session
    session = requests.Session()

    # Spamming loop
    for i in range(args.num_questions):
        # Randomly choose a question type
        question_type = choice(["general", "never_have"])

        if question_type == "general":
            question = choice(questions)
            game_slug = ""
        else:
            question = "I have never " + choice(never_have_questions)
            game_slug = "neverhave"

        # Generate device ID
        device_id = generate_device_id()

        # Send the question
        response = send_question(args.username, question, device_id, game_slug, session)

        if response.status_code == 200:
            print(f"[{i+1}] Question sent successfully!")
        else:
            print(f"[{i+1}] Error sending question. Status code: {response.status_code}")

        # Wait
        time.sleep(args.delay)

    print("Spamming complete!")

if __name__ == "__main__":
    main()
