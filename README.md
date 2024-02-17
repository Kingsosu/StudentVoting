# eVoting System for College Students

## Overview

This project is an electronic voting (eVoting) system designed specifically for college or university students. It provides a convenient platform for students to participate in the Student Union Government (SUG) elections by casting their votes for their preferred candidates. The system ensures transparency, efficiency, and security in the election process, allowing students to exercise their democratic rights easily and securely.

## Key Features

1. **User Authentication**: Students can register and login securely to access the eVoting platform. Passwords are securely hashed and stored in the database. Forgot password functionality allows users to reset their passwords via email.

2. **Candidate Registration**: Candidates can register for positions in the Student Union Government by providing necessary details and a passcode. Only students with a level of 400 or above are eligible to register as candidates.

3. **Voting Process**: Registered students can vote for their preferred candidates during the election period. The system ensures that each student can vote only once and that votes are securely recorded and counted.

4. **Real-time Updates**: Students can log in, register, vote, and view real-time updates on the progress of the election, including the number of votes cast and the remaining time until the end of the voting period.

5. **Profile Management**: Users can update their profile information, including uploading a profile image, to personalize their accounts.

6. **Result Viewing**: After the election, students can view the election results and see the winners for each position.

7. **Countdown Timer**: A countdown timer is displayed to inform students about the remaining time until the end of the voting period, promoting participation and engagement.

## Technologies Used

- **Django Framework**: The backend of the eVoting system is built using Django, a high-level Python web framework, for rapid development and clean, pragmatic design.

- **HTML/CSS/JavaScript**: Frontend components are developed using HTML, CSS, and JavaScript to create an intuitive and user-friendly interface.

- **Bootstrap Framework**: Bootstrap is utilized for frontend design and responsiveness, ensuring compatibility with various devices and screen sizes.

- **PostgresSQL Database**: PostgresSQL is used as the default database engine for storing user accounts, candidate information, student information, and voting records.

- **SMTP Protocol**: The system integrates with SMTP servers to handle email functionalities such as password reset requests.

## Usage

1. **User Registration and Login**: New users can register for an account using their matriculation number. After registration, they can log in to access the eVoting platform.

2. **Candidate Registration**: Eligible students can register as candidates for various positions in the Student Union Government by providing required information and a passcode.

3. **Voting**: Registered students can vote for their preferred candidates during the designated voting period. Each student can cast only one vote per position.

4. **Profile Management**: Users can update their profile information, including profile images, to personalize their accounts.

5. **Result Viewing**: After the election, students can view the election results to see the winners for each position.

6. **Password Reset**: In case of forgotten passwords, users can request a password reset via email to regain access to their accounts.

## Getting Started

To get started with the eVoting system for college students, follow these steps:

1. **Clone the Repository**: Clone the project repository to your local machine using Git:

    ```bash
    git clone https://github.com/your-username/StudentVoting.git
    ```

2. **Set up your virtual environment:**

    ```bash
    virtualenv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Dependencies**: Navigate to the project directory and install the required dependencies using pip:

    ```bash
    cd votesystem
    pip install -r requirements.txt
    ```

4. **Database Setup**: Migrate the database schema and create a superuser account:

    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    ```

5. **Run the Development Server**: Start the Django development server to run the eVoting system locally:

    ```bash
    python manage.py runserver
    ```

6. **Access the Application**: Open your web browser and navigate to [http://localhost:8000](http://localhost:8000) to access the eVoting system. You can log in with the superuser account created in step 4 or register a new account as a student user.

7. **Explore Features**: Explore the various features of the eVoting system, including user registration, candidate registration, voting, profile management, result viewing, and more.

8. **Customize as Needed**: Modify the codebase according to your requirements or contribute to the project by adding new features, fixing bugs, or improving existing functionality.

## Environment Variables

Before running the eVoting system, make sure to set up the following environment variables:

- **SECRET_KEY**: Django requires a secret key to securely manage sessions, passwords, and other cryptographic functions. Generate a random secret key and set it as the value for this variable.

- **EMAIL_HOST**: Specify the SMTP server host for sending email notifications, such as password reset emails. Consult your email service provider for the appropriate host address.

- **EMAIL_PORT**: Specify the SMTP server port for sending email notifications. The default port for SMTP is 587.

- **EMAIL_HOST_USER**: Provide the email address or username for authenticating with the SMTP server.

- **EMAIL_HOST_PASSWORD**: Provide the password for authenticating with the SMTP server.

Ensure that you securely manage these environment variables and do not expose them in version control or publicly accessible locations.


By following these steps, you can set up and start using the eVoting system for college students on your local machine. Enjoy voting and participating in campus elections with ease and convenience!

## Conclusion

The eVoting system for college students provides a secure, efficient, and transparent platform for conducting Student Union Government elections. By leveraging modern web technologies, it offers a user-friendly experience while ensuring the integrity and fairness of the electoral process. With features such as real-time updates, profile management, and result viewing, the system aims to promote student engagement and participation in campus governance.
