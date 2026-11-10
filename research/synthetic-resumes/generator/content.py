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


DEFAULT_HEADINGS = {
    "summary": "Summary", "experience": "Experience",
    "education": "Education", "skills": "Skills",
}

P1["headings"] = DEFAULT_HEADINGS
P2["headings"] = DEFAULT_HEADINGS

# A German-language CV: second-language headings, month/year dates, umlauts.
P3 = {
    "name": "Mara Lindner",
    "title": "Operations Analystin",
    "city": "Flussburg",
    "email": "mara.lindner@example.com",
    "phone": "+00 555 010 7788",
    "link_label": "LinkedIn",
    "link_url": "https://www.example.com/in/mara-lindner",
    "ocr_lang": "deu",
    "headings": {"summary": "Profil", "experience": "Berufserfahrung",
                 "education": "Ausbildung", "skills": "Kenntnisse"},
    "summary": (
        "Operations Analystin mit sechs Jahren Erfahrung in der Verbesserung "
        "von Lieferpl\u00e4nen und Bestandsgenauigkeit bei regionalen "
        "Distributoren."
    ),
    "experience": [
        {"role": "Senior Analystin", "org": "Nordhafen Logistik GmbH",
         "dates": "03/2022 - heute",
         "bullets": [
             "W\u00f6chentliches Dashboard zur Verfolgung von Lieferverz\u00f6gerungen aufgebaut",
             "Bestandsz\u00e4hlungen in vier Lagern vereinheitlicht und das Finanzreporting verbessert",
             "Acht Kolleginnen und Kollegen geschult und den Teamablauf dokumentiert",
         ]},
        {"role": "Analystin", "org": "Lindenau Handels AG",
         "dates": "09/2019 - 02/2022",
         "bullets": [
             "Monatliche Einkaufsberichte f\u00fcr die Finanzabteilung automatisiert",
             "Lieferantenrechnungen abgeglichen und Abweichungen gekl\u00e4rt",
         ]},
    ],
    "education": [{"degree": "B.Sc. Wirtschaftsinformatik",
                   "school": "Universit\u00e4t Flussburg",
                   "dates": "10/2015 - 09/2019"}],
    "skills": ["SQL", "Python", "Excel", "Prognose", "Prozessmodellierung",
               "Datenpr\u00fcfung", "Dokumentation", "Terminplanung",
               "Stakeholder-Kommunikation"],
}

# Cyrillic
P4 = {
    "name": "Ольга Ветрова",
    "title": "Аналитик по операциям",
    "city": "Новоград",
    "email": "olga.vetrova@example.com",
    "phone": "+00 555 010 3344",
    "link_label": "LinkedIn",
    "link_url": "https://www.example.com/in/olga-vetrova",
    "ocr_lang": "rus",
    "headings": {"summary": "Профиль", "experience": "Опыт работы",
                 "education": "Образование", "skills": "Навыки"},
    "summary": ("Аналитик по операциям с шестилетним опытом оптимизации "
                "графиков доставки и точности учёта запасов у региональных "
                "дистрибьюторов."),
    "experience": [
        {"role": "Старший аналитик", "org": "Северная гавань",
         "dates": "2022 - наст. время",
         "bullets": [
             "Создала еженедельную панель, снизившую число опозданий доставки",
             "Унифицировала учёт запасов на четырёх складах и улучшила отчётность",
             "Обучила восемь коллег и описала рабочий процесс команды",
         ]},
        {"role": "Аналитик", "org": "Липа Снабжение",
         "dates": "2019 - 2022",
         "bullets": [
             "Автоматизировала ежемесячные отчёты по закупкам для финансового отдела",
             "Сверяла счета поставщиков и устраняла расхождения",
         ]},
    ],
    "education": [{"degree": "Бакалавр, бизнес-информатика",
                   "school": "Университет Новограда",
                   "dates": "2015 - 2019"}],
    "skills": ["SQL", "Python", "Excel", "Прогнозирование",
               "Картирование процессов", "Проверка данных",
               "Документирование", "Планирование", "Коммуникация с заказчиками"],
}

# Greek
P5 = {
    "name": "Ελένη Βασιλείου",
    "title": "Αναλύτρια Λειτουργιών",
    "city": "Νέα Πόλη",
    "email": "eleni.vasileiou@example.com",
    "phone": "+00 555 010 5566",
    "link_label": "LinkedIn",
    "link_url": "https://www.example.com/in/eleni-vasileiou",
    "ocr_lang": "ell",
    "headings": {"summary": "Προφίλ", "experience": "Εμπειρία",
                 "education": "Εκπαίδευση", "skills": "Δεξιότητες"},
    "summary": ("Αναλύτρια λειτουργιών με έξι χρόνια εμπειρίας στη βελτίωση "
                "προγραμμάτων παράδοσης και της ακρίβειας αποθεμάτων σε "
                "περιφερειακούς διανομείς."),
    "experience": [
        {"role": "Ανώτερη Αναλύτρια", "org": "Βόρειο Λιμάνι Μεταφορές",
         "dates": "2022 - Σήμερα",
         "bullets": [
             "Δημιούργησε εβδομαδιαίο πίνακα ελέγχου που μείωσε τις καθυστερήσεις παραδόσεων",
             "Τυποποίησε την καταμέτρηση αποθεμάτων σε τέσσερις αποθήκες",
             "Εκπαίδευσε οκτώ συναδέλφους και τεκμηρίωσε τη ροή εργασίας της ομάδας",
         ]},
        {"role": "Αναλύτρια", "org": "Φλαμουριά Προμήθειες",
         "dates": "2019 - 2022",
         "bullets": [
             "Αυτοματοποίησε μηνιαίες αναφορές αγορών για το οικονομικό τμήμα",
             "Συμφιλίωσε τιμολόγια προμηθευτών και έλυσε αποκλίσεις",
         ]},
    ],
    "education": [{"degree": "Πτυχίο Επιχειρησιακών Πληροφοριακών Συστημάτων",
                   "school": "Πανεπιστήμιο Νέας Πόλης",
                   "dates": "2015 - 2019"}],
    "skills": ["SQL", "Python", "Excel", "Πρόβλεψη", "Χαρτογράφηση διαδικασιών",
               "Επικύρωση δεδομένων", "Τεκμηρίωση", "Προγραμματισμός",
               "Επικοινωνία με ενδιαφερόμενους"],
}

# Japanese (CJK, no spaces between words)
P6 = {
    "name": "佐藤 花子",
    "title": "オペレーションアナリスト",
    "city": "桜ヶ丘",
    "email": "hanako.sato@example.com",
    "phone": "+00 555 010 7799",
    "link_label": "LinkedIn",
    "link_url": "https://www.example.com/in/hanako-sato",
    "ocr_lang": "jpn",
    "skill_sep": "、 ",
    "headings": {"summary": "概要", "experience": "職務経歴",
                 "education": "学歴", "skills": "スキル"},
    "summary": "地域の物流会社で配送計画と在庫精度の改善に6年間取り組んだオペレーションアナリスト。",
    "experience": [
        {"role": "シニアアナリスト", "org": "北港ロジスティクス株式会社",
         "dates": "2022年 - 現在",
         "bullets": [
             "配送遅延を追跡する週次ダッシュボードを構築し、遅延を削減",
             "4拠点の倉庫で棚卸方法を標準化し、財務報告を改善",
             "同僚8名を指導し、チームの業務手順を文書化",
         ]},
        {"role": "アナリスト", "org": "リンデン商事株式会社",
         "dates": "2019年 - 2022年",
         "bullets": [
             "財務部門向けの月次購買レポートを自動化",
             "仕入先の請求書を照合し、差異を解消",
         ]},
    ],
    "education": [{"degree": "経営情報学 学士", "school": "桜ヶ丘大学",
                   "dates": "2015年 - 2019年"}],
    "skills": ["SQL", "Python", "Excel", "需要予測", "業務プロセスの整理",
               "データ検証", "ドキュメント作成", "スケジュール管理",
               "関係者との調整"],
}


# ---- Scripts that need text shaping. Built through a word processor, because
# the plain PDF writer used for the other files cannot shape them.
P7 = {
    "name": "ليلى حداد",
    "title": "محللة عمليات",
    "city": "المرفأ",
    "email": "layla.haddad@example.com",
    "phone": "+00 555 010 8811",
    "link_label": "LinkedIn",
    "link_url": "https://www.example.com/in/layla-haddad",
    "ocr_lang": "ara",
    "rtl": True,
    "font": "DejaVu Sans",
    "lang": "ar-SA",
    "skill_sep": "، ",
    "headings": {"summary": "الملخص", "experience": "الخبرة",
                 "education": "التعليم", "skills": "المهارات"},
    "summary": ("محللة عمليات لديها ست سنوات من الخبرة في تحسين جداول التسليم "
                "ودقة المخزون لدى موزعين إقليميين."),
    "experience": [
        {"role": "محللة أولى", "org": "شركة ميناء الصنوبر للخدمات اللوجستية",
         "dates": "2022 - الآن",
         "bullets": [
             "بناء لوحة متابعة أسبوعية قللت تأخر التسليم عبر تتبع تأخر المسارات",
             "توحيد جرد المخزون في أربعة مستودعات وتحسين التقارير المالية",
             "تدريب ثمانية زملاء وتوثيق سير عمل الفريق",
         ]},
        {"role": "محللة", "org": "شركة الزيزفون للتوريد",
         "dates": "2019 - 2022",
         "bullets": [
             "أتمتة تقارير المشتريات الشهرية لقسم المالية",
             "مطابقة فواتير الموردين وحل الفروقات",
         ]},
    ],
    "education": [{"degree": "بكالوريوس نظم المعلومات الإدارية",
                   "school": "جامعة المرفأ", "dates": "2015 - 2019"}],
    "skills": ["SQL", "Python", "Excel", "التنبؤ", "تخطيط العمليات",
               "التحقق من البيانات", "التوثيق", "الجدولة",
               "التواصل مع أصحاب المصلحة"],
}

P8 = {
    "name": "अनन्या वर्मा",
    "title": "ऑपरेशंस विश्लेषक",
    "city": "नदीपुर",
    "email": "ananya.verma@example.com",
    "phone": "+00 555 010 9922",
    "link_label": "LinkedIn",
    "link_url": "https://www.example.com/in/ananya-verma",
    "ocr_lang": "hin",
    "font": "FreeSans",
    "lang": "hi-IN",
    "headings": {"summary": "सारांश", "experience": "अनुभव",
                 "education": "शिक्षा", "skills": "कौशल"},
    "summary": ("ऑपरेशंस विश्लेषक, जिन्हें क्षेत्रीय वितरकों के लिए डिलीवरी "
                "शेड्यूल और इन्वेंट्री की सटीकता सुधारने का छह वर्षों का अनुभव है।"),
    "experience": [
        {"role": "वरिष्ठ विश्लेषक", "org": "हार्बर एंड पाइन लॉजिस्टिक्स",
         "dates": "2022 - वर्तमान",
         "bullets": [
             "मार्ग में देरी को ट्रैक करने वाला साप्ताहिक डैशबोर्ड बनाया, जिससे देरी से होने वाली डिलीवरी घटी",
             "चार गोदामों में स्टॉक गणना को मानकीकृत किया और वित्तीय रिपोर्टिंग बेहतर की",
             "आठ सहकर्मियों को प्रशिक्षित किया और टीम की कार्यप्रणाली दस्तावेज़ित की",
         ]},
        {"role": "विश्लेषक", "org": "लिंडेन सप्लाई कंपनी",
         "dates": "2019 - 2022",
         "bullets": [
             "वित्त कार्यालय के लिए मासिक खरीद रिपोर्ट स्वचालित कीं",
             "आपूर्तिकर्ता चालानों का मिलान किया और विसंगतियाँ सुलझाईं",
         ]},
    ],
    "education": [{"degree": "बी.एससी. व्यावसायिक सूचना प्रणाली",
                   "school": "नदीपुर विश्वविद्यालय", "dates": "2015 - 2019"}],
    "skills": ["SQL", "Python", "Excel", "पूर्वानुमान", "प्रक्रिया मानचित्रण",
               "डेटा सत्यापन", "दस्तावेज़ीकरण", "शेड्यूलिंग", "हितधारक संचार"],
}

P9 = {
    "name": "นภา วงศ์สว่าง",
    "title": "นักวิเคราะห์การปฏิบัติการ",
    "city": "ท่าเรือใหม่",
    "email": "napa.wongsawang@example.com",
    "phone": "+00 555 010 3344",
    "link_label": "LinkedIn",
    "link_url": "https://www.example.com/in/napa-wongsawang",
    "ocr_lang": "tha",
    "font": "Loma",
    "lang": "th-TH",
    "headings": {"summary": "สรุป", "experience": "ประสบการณ์",
                 "education": "การศึกษา", "skills": "ทักษะ"},
    "summary": ("นักวิเคราะห์การปฏิบัติการที่มีประสบการณ์หกปีในการปรับปรุงตาราง"
                "การจัดส่งและความแม่นยำของสินค้าคงคลังให้ผู้จัดจำหน่ายในภูมิภาค"),
    "experience": [
        {"role": "นักวิเคราะห์อาวุโส", "org": "บริษัท ฮาร์เบอร์แอนด์ไพน์ โลจิสติกส์ จำกัด",
         "dates": "2565 - ปัจจุบัน",
         "bullets": [
             "สร้างแดชบอร์ดรายสัปดาห์เพื่อติดตามความล่าช้าของเส้นทางและลดการส่งมอบล่าช้า",
             "ปรับมาตรฐานการนับสต็อกในคลังสินค้าสี่แห่งและปรับปรุงรายงานทางการเงิน",
             "ฝึกอบรมเพื่อนร่วมงานแปดคนและจัดทำเอกสารขั้นตอนการทำงานของทีม",
         ]},
        {"role": "นักวิเคราะห์", "org": "บริษัท ลินเดน ซัพพลาย จำกัด",
         "dates": "2562 - 2565",
         "bullets": [
             "ทำรายงานการจัดซื้อรายเดือนให้ฝ่ายการเงินโดยอัตโนมัติ",
             "กระทบยอดใบแจ้งหนี้ของผู้จัดหาสินค้าและแก้ไขความคลาดเคลื่อน",
         ]},
    ],
    "education": [{"degree": "ปริญญาตรี สาขาระบบสารสนเทศทางธุรกิจ",
                   "school": "มหาวิทยาลัยท่าเรือใหม่", "dates": "2558 - 2562"}],
    "skills": ["SQL", "Python", "Excel", "การพยากรณ์", "การทำแผนผังกระบวนการ",
               "การตรวจสอบข้อมูล", "การจัดทำเอกสาร", "การจัดตารางงาน",
               "การสื่อสารกับผู้มีส่วนได้ส่วนเสีย"],
}
