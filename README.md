# AWS Quiz Game - Japanese Names Edition

A fun and educational quiz game where AWS services are represented as fictional Japanese full names. Test your knowledge of AWS services by matching Japanese names to the correct AWS service.

## Overview

This game presents AWS services as fictional Japanese names and challenges players to identify the correct AWS service. Each name has been carefully crafted to metaphorically represent the AWS service's function or characteristics.

## Features

- Interactive quiz with multiple-choice questions
- Randomized selection of questions for each game session
- Visual feedback for correct and incorrect answers
- Explanations of the metaphorical connections between names and services
- Progress tracking and final score display
- Celebration effects for correct answers and high scores
- Sound effects for correct and incorrect answers

## Requirements

- Python 3.6+
- Pygame

## Installation

1. Clone this repository or download the source code
2. Install the required dependencies:

```bash
pip install pygame
```

## How to Play

1. Run the game:

```bash
python aws_quiz_game.py
```

2. For each question, click on the AWS service that you think matches the displayed Japanese name
3. After answering all questions, you'll see your final score
4. Press 'R' to restart the game or 'Q' to quit

## Game Mechanics

- Each game consists of 5 randomly selected questions from a larger pool
- For each question, you need to match a Japanese name to the correct AWS service
- After selecting an answer, you'll see if you were correct and an explanation of the name's connection to the service
- Your final score and a performance message will be displayed at the end

## Example Questions

- **高橋 龍 (Takahashi Ryu)** - Represents Amazon EC2
  - 高橋 (Takahashi) means 'high bridge', representing the connection to the cloud
  - 龍 (Ryu) means 'dragon', symbolizing EC2's powerful computing capabilities

- **水野 清 (Mizuno Sei)** - Represents Amazon RDS
  - 水野 (Mizuno) contains 水 (water)
  - 清 (Sei) means 'clear/pure', representing how RDS handles data flow like a well-managed stream of information

## Customization

You can add more questions by extending the `QUIZ_QUESTIONS` list in the source code. Each question should include:
- A Japanese name
- The correct AWS service
- An incorrect but plausible AWS service
- An explanation of the metaphorical connection

## Contributing

Contributions are welcome! Feel free to add more questions, improve the game mechanics, or enhance the visual effects.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
