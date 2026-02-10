# System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER INTERFACES                               │
├─────────────────────────────────┬───────────────────────────────────┤
│                                 │                                   │
│  ┌───────────────────────┐     │     ┌───────────────────────┐   │
│  │   WEB FRONTEND        │     │     │  DESKTOP FRONTEND     │   │
│  │   (React.js)          │     │     │  (PyQt5)              │   │
│  ├───────────────────────┤     │     ├───────────────────────┤   │
│  │ • Login/Register      │     │     │ • Login Window        │   │
│  │ • CSV Upload          │     │     │ • File Dialog         │   │
│  │ • Data Tables         │     │     │ • Tab Interface       │   │
│  │ • Chart.js Charts     │     │     │ • Matplotlib Charts   │   │
│  │ • PDF Download        │     │     │ • PyQt5 Tables        │   │
│  │ • History View        │     │     │ • History View        │   │
│  └───────────┬───────────┘     │     └───────────┬───────────┘   │
│              │                  │                 │               │
│              │ HTTP/REST        │                 │ HTTP/REST     │
│              │ (Axios)          │                 │ (Requests)    │
└──────────────┼──────────────────┴─────────────────┼───────────────┘
               │                                    │
               └────────────────┬───────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      BACKEND API LAYER                               │
│                   (Django REST Framework)                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    API ENDPOINTS                              │  │
│  ├──────────────────────────────────────────────────────────────┤  │
│  │  POST   /api/register/              (No Auth)                │  │
│  │  POST   /api/login/                 (No Auth)                │  │
│  │  POST   /api/upload/                (Basic Auth)             │  │
│  │  GET    /api/datasets/              (Basic Auth)             │  │
│  │  GET    /api/datasets/<id>/         (Basic Auth)             │  │
│  │  GET    /api/datasets/<id>/pdf/     (Basic Auth)             │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                   BUSINESS LOGIC                              │  │
│  ├──────────────────────────────────────────────────────────────┤  │
│  │  • User Authentication (Django Auth)                         │  │
│  │  • CSV Validation & Parsing (Pandas)                         │  │
│  │  • Statistical Calculations                                  │  │
│  │  • Data Serialization (DRF Serializers)                      │  │
│  │  • PDF Generation (ReportLab)                                │  │
│  │  • History Management (Keep Last 5)                          │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       DATA LAYER                                     │
│                      (SQLite Database)                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────┐         ┌────────────────────────┐     │
│  │  EquipmentDataset      │         │     Equipment          │     │
│  ├────────────────────────┤         ├────────────────────────┤     │
│  │ • id (PK)              │◄────────┤ • id (PK)              │     │
│  │ • user_id (FK)         │    1:N  │ • dataset_id (FK)      │     │
│  │ • filename             │         │ • name                 │     │
│  │ • uploaded_at          │         │ • type                 │     │
│  │ • total_count          │         │ • flowrate             │     │
│  │ • avg_flowrate         │         │ • pressure             │     │
│  │ • avg_pressure         │         │ • temperature          │     │
│  │ • avg_temperature      │         └────────────────────────┘     │
│  │ • type_distribution    │                                        │
│  └────────────────────────┘                                        │
│           ▲                                                         │
│           │                                                         │
│           │ 1:N                                                     │
│  ┌────────────────────────┐                                        │
│  │      User (Django)     │                                        │
│  ├────────────────────────┤                                        │
│  │ • id (PK)              │                                        │
│  │ • username             │                                        │
│  │ • password (hashed)    │                                        │
│  └────────────────────────┘                                        │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘


DATA FLOW DIAGRAM
=================

1. CSV UPLOAD FLOW:
   ┌──────┐    ┌─────────┐    ┌─────────┐    ┌──────────┐
   │ User │───▶│ Upload  │───▶│ Pandas  │───▶│ Database │
   └──────┘    │ CSV     │    │ Parse & │    │ Store    │
               └─────────┘    │ Analyze │    └──────────┘
                              └─────────┘

2. VISUALIZATION FLOW:
   ┌──────────┐    ┌─────────┐    ┌──────────┐    ┌────────┐
   │ Database │───▶│ API     │───▶│ Frontend │───▶│ Charts │
   └──────────┘    │ Endpoint│    │ Receives │    │ Render │
                   └─────────┘    │ JSON     │    └────────┘
                                  └──────────┘

3. PDF GENERATION FLOW:
   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────┐
   │ Database │───▶│ ReportLab│───▶│ PDF File │───▶│ User │
   └──────────┘    │ Generate │    │ Download │    └──────┘
                   └──────────┘    └──────────┘


TECHNOLOGY STACK
================

┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                            │
├──────────────────────────┬──────────────────────────────────┤
│ Web (React.js)           │ Desktop (PyQt5)                  │
│ • React.js 18.x          │ • PyQt5 5.15.10                  │
│ • Chart.js 4.x           │ • Matplotlib 3.8.2               │
│ • Axios                  │ • Requests                       │
│ • Component-based        │ • Component-based                │
│   - Login/               │   - Login/                       │
│   - Header/              │   - Header/                      │
│   - UploadSection/       │   - Upload/                      │
│   - DatasetHistory/      │   - History/                     │
│   - Charts/              │   - Data/                        │
│   - DatasetDetails/      │   - Chart/                       │
│ • Each component has     │ • Each component has             │
│   separate CSS file      │   inline styling                 │
└──────────────────────────┴──────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    BACKEND LAYER                             │
├─────────────────────────────────────────────────────────────┤
│ • Django 4.2.7                                              │
│ • Django REST Framework 3.14.0                              │
│ • Pandas 2.1.3                                              │
│ • ReportLab 4.0.7                                           │
│ • django-cors-headers 4.3.1                                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    DATABASE LAYER                            │
├─────────────────────────────────────────────────────────────┤
│ • SQLite 3.x (File-based)                                   │
│ • Django ORM                                                │
└─────────────────────────────────────────────────────────────┘


DEPLOYMENT ARCHITECTURE
=======================

Development:
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ React Dev    │  │ Django Dev   │  │ PyQt5 App    │
│ Server       │  │ Server       │  │ Standalone   │
│ :3000        │  │ :8000        │  │              │
└──────────────┘  └──────────────┘  └──────────────┘

Production:
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Nginx +      │  │ Gunicorn +   │  │ Packaged     │
│ React Build  │  │ Django       │  │ Executable   │
│ :80/443      │  │ :8000        │  │              │
└──────────────┘  └──────────────┘  └──────────────┘
```
