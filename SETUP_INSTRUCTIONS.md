# VirtualDoctor Project Setup Guide


## Setup Instructions
Git command that helped me :
`git config --global credential.helper store`
So git stores your credentialss
### Requirements
- Python 3.11 or higher
- PostgreSQL database (or SQLite)

### Python Dependencies
Install required dependencies:

```bash
pip install kivy matplotlib numpy psycopg2-binary sqlalchemy
```

### Database Setup
Create a `.env` file in the project root with your database connection:

```
DATABASE_URL=sqlite:///virtualdoctor.db
```

### Running the Applications

Console version:
```bash
python main.py
```

Web interface:
```bash
python web_doctor.py
```

Kivy GUI:
```bash
python kivy_doctor.py
```

## Note About Game Progress
Your progress will be saved in the database specified by DATABASE_URL.