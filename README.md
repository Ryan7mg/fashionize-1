# Fashionize
Welcome to the Fashionize Django project! This document outlines the steps required to set up and run the project locally on your machine.

## Prerequisites

Before you begin, ensure you have the following installed on your system:
- Python 3.9 or higher
- pip (Python package manager)
- virtualenv (optional but recommended for creating isolated Python environments)

## Setting Up the Project

1. **Clone the Repository**

   First, clone the Fashionize project repository to your local machine using git:

   ```bash
   git clone https://github.com/<your-username>/Fashionize.git
   cd Fashionize
   ```

2. **Create a Virtual Environment** (Optional)

   It's recommended to create a virtual environment to keep dependencies required by the project separate from your global Python environment:

   ### Using `conda`

   - Create a Conda environment:

     ```bash
     conda create --name fashionize python=3.9
     conda activate fashionize
     ```

 

   ```bash
   python -m venv venv
   # Activate the virtual environment
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**

   Install the project dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**

   Apply migrations to set up your database:

   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser** (Optional)

   To access the Django admin interface, create a superuser account:

   ```bash
   python manage.py createsuperuser
   ```

   Follow the prompts to complete the creation of your superuser account.

6. **Run the Development Server**

   Start the Django development server:

   ```bash
   python manage.py runserver
   ```

   You can now access the project at [http://localhost:8000](http://localhost:8000).

## Additional Information

- **Django Admin Site**: Access the Django admin site at [http://localhost:8000/admin](http://localhost:8000/admin) using the superuser credentials you have created.

## Contributing to Fashionize

We appreciate your contributions. To maintain code quality and ease collaboration, please adhere to these guidelines.

### Commit Messages

Effective commit messages are crucial for understanding the history of the project:

- **Format**: `<type>: <short, descriptive message>`
- **Types**:
  - `feat` for new features.
  - `fix` for bug fixes.
  - `docs` for changes to documentation.
  - `style` for formatting, white space, etc.
  - `refactor` for code changes that neither fix a bug nor add a feature.
  - `test` for adding missing tests or correcting existing ones.
  - `chore` for mundane tasks like updating dependencies.
- **Example**: `feat: implement user login`

### Creating Branches

Use descriptive branch names to signify the purpose of the branch:

- **Command**: `git checkout -b [type]/[description]`
 **Naming Convention**:
  - `feat/[feature-name]` for new features, e.g., `feat/user-authentication`
  - `fix/[bug-name]` for bug fixes, e.g., `fix/login-bug`
  - `docs/[change-description]` for documentation updates, e.g., `docs/update-readme`
  - `style/[change-description]` for formatting changes, e.g., `style/header-format`
  - `refactor/[change-description]` for refactoring, e.g., `refactor/closet-ui-enhancement`
  - `test/[test-name]` for adding tests, e.g., `test/user-registration`
  - `chore/[task]` for mundane tasks, e.g., `chore/update-dependencies`


### Workflow

1. Fork the repository and clone it locally.
2. Create a branch for your work following the naming conventions.
3. Make your changes, committing them with clear, descriptive messages.
4. Push your branch to your fork, then open a pull request against the original repository's `main` branch.

detailed steps below
  

1. **Fork the Repository**: Click the "Fork" button on the GitHub repository page.

2. **Clone Your Fork**:
   ```bash
   git clone https://github.com/yourusername/Fashionize.git
   cd Fashionize
   ```

3. **Create a Feature Branch**:
   ```bash
   git checkout -b feat/my-new-feature
   ```

4. **Make Your Changes**: Implement your feature or fix, adhering to the code style guidelines.

5. **Commit Your Changes**:
   Make sure your commit messages are in the correct format:
   ```bash
   git commit -am 'feat: my new feature'
   ```

6. **Push to Your Fork**:
   ```bash
   git push origin feat/my-new-feature
   ```

7. **Open a Pull Request**:
   Go to the original repository on GitHub, and you'll see a prompt to open a pull request. Fill in the pull request template with all required details.

### Pull Request Review

- Once submitted, the team will review your pull request. Engage in any discussions, and make necessary revisions.
- After approval, a maintainer will merge your pull request into the main branch.

Following these guidelines helps everyone to understand changes, streamline the development process, and keep the project organized. 
```

