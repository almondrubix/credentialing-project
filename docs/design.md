
# Credentialing Interview Evaluation System Design

## Overview
This system evaluates candidate responses to interview scenarios, scoring them on originality, teamwork, business savvy, and conscientiousness. It simulates a real-world pipeline for credentialing interviews using mock data and local storage.

## Architecture
- **Frontend**: React (with Vite) for user interaction.
- **Backend**: Flask for processing logic and SQLite for persistence.
- **Database**: SQLite with a `responses` table to store answers and scores.

![Architecture Diagram](./architecture-diagram.png) <!-- Add a diagram here later -->

## Component Details
### Frontend
- Collects user input and displays scenarios, scores, and follow-ups.
- Uses state management for question and answer handling.
- Styled to mimic the ChatGPT interface.

### Backend
- Serves scenarios and follow-ups.
- Implements scoring logic with silent baseline comparison.
- Stores responses and scores in the SQLite database.

### Database Schema
- `responses` table:
  - `id` (int, primary key)
  - `scenario` (text)
  - `candidate_answer` (text)
  - `baseline` (text)
  - `uniqueness` (int)
  - `teamwork` (int)
  - `biz_savvy` (int)
  - `conscientiousness` (int)

## Workflow
1. Fetch the initial scenario from the backend.
2. Submit the candidate's answer.
3. Compare the answer to a hidden baseline for scoring.
4. Generate a follow-up question and a new baseline.
5. Store the response and scores in the database.
6. Repeat for subsequent questions.

## Future Improvements
- Integrate with an LLM for dynamic baselines and follow-ups.
- Enhance scoring logic for more nuanced evaluation.
- Deploy the app for online access.

## Challenges
- Balancing simplicity for local testing with scalability for future deployment.
- Mock logic may diverge from real-world scenarios.

