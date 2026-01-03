# Russian vocabulary trainer
A Python-based language learning application that allows users to store 
Russian–Finnish vocabulary pairs (in theory, you can replace Finnish with any other language) 
and practice Russian word recall through an interactive game interface.
The project was created to experiment with different ways of memorizing words and short phrases.

## Features
- Simple interface for adding words and playing the game
- Stores user-defined word pairs in JSON files
- Asks for the Russian equivalent of the user’s words during a game session
- Tracks a score (0–3) for each word pair
- Permanently removes word pairs once a score of 3 is reached
- Allows the user to listen to the pronunciation of the Russian word after answering

## Setting Up 
You will have to set up **Conda, and Python3**.
* To create virtualenv `conda create --name myenv python=3.11`
* To activate the environment `conda activate myenv`
* To install dependencies: `pip install -r requirements.txt`
* To launch the game: `python main.py`
