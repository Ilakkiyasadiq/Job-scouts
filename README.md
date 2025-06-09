🤖 JOB SCOUTS – Automated Resume Screening & Recruitment Assistant
JOB SCOUTS is an intelligent full-stack application designed to automate the resume screening process using cutting-edge NLP and Generative AI models. Built with Django, Flask, Transformers, PyTorch, and SQLite, it efficiently evaluates candidate resumes against customizable criteria and automates communication with qualified candidates — significantly speeding up recruitment workflows and improving hiring accuracy.

🚀 Features
📄 Automated Resume Screening – Uses NLP and AI models to analyze resumes and match candidate skills to job criteria.

✉️ Auto Email Generation – Automatically generates and sends emails to qualified candidates.

⚙️ Customizable Criteria – Recruiters can define or update screening parameters for different job roles.

🕒 Faster Recruitment – Reduces manual resume review effort and accelerates candidate shortlisting.

📊 Recruitment Analytics – Provides insights into candidate pools and screening effectiveness.

💾 Lightweight Storage – Uses SQLite for quick data storage and retrieval during evaluation.

🛠 Tech Stack
Backend	Machine Learning	Database	Frameworks	Others
Django, Flask	Transformers, PyTorch	SQLite	REST APIs	NLP, Gen AI

🎯 Project Objectives
Leverage AI to automate tedious manual resume screening tasks.

Improve recruitment accuracy with advanced NLP evaluation models.

Integrate seamless automated communication to candidates.

Build a scalable, maintainable pipeline using Python frameworks.

📸 Screenshots
Add screenshots or GIFs showing:

Dashboard with screening results

Candidate evaluation details

Email generation interface

Recruitment analytics panel

🧩 How to Run Locally
bash
Copy
Edit
# Clone the repository
git clone https://github.com/your-username/job-scouts.git
cd job-scouts

# Setup virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Setup database and run migrations
python manage.py migrate

# Start backend server (Django + Flask APIs)
python manage.py runserver

# (Optional) Run any additional ML model services if separated

# Access the app at http://localhost:8000
⚙️ Configuration
Configure model parameters and screening criteria in the provided config files.

Customize email templates for candidate communication.

Update database settings if switching from SQLite.

🤝 Contributing
Contributions, bug reports, and feature requests are welcome!
Please submit issues or pull requests via the GitHub repository.

📄 License
This project is licensed under the MIT License.
