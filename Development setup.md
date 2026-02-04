""
This document help you set up a development environment for Kotlin using Visual Studio Code (VS Code), React, python and Maven.
""
1. git setup (if needed):
- Install git from: https://git-scm.com/downloads
- Configure git:
  - git config --global user.name "Your Name"
  - git config --global user.email "your.email@example.com"

2. Install Chocolatey (Windows Package Manager - Optional but Recommended):

**Windows only:**
1. Open PowerShell as Administrator (Right-click PowerShell → Run as Administrator)
2. Run the following command:
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```
3. Close and reopen PowerShell (as Administrator) to verify installation:
   ```powershell
   choco --version
   ```
4. Chocolatey makes it easier to install tools like Maven, Python, Node.js, etc.

**Note:** macOS users use Homebrew (brew), Linux users use their distribution's package manager (apt, dnf, etc.)

3. Install JDK: 
Download JDK (LTS version 21) from: https://adoptium.net/

or Run PowerShell as Administrator: choco install temurin21 -y

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

4. Install Maven (Required for backend development):

**Windows:**
1. Check if Maven is already installed: `mvn --version`
2. If not installed, first install Chocolatey (if you haven't already from step 2):
   - Open PowerShell as Administrator
   - Run:
     ```powershell
     Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
     ```
   - Close and reopen PowerShell as Administrator
   - Verify: `choco --version`
3. Install Maven using Chocolatey:
   ```powershell
   choco install maven -y
   ```
4. Restart VS Code and verify: `mvn --version`

**macOS:**
1. Check if Maven is already installed: `mvn --version`
2. Install using Homebrew (recommended):
   ```bash
   brew install maven
   ```
3. Or download manually:
   - Download from: https://maven.apache.org/download.cgi
   - Extract to `/usr/local/apache-maven`
   - Add to PATH in `~/.zshrc` or `~/.bashrc`:
     ```bash
     export PATH="/usr/local/apache-maven/bin:$PATH"
     ```
   - Apply changes: `source ~/.zshrc` or `source ~/.bashrc`
4. Verify installation: `mvn --version`

**Linux:**
1. Check if Maven is already installed: `mvn --version`
2. Install using package manager:
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install maven -y
   
   # Fedora/RHEL
   sudo dnf install maven -y
   ```
3. Verify installation: `mvn --version`

5. Install VS Code extensions for Java/Maven/Kotlin:

- "Extension Pack for Java" by Microsoft (includes Maven support)
- "Language Support for Java(TM)" by Red Hat for build tool integration
- "Kotlin" extension by fwcd

6. Install Docker:

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

7. Install Python:

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

8. Install VS Code extension for Python:

- "Python" extension by Microsoft

9. Install Node.js for React/TypeScript with Vite:

Download Node.js LTS from: https://nodejs.org/

- Verify installation: node --version and npm --version

10. Install VS Code extensions for JavaScript/TypeScript:

- "ESLint" for JavaScript/TypeScript linting
- "Prettier" for code formatting

11. Install UV (Python package manager and version controller):

- Windows:
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

- macOS/Linux:
  curl -LsSf https://astral.sh/uv/install.sh | sh

- Verify installation: uv --version

12. Create new Kotlin Maven project (if you need a new one):

Open VS Code Command Palette (Ctrl+Shift+P)
Type: "Maven: Create Maven Project"

- Select "Create from Archetype"
- Choose "org.jetbrains.kotlin:kotlin-maven-archetype"
- Follow prompts to set Group Id, Artifact Id, Version, Package, and Project Location.

13. Build and run (from VS Code):

- Use Maven sidebar in VS Code
- OR terminal: mvn clean compile (uses VS Code's built-in Maven)

14. ESLint and Prettier setup for React/TypeScript (if needed):
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

15. Additional Code Quality Tools (optional):

**For Kotlin/Java:**
- Install "SonarLint" extension in VS Code for code quality checks

**For Python:**
- Install Flake8 linter: pip install flake8
- Install Black formatter: pip install black
- Configure in VS Code settings.json:
  ```json
  {
    "[python]": {
      "editor.defaultFormatter": "ms-python.black-formatter",
      "editor.formatOnSave": true
    }
  }
  ```

16. Turn on additional features and models in Copilot !