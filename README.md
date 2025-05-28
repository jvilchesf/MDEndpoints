# MDEndpoints

A comprehensive endpoint data management system for Microsoft Defender for Endpoint (MDE) data collection and processing.

## Overview

This project provides a robust solution for collecting, processing, and storing Microsoft Defender for Endpoint data across multiple endpoints. It includes automated data collection, database management, and API services for endpoint security data.

## Project Structure

```
MDEndpoints/
├── services/
│   └── get_data/
│       └── src/
│           ├── config.py          # Endpoint configurations and database settings
│           ├── main.py            # Main application entry point
│           ├── api.py             # API client for MDE data collection
│           ├── database.py        # Database connection and operations
│           ├── process_data.py    # Data processing and transformation
│           └── settings.env       # Environment configuration
├── scripts/                       # Database and utility scripts
├── deployments/                   # Deployment configurations
├── docker/                        # Docker configurations
├── pyproject.toml                # Python project configuration
├── uv.lock                       # Dependency lock file
└── Makefile                      # Build and deployment commands
```

## Features

### Endpoint Data Collection
- **28 Different Endpoints**: Comprehensive coverage of MDE API endpoints
- **Automated Data Retrieval**: Scheduled data collection from Microsoft Defender APIs
- **Batch Processing**: Efficient handling of large datasets with configurable batch sizes
- **Error Handling**: Robust error handling and retry mechanisms

### Database Management
- **SQL Server Integration**: Native support for Microsoft SQL Server
- **Table Management**: Automated table creation and schema management
- **Data Deduplication**: Built-in deduplication based on unique keys
- **Execution Logging**: Comprehensive logging of all data collection operations

### Supported Endpoints

The system collects data from the following MDE endpoints:

| Category | Endpoints |
|----------|-----------|
| **Vulnerabilities** | Vulnerabilities, Vulnerabilities by Machine, Software Vulnerabilities by Machine |
| **Machines** | Machines, Device AV Info, Machine Actions |
| **Security Assessment** | Secure Config Assessment, Baseline Compliance Assessment, Certificate Assessments |
| **Software Management** | Software Inventory, Non-Product Software Inventory, Software |
| **Threat Detection** | Alerts, Investigations, Indicators |
| **Scanning** | Device Authenticated Scan Definitions, Device Authenticated Scan Agents |
| **Browser Security** | Browser Extensions Inventory, Browser Extensions Permissions |
| **Remediation** | Remediation Tasks |
| **Scoring** | Exposure Score, Exposure Score by Machine Groups, Device Secure Score |
| **Baselines** | Baseline Profiles, Baseline Configurations |
| **Utilities** | Info Gathering, Library Files |

## Configuration

### Environment Setup
1. Copy `services/get_data/src/settings.env.example` to `settings.env`
2. Configure your database connection and API credentials
3. Set up endpoint-specific configurations in `config.py`

### Database Configuration
- **Server**: SQL Server with ODBC Driver 18
- **Database**: Configurable database name
- **Tables**: Auto-created with `ep_` prefix
- **Connection**: Integrated security or SQL authentication

## Installation

### Prerequisites
- Python 3.8+
- SQL Server with ODBC Driver 18
- Microsoft Defender for Endpoint API access
- UV package manager (recommended)

### Setup
```bash
# Clone the repository
git clone https://github.com/jvilchesf/MDEndpoints.git
cd MDEndpoints

# Install dependencies
uv sync

# Configure environment
cp services/get_data/src/settings.env.example services/get_data/src/settings.env
# Edit settings.env with your configuration

# Run the application
python main.py
```

## Usage

### Running Data Collection
```bash
# Run all endpoints
python services/get_data/src/main.py

# Run specific endpoint (if supported)
python services/get_data/src/main.py --endpoint vulnerabilities
```

### Database Operations
The system automatically:
- Creates database tables if they don't exist
- Handles data deduplication
- Logs execution details
- Manages batch processing

### Monitoring
- Check `ep_endpoint_execution_log` table for execution status
- Monitor logs for error handling and performance metrics
- Review batch processing statistics

## API Endpoints Configuration

Each endpoint is configured with:
- **API Path**: Microsoft Defender API endpoint URL
- **Table Name**: Target database table (with `ep_` prefix)
- **Columns**: Database column definitions
- **Page Size**: Number of records per API call
- **Batch Size**: Number of records per database batch
- **Unique Key**: Fields used for deduplication
- **Special Settings**: Endpoint-specific configurations

## Development

### Adding New Endpoints
1. Add endpoint configuration to `ENDPOINT_CONFIGS` in `config.py`
2. Define table schema and column mappings
3. Set appropriate page and batch sizes
4. Configure unique keys for deduplication

### Database Schema Updates
- Tables are created automatically based on configuration
- Column definitions support various SQL Server data types
- Indexes and constraints can be added as needed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Create an issue in the GitHub repository
- Check the execution logs for troubleshooting
- Review the configuration documentation

## Changelog

### Version 1.0.0
- Initial release with 28 endpoint configurations
- Complete database schema management
- Automated data collection and processing
- Comprehensive error handling and logging
