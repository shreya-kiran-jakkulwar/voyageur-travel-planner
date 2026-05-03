# Voyageur: AI-Powered Travel Planner

Voyageur is a sophisticated CLI application that generates detailed, structured travel itineraries using LLMs via the OpenRouter API. It doesn't just list places; it plans your entire day, estimates costs, and even tells you what to pack.
##  Features

- ** Context-Aware Planning**: Generates trips based on destination, duration, budget, and personal interests.
- ** Cost Aggregation**: Automatically calculates the total estimated cost of your entire trip in INR.
- ** Smart Packing List**: Tailors a packing list specifically for your destination's climate and planned activities.
- ** Beautiful Terminal UI**: Uses ANSI colors and clean ASCII formatting for a premium CLI experience.
- ** Robust Error Handling**: Includes automatic retry logic for API parsing and UTF-8 enforcement for Windows terminals.
- ** Modular Architecture**: Cleanly separated concerns between API logic, schemas, prompts, and formatting.
- 
##  Getting Started

### Prerequisites
- Python 3.10+
- An [OpenRouter API Key](https://openrouter.ai/)
  
### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/shreya-kiran-jakkulwar/voyageur-travel-planner.git
   cd voyageur-travel-planner
   
Set up a virtual environment:

bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
Install dependencies:

   bash
pip install -r requirements.txt
Configure your environment: Create a .env file in the root directory and add your API key:

env
OPENROUTER_API_KEY=your_actual_key_here

Usage
Run the main script to start planning:

   bash
python main.py
Simply describe your dream trip (e.g., "A 3-day budget solo trip to Kyoto focused on temples and ramen"), and let Voyageur do the rest.

Project Structure
main.py: The CLI entry point and orchestrator.
client.py: Handles communication with OpenRouter/LLMs.
prompts/: Contains the system instructions and AI persona logic.
schemas/: Defines the strict JSON structure for predictable AI outputs.
utils/: Houses the formatting engine and color logic.
