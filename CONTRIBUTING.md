# Contributing to the Neuronal Spike Detection Project

Thank you for contributing to this project! We primarily use GitHub Desktop for collaboration to make version control accessible, even for team members newer to coding. This guide provides step-by-step instructions to help you work effectively.

---

## Getting Started

### 1. **Install GitHub Desktop**
   - If you haven't already, download and install [GitHub Desktop](https://desktop.github.com/).

### 2. **Clone the Repository**
   - Open GitHub Desktop.
   - Sign in with your GitHub account.
   - Click `File > Clone Repository`.
   - Select this repository from your list or enter its URL, then choose a local folder to save it.

### 3. **Set Up the Project**
   - Ensure Python 3.8 or later is installed on your machine.
   - Open a terminal in the project folder and install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

### 4. **Sync Regularly**
   - Before starting work, click the `Fetch Origin` button in GitHub Desktop to pull the latest changes from the `main` branch.

---

## Workflow for Contributions Using GitHub Desktop

### 1. **Create a Branch**
   - In GitHub Desktop, go to the `Current Branch` menu and select `New Branch`.
   - Name your branch descriptively, like `feature/preprocessing` or `fix/spike-detection`.

### 2. **Write Your Code**
   - Open the project in your preferred code editor.
   - Implement your assigned task or changes.

### 3. **Commit Your Changes**
   - Once you've made changes, return to GitHub Desktop.
   - Review the changes in the `Changes` tab.
   - Write a clear and descriptive commit message, then click `Commit to [your branch name]`.

### 4. **Push Your Changes**
   - Click `Push Origin` in GitHub Desktop to upload your branch to the remote repository.

### 5. **Open a Pull Request**
   - After pushing your branch, GitHub Desktop will provide a link to open a pull request (PR) on GitHub. Alternatively, you can go to the repository page on GitHub and open a PR manually.
   - Include a clear explanation of your changes and link any related issues or tasks.

---

## Guidelines

### Code Style
- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code style.
- Use meaningful and descriptive names for variables and functions.

### Documentation
- Add comments for complex logic and use docstrings for functions:
  ```python
  def preprocess_data(data: list) -> list:
      """
      Processes raw electrical signal data for analysis.

      Args:
          data (list): Raw signal data.

      Returns:
          list: Processed signal data.
      """
### Testing

#### Example: Testing your code locally
# Run the code to verify it works as expected
    ```python
        from my_module import preprocess_data
        
        data = [0.1, 0.5, 0.9]
        processed_data = preprocess_data(data)
        assert isinstance(processed_data, list), "Output should be a list"

# Example: Adding a test using pytest
# Save this file in the 'tests' folder, e.g., tests/test_preprocess.py
    ```python
    import pytest
    from my_module import preprocess_data
    
    def test_preprocess_data():
        data = [0.1, 0.5, 0.9]
        result = preprocess_data(data)
        assert len(result) == len(data), "Output length should match input"
        assert all(isinstance(x, float) for x in result), "All elements should be floats"

# Resolving Conflicts in GitHub Desktop
## Step 1: Pull the Latest Changes
### If GitHub Desktop notifies you of a conflict:
1. Open GitHub Desktop.
2. Click the "Pull Origin" button to fetch the latest changes from the main branch.

## Step 2: Resolve Conflicts
1. Navigate to the "Changes" tab in GitHub Desktop.
2. Locate files marked as "conflicted."
3. Click on a conflicted file to open the merge tool.
4. Review both versions of the code. Choose which changes to keep, or combine changes as necessary.

## Step 3: Commit the Resolved Changes
1. After resolving all conflicts, commit your changes in GitHub Desktop.
2. Click "Push Origin" to upload the updated branch.

# Need Help?

## If you encounter issues:
- Discuss during team meetings or ask questions in the communication channel.
- Open a GitHub issue if the problem is technical.

## Reminder:
We are here to support your contributions and help resolve any issues!
