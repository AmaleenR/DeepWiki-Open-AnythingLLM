# My AnythingLLM Project

This project connects to an [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm) instance using its REST API.  
It allows you to send requests to your local or hosted AnythingLLM environment.

## Prerequisites
- Python 3.10+
- Virtual environment tool (venv or virtualenv)
- Access to an AnythingLLM instance (local or hosted)

## Installation

1. Clone this repository:
   ```bash
   git clone <your_repo_url>
   cd <repo_name>
2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   ```

   Activate the virtual environment
    ```bash
    venv\Scripts\Activate.ps1 #On Windows (PowerShell)
    venv\Scripts\activate.bat #On Windows (Command Prompt)
    source venv/bin/activate  #On macOS/Linux
    ```
  
3. Install dependencies
   ```bash
   pip install requests python-dotenv

4. Create a `.env` file in the root directory and add the following:
   ```env
   ANYTHINGLLM_API_KEY=your_anythingllm_api_key_here
   ANYTHINGLLM_API_URL=http://localhost:{port}/api/v1

5. Update the local folder path in deepwiki_to_anythingllm.py
   Find the variable for the Deepwiki output folder and update it:
   ```bash
   LOCAL_FOLDER = r"C:\Users\<username>\.adalflow\wikicache" 
   ```
7. Update the workspace slug in deepwiki_to_anythingllm.py
   ```bash
   WORKSPACE_SLUG = "your-workspace-slug"
   ```

8. Running the App
     Activate the virtual environment, then:
      ```bash
      python deepwiki_to_anythingllm.py

## Notes
- Do **NOT** commit `.env` to the repository.
- `.venv` is your local virtual environment folder; it should also be in `.gitignore`.
- Example `.gitignore`:
``` bash
# Environment files
.env

# Virtual environment
.venv/
venv/
