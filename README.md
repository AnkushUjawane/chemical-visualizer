# Chemical Equipment Parameter Visualizer

A hybrid Web + Desktop application for visualizing and analyzing chemical equipment data.

## Tech Stack

- **Frontend (Web)**: React.js + Chart.js
- **Frontend (Desktop)**: PyQt5 + Matplotlib
- **Backend**: Django + Django REST Framework
- **Data Processing**: Pandas
- **Database**: SQLite
- **Reports**: ReportLab (PDF generation)

## Features

- CSV file upload for chemical equipment data
- Data summary and statistics (count, averages, type distribution)
- Interactive visualizations (charts and graphs)
- History management (stores last 5 datasets)
- PDF report generation
- Basic authentication (username/password)
- Dual interface: Web browser and Desktop application

## Project Structure

```
chemical-visualizer/
├── backend/                 # Django backend
│   ├── api/                # API app (models, views, serializers)
│   ├── config/             # Django settings
│   ├── venv/               # Python virtual environment
│   ├── requirements.txt
│   └── manage.py
├── frontend/               # React web app
│   ├── src/
│   │   ├── components/     # Modular components
│   │   │   ├── Login/      # Login.js + Login.css
│   │   │   ├── Header/     # Header.js + Header.css
│   │   │   ├── UploadSection/
│   │   │   ├── DatasetHistory/
│   │   │   ├── Charts/
│   │   │   └── DatasetDetails/
│   │   ├── App.js
│   │   └── App.css
│   ├── public/
│   └── package.json
├── desktop/                # PyQt5 desktop app
│   ├── components/         # Modular components
│   │   ├── Login/          # login_widget.py (with styling)
│   │   ├── Header/         # header_widget.py (with styling)
│   │   ├── Upload/         # upload_widget.py (with styling)
│   │   ├── History/        # history_widget.py (with styling)
│   │   ├── Data/           # data_widget.py (with styling)
│   │   └── Chart/          # chart_widget.py
│   ├── app.py              # Main application
│   └── requirements.txt
├── sample_equipment_data.csv
├── README.md
└── ARCHITECTURE.md
```

## Setup Instructions

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install dependencies (virtual environment already created):
```bash
export PATH="/home/Project/chemical-visualizer/backend/venv/bin:$PATH"
```

3. Run migrations (already done):
```bash
python manage.py migrate
```

4. Start Django server:
```bash
python manage.py runserver
```

Backend will run at: http://localhost:8000

### Web Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies (already done):
```bash
npm install
```

3. Start React development server:
```bash
npm start
```

Web app will run at: http://localhost:3000

### Desktop App Setup

1. Navigate to desktop directory:
```bash
cd desktop
```

2. Install dependencies:
```bash
export PATH="/home/Project/chemical-visualizer/backend/venv/bin:$PATH"
pip install -r requirements.txt
```

3. Run the desktop application:
```bash
export PATH="/home/Project/chemical-visualizer/backend/venv/bin:$PATH"
python app.py
```

## Usage

### First Time Setup

1. Start the backend server (Django)
2. Start either the web frontend OR desktop app
3. Register a new user account
4. Login with your credentials

### Uploading Data

1. Click "Select CSV" or "Choose File"
2. Select a CSV file with the following format:
   - Columns: Equipment_Name, Type, Flowrate, Pressure, Temperature
   - Use the provided `sample_equipment_data.csv` for testing
3. Click "Upload"

### Viewing Data

- **Web App**: Click "View" button in the history table
- **Desktop App**: Click "View" button, then switch to "Data" or "Charts" tabs

### Generating Reports

- **Web App**: Click "PDF" button next to any dataset
- **Desktop App**: (PDF download can be added similarly)

## API Endpoints

- `POST /api/register/` - Register new user
- `POST /api/login/` - Login user
- `POST /api/upload/` - Upload CSV file (requires auth)
- `GET /api/datasets/` - Get last 5 datasets (requires auth)
- `GET /api/datasets/<id>/` - Get specific dataset details (requires auth)
- `GET /api/datasets/<id>/pdf/` - Download PDF report (requires auth)

## Sample Data Format

```csv
Equipment_Name,Type,Flowrate,Pressure,Temperature
Reactor-A1,Reactor,150.5,25.3,180.2
Pump-B2,Pump,200.0,45.0,85.5
Heat Exchanger-C3,Heat Exchanger,175.3,30.5,220.0
```

## Development Notes

- Backend uses Basic Authentication for API security
- CORS is enabled for local development
- SQLite database stores all data
- Last 5 datasets are automatically maintained per user
- Both frontends consume the same REST API
- **Modular Architecture**: Both web and desktop apps use component-based structure
- **Component Styling**: Each component contains its own styling code
- **Persistent Login**: Desktop app saves credentials locally

## Running All Components

Open 3 terminal windows:

**Terminal 1 - Backend:**
```bash
cd backend
export PATH="/home/Project/chemical-visualizer/backend/venv/bin:$PATH"
python manage.py runserver
```

**Terminal 2 - Web Frontend:**
```bash
cd frontend
npm start
```

**Terminal 3 - Desktop App:**
```bash
cd desktop
python app.py
```

## Testing

Use the provided `sample_equipment_data.csv` file to test the upload and visualization features.

## License

MIT
