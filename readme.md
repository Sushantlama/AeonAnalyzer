# 🧠 Aeon-RC Passage Reader

> An open-source AI-powered Aeon essay reader for CAT VARC preparation.

This project lets CAT aspirants and critical readers paste Aeon essay URLs and receive clean reading views and Gemini Flash–powered AI breakdowns. Built to simplify dense reading and help analyze tone, argument structure, and genre.

---

## ✨ Features

* 📖 Paste Aeon essay link to auto-fetch title, author, subheading, and main content
* 🧠 One-click AI analysis using Google Gemini 1.5 Flash:

  * Summary
  * Genre and classification
  * Main point, arguments, contrasting views
  * Paragraph-wise breakdown
* 🏼 Clean reader interface with distraction-free view
* 📊 Simple quota tracking for free-tier Gemini usage (50/day)
* 🔍 Responsive layout for desktop and mobile

---

## 📁 Project Structure

```
├── backend
│   ├── main.py               # FastAPI backend server
│   ├── utils.py              # Text cleaning and helper functions
│   └── gemini.py             # Gemini API interaction
├── frontend
│   ├── index.html            # Main HTML interface
│   ├── script.js             # JavaScript to interact with backend
│   └── style.css             # Styling
├── requirements.txt          # Python dependencies
├── .env                      # API keys and config (not committed)
├── README.md                 # Project documentation
└── render.yaml               # (Optional) Render deployment config
```

---

## 👥 Contributions

Pull requests are welcome. Please:

* Follow PEP8 for Python
* Keep frontend files under `/frontend`
* Document any new API routes

---

## 🙏 Credits

* [Aeon.co](https://aeon.co/) – for the rich, high-quality essays
* [Google Gemini API](https://ai.google.dev/) – AI content analysis
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) – for web scraping

---

## ⚖️ Ethical Use

* This app is meant **strictly for personal academic use**
* Do **not** scrape, republish, or store Aeon content beyond personal device
* Gemini API usage is limited to **free quota**, so use responsibly

---

## 🎯 Purpose

Aeon essays are ideal for CAT VARC prep — but their density can intimidate many readers.
This project aims to:

* Offer a simple interface to parse and interact with Aeon essays
* Provide AI-powered breakdowns for improved comprehension
* Help CAT aspirants build stamina, reading speed, and interpretative skills

---

Built with ❤️ for serious learners.
