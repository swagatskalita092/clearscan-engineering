"""Invented resume content. Every person, employer and school is fictional."""

P1 = {
    "name": "Jordan Ellis",
    "title": "Operations Analyst",
    "city": "Riverton",
    "email": "jordan.ellis@example.com",
    "phone": "+00 555 010 2030",
    "link_label": "LinkedIn",
    "link_url": "https://www.example.com/in/jordan-ellis",
    "summary": (
        "Operations analyst with six years of experience improving delivery "
        "schedules and inventory accuracy for regional distributors."
    ),
    "experience": [
        {
            "role": "Senior Analyst",
            "org": "Harbor and Pine Logistics",
            "dates": "2022 - Present",
            "bullets": [
                "Built a weekly dashboard that reduced late deliveries by tracking route delays",
                "Standardised stock counts across four warehouses and improved financial reporting",
                "Trained eight colleagues and documented the team workflow",
            ],
        },
        {
            "role": "Analyst",
            "org": "Linden Supply Company",
            "dates": "2019 - 2022",
            "bullets": [
                "Automated monthly purchase reports for the finance office",
                "Reconciled supplier invoices and resolved discrepancies",
            ],
        },
    ],
    "education": [
        {
            "degree": "B.Sc. Business Information Systems",
            "school": "Riverton University",
            "dates": "2015 - 2019",
        }
    ],
    "skills": [
        "SQL", "Python", "Excel",
        "Forecasting", "Process mapping", "Data validation",
        "Documentation", "Scheduling", "Stakeholder communication",
    ],
}

P2 = {
    "name": "Renée Ødegård",
    "title": "Clinical Coordinator",
    "city": "Málaga",
    "email": "renee.odegard@example.com",
    "phone": "+00 555 010 4455",
    "link_label": "LinkedIn",
    "link_url": "https://www.example.com/in/renee-odegard",
    "summary": (
        "Clinical coordinator with seven years of experience organising patient "
        "schedules and records in busy outpatient departments."
    ),
    "experience": [
        {
            "role": "Clinical Coordinator",
            "org": "Clínica Sønderby",
            "dates": "2021 - Present",
            "bullets": [
                "Coordinated appointments for five departments and reduced waiting times",
                "Introduced a shared checklist for patient records and audits",
                "Mentored four new coordinators",
            ],
        },
        {
            "role": "Administrator",
            "org": "Hôpital Saint-Étienne",
            "dates": "2018 - 2021",
            "bullets": [
                "Maintained patient records in line with local regulations",
                "Prepared monthly reports for the department head",
            ],
        },
    ],
    "education": [
        {
            "degree": "B.A. Health Administration",
            "school": "Universidad de Málaga",
            "dates": "2014 - 2018",
        }
    ],
    "skills": [
        "Scheduling", "Patient records", "Quality audits",
        "Mentoring", "Documentation", "Triage support",
        "Spanish", "Norwegian", "English",
    ],
}


def contact_line(p):
    return " | ".join([p["city"], p["email"], p["phone"], p["link_label"]])
