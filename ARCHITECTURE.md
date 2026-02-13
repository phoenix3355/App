# System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    INSTRUMENT MANAGEMENT SYSTEM                      │
│                         (Desktop Application)                        │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE LAYER                        │
│                             (PyQt6 Views)                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────┐    ┌──────────────────────────────────────────┐  │
│  │              │    │         Main Window (Tabbed)             │  │
│  │   Login      │───>├──────────────────────────────────────────┤  │
│  │   Window     │    │ ┌──────────┬──────────┬──────────┬─────┐│  │
│  │              │    │ │Instrument│Calibration│Inventory│Report││  │
│  │ ┌──────────┐ │    │ │   View   │   View    │   View  │View ││  │
│  │ │ Username │ │    │ └──────────┴──────────┴──────────┴─────┘│  │
│  │ │ Password │ │    │                                          │  │
│  │ └──────────┘ │    │  - CRUD Operations                       │  │
│  │   [Login]    │    │  - Search & Filter                       │  │
│  └──────────────┘    │  - Data Entry Forms                      │  │
│                      │  - Report Generation                      │  │
│                      └──────────────────────────────────────────┘  │
│                                                                       │
└───────────────────────────────┬───────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       CONTROLLER LAYER                               │
│                       (Business Logic)                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │     User     │  │  Instrument  │  │ Calibration  │              │
│  │  Controller  │  │  Controller  │  │  Controller  │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐                                 │
│  │  Inventory   │  │    Report    │                                 │
│  │  Controller  │  │  Controller  │                                 │
│  └──────────────┘  └──────────────┘                                 │
│                                                                       │
│  Functions:                                                           │
│  - Data validation                                                    │
│  - Business rules enforcement                                         │
│  - CRUD operations orchestration                                      │
│  - Transaction management                                             │
│                                                                       │
└───────────────────────────────┬───────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         MODEL LAYER                                  │
│                    (SQLAlchemy ORM Models)                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │     User     │  │  Instrument  │  │ Calibration  │              │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤              │
│  │ id           │  │ id           │  │ id           │              │
│  │ username     │  │ serial_number│  │ instrument_id│              │
│  │ email        │  │ name         │  │ cal_date     │              │
│  │ password_hash│  │ type         │  │ next_due     │              │
│  │ is_admin     │  │ manufacturer │  │ status       │              │
│  └──────────────┘  │ location     │  │ certificate  │              │
│                    │ status       │  └──────────────┘              │
│  ┌──────────────┐  └──────────────┘                                 │
│  │  Inventory   │                                                    │
│  ├──────────────┤         Relationships:                             │
│  │ id           │         - User ← Admin                             │
│  │ instrument_id│         - Instrument → Calibrations                │
│  │ status       │         - Instrument → Inventory                   │
│  │ location     │         - Foreign Keys with CASCADE                │
│  │ assigned_to  │                                                    │
│  └──────────────┘                                                    │
│                                                                       │
└───────────────────────────────┬───────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        DATABASE LAYER                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌───────────────────────────────────────────────────────────┐      │
│  │            SQLAlchemy Engine & Session                     │      │
│  │                                                             │      │
│  │  - Connection pooling                                      │      │
│  │  - Transaction management                                  │      │
│  │  - Query optimization                                      │      │
│  │  - Automatic schema creation                               │      │
│  └───────────────────────────────────────────────────────────┘      │
│                                                                       │
│  Supported Databases:                                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │  SQLite  │  │PostgreSQL│  │  MySQL   │  │SQL Server│           │
│  │ (default)│  │          │  │          │  │          │           │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────┐
│                        SUPPORTING SYSTEMS                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────────┐    ┌─────────────────────┐                │
│  │   Configuration     │    │     Security        │                │
│  │   System            │    │     System          │                │
│  ├─────────────────────┤    ├─────────────────────┤                │
│  │ - .env files        │    │ - bcrypt hashing    │                │
│  │ - Laravel-style     │    │ - Input validation  │                │
│  │ - Dot notation      │    │ - Sanitization      │                │
│  │ - Runtime config    │    │ - Authentication    │                │
│  └─────────────────────┘    └─────────────────────┘                │
│                                                                       │
│  ┌─────────────────────┐    ┌─────────────────────┐                │
│  │   Report Engine     │    │     Utilities       │                │
│  │   (Jinja2)          │    │                     │                │
│  ├─────────────────────┤    ├─────────────────────┤                │
│  │ - HTML templates    │    │ - Helper functions  │                │
│  │ - Report generation │    │ - Validators        │                │
│  │ - Styling           │    │ - Error handlers    │                │
│  │ - Export functions  │    │ - Date utilities    │                │
│  └─────────────────────┘    └─────────────────────┘                │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘


DATA FLOW EXAMPLE - Adding an Instrument
═══════════════════════════════════════════

1. USER ACTION
   └─> Clicks "Add Instrument" button in InstrumentView

2. VIEW LAYER
   └─> Opens InstrumentDialog
   └─> User fills form
   └─> Clicks "Save"
   └─> Validates required fields

3. CONTROLLER LAYER
   └─> InstrumentController.create_instrument() called
   └─> Sanitizes input (Security)
   └─> Checks for duplicate serial number
   └─> Creates Instrument model instance

4. MODEL LAYER
   └─> Instrument object created with attributes
   └─> SQLAlchemy prepares INSERT statement

5. DATABASE LAYER
   └─> Transaction begins
   └─> INSERT INTO instruments (...) VALUES (...)
   └─> Transaction commits
   └─> Returns new instrument with ID

6. RETURN PATH
   └─> Controller returns instrument object
   └─> View refreshes table
   └─> User sees new instrument in list
   └─> Success message displayed


SECURITY FLOW
═══════════════

Login Request
   │
   ├─> Username/Password entered
   │
   ├─> Security.authenticate_user()
   │   │
   │   ├─> Validate format
   │   ├─> Query user from database
   │   ├─> Check if account is active
   │   ├─> Verify password with bcrypt
   │   └─> Update last_login timestamp
   │
   ├─> Return User object or raise AuthenticationError
   │
   └─> Open main application window


REPORT GENERATION FLOW
═════════════════════════

User Request
   │
   ├─> Select report type
   ├─> Set filters (optional)
   └─> Click "Generate Report"
       │
       ├─> ReportController queries database
       ├─> Retrieves relevant data
       ├─> Loads Jinja2 template
       ├─> Renders HTML with data
       ├─> Returns HTML string
       │
       ├─> Preview in QTextBrowser
       │
       └─> "Save Report" → Write to file
           └─> Open in browser (optional)


CONFIGURATION SYSTEM
═══════════════════════

.env file
   │
   ├─> Loaded by python-dotenv
   │
   ├─> Config class singleton
   │   │
   │   ├─> app: Application settings
   │   ├─> database: DB connection
   │   ├─> security: Auth settings
   │   └─> custom: Extended config
   │
   └─> Accessed via config.get('key.subkey')
       Example: config.get('database.url')


KEY FEATURES SUMMARY
════════════════════

✓ MVC Architecture - Clean separation of concerns
✓ PyQt6 UI - Modern cross-platform interface
✓ SQLAlchemy ORM - Database abstraction
✓ Jinja2 Templates - Professional reports
✓ bcrypt Security - Password protection
✓ Input Validation - Data integrity
✓ Session Management - Proper cleanup
✓ Extensible Design - Easy to add features
✓ Comprehensive Docs - 39,000+ words
✓ Production Ready - Tested and verified
```
