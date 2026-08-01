# 🏥 Health Companion

> **A continuous-care companion that turns healthcare into a smart, ongoing conversation.**

[![React](https://img.shields.io/badge/Frontend-React-blue?logo=react)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Gemini Live](https://img.shields.io/badge/AI-Gemini%20Live-orange?logo=google)](https://deepmind.google/technologies/gemini/)
[![GCP](https://img.shields.io/badge/Cloud-GCP-red?logo=googlecloud)](https://cloud.google.com/)

Health Companion is not just another health app; it is an end-to-end product designed to walk with you every step of the way. It acts as a personal health coach that checks in, understands medical reports, detects risks early, and connects you to the right doctors through natural, human-like voice conversations.

---

## 🌟 What Makes This Different

We built a system that lives where you already are. It integrates seamlessly with **Gmail**, speaks to you like a real person, and generates visually stunning health report PDFs that doctors actually want to read.

Behind the scenes, we utilize a smart, **low-latency voice conversation pipeline** orchestrated through **Google ADK**, **Gemini Live**, and a **Multi-Agent Architecture**. This brings together lab analysis, medical summarization, doctor coordination, and insurance guidance into one seamless ecosystem.

---

## 🚀 Core Features

### 1. 📄 Smart Record Digitization
**The Problem:** Medical reports are usually unstructured images or PDFs, making them useless for tracking trends.
**Our Solution:**
* **Medical OCR:** Custom-trained OCR understands medical terminology.
* **Structured Data:** Converts labs and prescriptions into searchable data (dates, values, reference ranges).
* **Gemini Extraction:** Intelligently extracts diagnoses and doctor notes.

### 2. 📅 Timeline-Based Health View
**The Problem:** Doctors struggle to find context in a mess of PDF files.
**Our Solution:**
* **Chronological Feed:** Auto-organizes visits, tests, and meds by date.
* **Trend Visualization:** Automatic graphing of repeated tests (e.g., HbA1c levels over 2 years).
* **Smart Filters:** Quickly toggle between Labs, Prescriptions, Visits, and Imaging.

### 3. 🚑 Pre-Visit Intelligent Triage
**The Problem:** Patients often visit the wrong department or delay urgent care.
**Our Solution:**
* **Symptom Analysis:** Collects symptoms via voice/chat before the visit.
* **Urgency Scoring:** Assigns severity scores based on vitals and history.
* **Smart Routing:** Directs patients to Emergency, Urgent Care, or Specialists automatically.

### 4. 🆘 Emergency Access Mode
**The Problem:** Critical info is often locked away when a patient is unconscious.
**Our Solution:**
* **Offline QR Code:** A scannable code for paramedics (works without internet).
* **Critical Info Only:** Displays blood type, allergies, and chronic conditions.
* **Privacy First:** Hides detailed history and sensitive notes.

---

## 🗣️ The Voice Conversation Pipeline

We have built a low-latency system that mimics talking to a knowledgeable healthcare professional.

### Multi-Agent Architecture
1.  **Lab Analysis Agent:** Interprets test results and spots abnormalities.
2.  **Medical Summarization Agent:** Condenses complex reports into plain English.
3.  **Doctor Coordination Agent:** Schedules appointments and manages referrals.
4.  **Insurance Guidance Agent:** Recommends plans and explains coverage/costs.

### Example Interactions
> **User:** "Hey, what did my latest blood test show?"
> **Agent:** Pulls up the record, explains results in simple terms, and flags concerning metrics.

> **User:** "I've been having chest pain for two days."
> **Agent:** Triage protocol initiates -> Assesses severity -> Directs to ER if necessary.

---

## 📧 Seamless Integrations

### Gmail Integration
Your health info flows automatically into the system via secure OAuth.
* **Auto-Ingestion:** Scans for emails from LabCorp, Quest, and patient portals.
* **Privacy:** Only health-related emails are processed; everything is encrypted.

### Professional PDF Reports
Generates executive summaries for specialists or travel.
* **Visual Trends:** Charts and graphs for key metrics.
* **Clean Layout:** Color-coded sections for quick scanning by doctors.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | React | Modern, responsive UI, mobile-first design. |
| **Voice** | Gemini Live | Real-time voice processing and medical reasoning. |
| **Backend** | FastAPI | High-performance Python backend. |
| **Orchestration** | Google ADK | Advanced dialogue management & context retention. |
| **Database** | Firebase | Real-time data for patient flow & notifications. |
| **Infrastructure** | GCP | Scalable, HIPAA-compliant cloud architecture. |
| **OCR** | Custom ML Models | Fine-tuned for healthcare documents. |

---

## 🏁 Getting Started

### Prerequisites
* Node.js & npm
* Python 3.9+
* Google Cloud Platform Account (for Gemini/ADK)

### Installation

1.  **Clone the repo**
    ```bash
    git clone [https://github.com/yourusername/health-companion.git](https://github.com/yourusername/health-companion.git)
    cd health-companion
    ```

2.  **Setup Backend**
    ```bash
    cd backend
    pip install -r requirements.txt
    uvicorn main:app --reload
    ```

3.  **Setup Frontend**
    ```bash
    cd frontend
    npm install
    npm start
    ```

---

## 🛡️ Privacy & Security
* **Encryption:** End-to-end encryption for all patient data.
* **Audit Trails:** Logs regarding who accessed emergency data.
* **Control:** Users can disconnect Gmail integration or delete data at any time.

---

## 💡 Why This Matters
Healthcare is broken. Information is scattered. Patients feel lost.
**Health Companion** is proactive, not reactive. It is continuous, not episodic. It is conversational, not transactional.

---

*Built with using Gemini Live and Google ADK.*
