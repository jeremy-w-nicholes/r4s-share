
# Roll for Shoes: The Heist Game

## Overview
This is a simplified text-based RPG game using **Roll for Shoes** mechanics, where the player attempts a heist by interacting with an AI Game Master (GM). Players perform actions, roll dice, gain experience, and level up their skills as they attempt to complete their objective. This game is built with **Python**, **Tkinter** for GUI, and the **OpenAI API** for generating responses and narrative twists.

## Features
- **Heist Adventure**: Players plan and execute a heist, interacting with a GM to narrate the story and determine outcomes.
- **AI-Powered Game Master**: The AI GM provides rich, dynamic storytelling, creating unique scenarios based on player actions.
- **Level-Up System**: Players start with the basic "Do Anything" skill and can gain new skills based on their actions.
- **Twists**: The AI introduces twists to keep the game unpredictable and exciting.
- **Dice Roll Animation**: Simple dice roll animations add visual feedback for player actions.

## Requirements

### Dependencies:
- **Python 3.8 or higher**
- **OpenAI Python Client Library** (`openai`)
- **python-dotenv** (`dotenv`)
- **Tkinter** (Python’s standard GUI package, typically pre-installed)

### Installation:

#### Linux:
1. Install Python 3 and Tkinter:
    ```bash
    sudo apt update
    sudo apt install python3 python3-tk
    ```
2. Create a virtual environment (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Install the required Python packages:
    ```bash
    pip install openai python-dotenv
    ```

#### Windows:
1. Install Python 3 and make sure to add Python to your PATH during installation.
2. Install Tkinter (usually included with Python):
    - If Tkinter is not installed, use:
    ```bash
    python -m pip install python-tk
    ```
3. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
4. Install the required Python packages:
    ```bash
    pip install openai python-dotenv
    ```

#### macOS:
1. Install Python 3 and Tkinter:
    ```bash
    brew install python-tk
    ```
2. Create a virtual environment (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Install the required Python packages:
    ```bash
    pip install openai python-dotenv
    ```

### Setup OpenAI API Key:
1. Create a `.env` file in the root directory of your project.
2. Add the following line to the `.env` file:
    ```
    OPENAI_API_KEY=your_openai_api_key_here
    ```
3. Replace `your_openai_api_key_here` with your actual API key from OpenAI.

### How to Run the Game:
1. Activate the virtual environment (if you created one).
2. Run the Python script:
    ```bash
    python main.py
    ```

## Game Mechanics

### The Objective:
You are part of a team on a mission to steal a highly coveted object. The AI Game Master will guide the story, generate the target object, and provide descriptions of the NPCs involved.

### Actions & Dice Rolls:
- **Do Anything**: This is the base skill, and all players start with it at level 1. If the action fits within a specific skill like "Sneak," "Hack," or "Fight," the player can use that skill if available.
- **Rolling**: The player rolls a number of D6s based on the level of their skill. The AI GM also rolls D6s based on the difficulty of the action.
- **Twists**: The AI introduces twists when actions are successful or tie, adding complexity to the story.
  
### XP & Leveling Up:
- **XP**: If a player fails a roll, they gain XP.
- **Leveling Up**: Skills level up when the XP threshold is reached, allowing the player to roll more dice for specific actions.

### Error Handling:
The game is designed to handle several potential errors during communication with the OpenAI API, such as:
- **APIError**
- **APIConnectionError**
- **RateLimitError**
- **Timeout**

If any errors occur, the player will be informed and the game will continue.

## How the Code Works

- **GameMaster Class**: Handles interactions with OpenAI, generating responses for the player’s actions, including twists, success/failure outcomes, and NPC descriptions.
- **Character Class**: Manages the player's skills, experience points (XP), and levels. Tracks actions and calculates dice rolls.
- **HeistGameGUI Class**: Manages the game’s graphical interface using Tkinter, including input fields, action buttons, and a scrollable text area to display game updates.
- **Dice Rolling**: The game animates dice rolls for a more engaging experience.
- **AI Responses**: The AI generates dynamic story elements based on the player's actions, ensuring no two games are alike.

## Known Issues & Future Improvements
- **Future Features**: Additional skills, more complex NPCs, and heist tools may be added in future updates.
- **Known Bugs**: None at the moment, but if any errors occur, ensure the `.env` file is correctly set and API limits are not exceeded.

## License
This project is licensed under the MIT License.
