# Computer Networks Quiz – CLI Application

A **console-based quiz application** designed to help **UBB Computer Science students** prepare for the **Computer Networks exam**.

The application supports multiple practice modes (such as *Quick Mode* and *Practice Mode*) and tracks your progress over time by storing correct and incorrect answers using JSON-based persistence.

---

## Features

- Multiple quiz modes (quick practice, full practice, etc.)
- Persistent tracking of correct / incorrect answers
- Questions stored in JSON format
- Easily reusable for other subjects
- Simple and intuitive CLI interface

---

## Default Usage (Exam Practice)

By default, the application already includes the **Computer Networks exam questions**.

To start practicing:
1. Clone the repository
2. Run:
   ```bash
   python main.py
   ```
3. Follow the instructions displayed in the console

---

## Custom Question Sets (Optional)

This application can be reused to practice **any subject**, as long as the questions follow the same JSON format.

### Steps

1. Open the `collections` folder  
2. Navigate to a desired folder and choose a topic  
3. Copy the contents of `questions.txt`  
4. Paste the content into `safety.json`  
5. Make sure the following files are **empty** to avoid unexpected behavior:
   - `question_status.json`
   - `questions.json`
6. Run:
   ```bash
   python main.py
   ```
7. Follow the CLI instructions and start practicing

---

## Notes

- `safety.json` contains the active set of questions
- `question_status.json` is automatically generated if missing or empty
- Clearing `question_status.json` resets your progress

---

## File Overview

- `main.py` – Application entry point  
- `safety.json` – Active question pool  
- `question_status.json` – Stores correct / incorrect statistics  
- `collections/` – Organized question sets by topic
- `questions.json/` - This is where the questions are generated in their final format using the safety.json file 
