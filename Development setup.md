""
This document help you set up a development environment for Kotlin using Visual Studio Code (VS Code), React, python and Maven.
""
1. git setup (if needed):
- Install git from: https://git-scm.com/downloads
- Configure git:
  - git config --global user.name "Your Name"
  - git config --global user.email "your.email@example.com"

2. Install VS Code extensions for Kotlin and Maven:

"Extension Pack for Java" by Microsoft (includes Maven support), and "Language Support for Java(TM)" by Red Hat for build tool integration.

3. Install JDK:
Download JDK (LTS versions) from: https://adoptium.net/

- Set java in path:
  - Windows: Set JAVA_HOME and update PATH in Environment Variables.
  - macOS/Linux: Add export JAVA_HOME and export PATH to ~/.bashrc or ~/.zshrc.

- Setting JAVA_HOME Permanently in Windows:
  1. Win + X -> System → Avanserte systeminstillinger → Miljøvariabler
  2. Under System variables, click New, set Variable name to JAVA_HOME and Variable value to JDK installation path (e.g., C:\Program Files\Java\jdk-17).
  3. Select the PATH variable, click Edit, and add %JAVA_HOME%\bin to the list.
  4. Click OK to save changes and restart your terminal or IDE to apply.

- Setting JAVA_HOME Permanently in macOS/Linux: (not tested good luck)
  1. Open terminal.
  2. Edit ~/.bashrc or ~/.zshrc file using a text editor (e.g., nano ~/.bashrc).
  3. Add the following lines at the end of the file:
     export JAVA_HOME=/path/to/your/jdk
     export PATH=$JAVA_HOME/bin:$PATH
  4. Save the file and run source ~/.bashrc or source ~/.zshrc to apply changes.

5. Install Docker:

- Windows:
  1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop/
  2. Run the installer and follow the installation wizard.
  3. After installation, restart your computer.
  4. Launch Docker Desktop and complete the initial setup.
  5. Verify installation by opening terminal and running: docker --version

- macOS/Linux:
  1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop/
  2. For macOS: Drag Docker.app to Applications folder and launch it.
  3. For Linux: Follow distribution-specific instructions at https://docs.docker.com/desktop/install/linux-install/
  4. Complete the initial setup when Docker Desktop launches.
  5. Verify installation by opening terminal and running: docker --version

6. Install Python:

Download Python 3.11 or later from: https://www.python.org/downloads/

- Windows:
  1. Run the installer
  2. **Important:** Check "Add Python to PATH" during installation
  3. Click "Install Now"
  4. Verify installation: python --version

- macOS/Linux:
  1. macOS: Install using Homebrew: brew install python@3.11
  2. Linux: Use package manager: sudo apt install python3.11 python3-pip (Ubuntu/Debian)
  3. Verify installation: python3 --version


7. Install Node.js for React/TypeScript with Vite:

Download Node.js LTS from: https://nodejs.org/

- Verify installation: node --version and npm --version

8. Create new Kotlin Maven project:(If you need a new one)

Open VS Code Command Palette (Ctrl+Shift+P)
Type: "Maven: Create Maven Project"

- Select "Create from Archetype"
- Choose "org.jetbrains.kotlin:kotlin-maven-archetype"
- Follow prompts to set Group Id, Artifact Id, Version, Package, and Project Location.

9. If not installed install Kotlin extension by fwcd.
10. Build and run (from VS Code):

- Use Maven sidebar in VS Code
- OR terminal: mvn clean compile (uses VS Code's built-in Maven)

11. Eslint and Prettier setup for React/TypeScript (if needed):
- Install ESLint and Prettier extensions in VS Code.
- Initialize ESLint in your project:
  - npx eslint --init
- Configure Prettier settings in VS Code settings.json:
  ```json
  {
    "editor.formatOnSave": true,
    "eslint.validate": [
      "javascript",
      "javascriptreact",
      "typescript",
      "typescriptreact"
    ]
  }
  ```

12. Install UV (Python package manager and version controller):

- Windows:
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

- macOS/Linux:
  curl -LsSf https://astral.sh/uv/install.sh | sh

- Verify installation: uv --version

13. Code Quality Tools (To explore):

**For Kotlin/Java:**
- Install "SonarLint" extension in VS Code for code quality checks

**For Python:**
- Install Flake8 linter: pip install flake8
- Install "Python" extension by Microsoft (if not already installed)
- Install Black formatter: pip install black
- Add to VS Code settings.json:
  ```json
  {
    "[python]": {
      "editor.defaultFormatter": "ms-python.black-formatter",
      "editor.formatOnSave": true
    }
  }
  ```
  14. Turn on additional features and models in Copilot !