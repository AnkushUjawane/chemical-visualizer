# System Architecture

## Architecture Diagram

```mermaid
graph TB
    subgraph "User Interfaces"
        WEB[Web Frontend<br/>React.js + Chart.js]
        DESKTOP[Desktop Frontend<br/>PyQt5 + Matplotlib]
    end
    
    subgraph "Backend API"
        API[Django REST Framework<br/>Port: 8000]
        AUTH[Authentication<br/>Basic Auth]
        LOGIC[Business Logic<br/>CSV Processing<br/>Statistics<br/>PDF Generation]
    end
    
    subgraph "Database"
        DB[(SQLite Database<br/>User<br/>EquipmentDataset<br/>Equipment)]
    end
    
    WEB -->|HTTP/REST<br/>Axios| API
    DESKTOP -->|HTTP/REST<br/>Requests| API
    API --> AUTH
    AUTH --> LOGIC
    LOGIC --> DB
    
    style WEB fill:#61dafb,stroke:#333,stroke-width:2px
    style DESKTOP fill:#41cd52,stroke:#333,stroke-width:2px
    style API fill:#092e20,stroke:#333,stroke-width:2px,color:#fff
    style DB fill:#003b57,stroke:#333,stroke-width:2px,color:#fff
```

## Component Structure

```mermaid
graph LR
    subgraph "Web Components"
        W1[Login]
        W2[Header]
        W3[UploadSection]
        W4[DatasetHistory]
        W5[Charts]
        W6[DatasetDetails]
    end
    
    subgraph "Desktop Components"
        D1[Login]
        D2[Header]
        D3[Upload]
        D4[History]
        D5[Data]
        D6[Chart]
    end
    
    subgraph "Backend API"
        B1[/api/register/]
        B2[/api/login/]
        B3[/api/upload/]
        B4[/api/datasets/]
        B5[/api/datasets/id/]
        B6[/api/datasets/id/pdf/]
    end
    
    W1 & W2 & W3 & W4 & W5 & W6 --> B1 & B2 & B3 & B4 & B5 & B6
    D1 & D2 & D3 & D4 & D5 & D6 --> B1 & B2 & B3 & B4 & B5 & B6
    
    style W1 fill:#e3f2fd,stroke:#1976d2
    style W2 fill:#e3f2fd,stroke:#1976d2
    style W3 fill:#e3f2fd,stroke:#1976d2
    style W4 fill:#e3f2fd,stroke:#1976d2
    style W5 fill:#e3f2fd,stroke:#1976d2
    style W6 fill:#e3f2fd,stroke:#1976d2
    style D1 fill:#e8f5e9,stroke:#388e3c
    style D2 fill:#e8f5e9,stroke:#388e3c
    style D3 fill:#e8f5e9,stroke:#388e3c
    style D4 fill:#e8f5e9,stroke:#388e3c
    style D5 fill:#e8f5e9,stroke:#388e3c
    style D6 fill:#e8f5e9,stroke:#388e3c
```

## Data Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant Pandas
    participant Database
    
    User->>Frontend: Upload CSV
    Frontend->>API: POST /api/upload/
    API->>Pandas: Parse & Analyze CSV
    Pandas->>API: Statistics
    API->>Database: Store Data
    Database->>API: Confirm
    API->>Frontend: Success Response
    Frontend->>User: Show Success
    
    User->>Frontend: View Data
    Frontend->>API: GET /api/datasets/
    API->>Database: Query Data
    Database->>API: Return Data
    API->>Frontend: JSON Response
    Frontend->>User: Display Charts & Tables
```

## Technology Stack

```mermaid
graph TD
    subgraph "Frontend Layer"
        A1[React.js 18.x]
        A2[Chart.js 4.x]
        A3[Axios]
        B1[PyQt5 5.15.10]
        B2[Matplotlib 3.8.2]
        B3[Requests]
    end
    
    subgraph "Backend Layer"
        C1[Django 4.2.7]
        C2[Django REST Framework 3.14.0]
        C3[Pandas 2.1.3]
        C4[ReportLab 4.0.7]
    end
    
    subgraph "Database Layer"
        D1[(SQLite 3.x)]
    end
    
    A1 & A2 & A3 --> C1 & C2
    B1 & B2 & B3 --> C1 & C2
    C1 & C2 --> C3 & C4
    C3 & C4 --> D1
    
    style A1 fill:#61dafb
    style A2 fill:#ff6384
    style B1 fill:#41cd52
    style B2 fill:#11557c
    style C1 fill:#092e20,color:#fff
    style C2 fill:#092e20,color:#fff
    style D1 fill:#003b57,color:#fff
```

## Database Schema

```mermaid
erDiagram
    User ||--o{ EquipmentDataset : owns
    EquipmentDataset ||--o{ Equipment : contains
    
    User {
        int id PK
        string username
        string password
    }
    
    EquipmentDataset {
        int id PK
        int user_id FK
        string filename
        datetime uploaded_at
        int total_count
        float avg_flowrate
        float avg_pressure
        float avg_temperature
        json type_distribution
    }
    
    Equipment {
        int id PK
        int dataset_id FK
        string name
        string type
        float flowrate
        float pressure
        float temperature
    }
```

## Project Structure

```
chemical-visualizer/
├── backend/                    # Django REST API
│   ├── api/                   # Models, Views, Serializers
│   ├── config/                # Settings
│   └── venv/                  # Virtual Environment
│
├── frontend/                   # React Web App
│   └── src/components/        # Modular Components
│       ├── Login/             # Login.js + Login.css
│       ├── Header/            # Header.js + Header.css
│       ├── UploadSection/     # UploadSection.js + .css
│       ├── DatasetHistory/    # DatasetHistory.js + .css
│       ├── Charts/            # Charts.js + Charts.css
│       └── DatasetDetails/    # DatasetDetails.js + .css
│
├── desktop/                    # PyQt5 Desktop App
│   ├── app.py                 # Main Application
│   └── components/            # Modular Components
│       ├── Login/             # login_widget.py (with styling)
│       ├── Header/            # header_widget.py (with styling)
│       ├── Upload/            # upload_widget.py (with styling)
│       ├── History/           # history_widget.py (with styling)
│       ├── Data/              # data_widget.py (with styling)
│       └── Chart/             # chart_widget.py
│
└── sample_equipment_data.csv  # Test Data
```

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/register/` | No | Register new user |
| POST | `/api/login/` | No | Login user |
| POST | `/api/upload/` | Yes | Upload CSV file |
| GET | `/api/datasets/` | Yes | Get last 5 datasets |
| GET | `/api/datasets/<id>/` | Yes | Get dataset details |
| GET | `/api/datasets/<id>/pdf/` | Yes | Download PDF report |

## Key Features

- ✅ **Dual Interface**: Web (React) + Desktop (PyQt5)
- ✅ **Component-Based**: Modular architecture for easy maintenance
- ✅ **CSV Processing**: Pandas for data analysis
- ✅ **Visualizations**: Chart.js (Web) + Matplotlib (Desktop)
- ✅ **Authentication**: Basic HTTP Auth
- ✅ **History Management**: Last 5 datasets per user
- ✅ **PDF Reports**: ReportLab for report generation
- ✅ **Persistent Login**: Desktop app saves credentials