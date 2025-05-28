from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='services/get_data/src/settings.env', env_file_encoding='utf-8'
    )

    SQL_HOST: str 
    SQL_DATABASE: str 
    SQL_USERNAME: str 
    SQL_PASSWORD: str 
    SQL_PORT: int 

    # API Configuration
    API_TENANT_ID: str
    API_CLIENT_ID: str
    API_CLIENT_SECRET: str
    # API Base URL
    BASE_URL: str 

    # Endpoint configurations for data processing
    ENDPOINT_CONFIGS :dict = {
        "vulnerabilities_by_machine": {
            "endpoint": "vulnerabilities/machinesVulnerabilities",
            "table_name": "ep_vulnerabilities_by_machine",
            "pagesize": 10000, 
        },
        "device_av_info": {
            "endpoint": "deviceavinfo",
            "table_name": "ep_device_av_info",
            "pagesize": 10000,
        },
        "vulnerabilities": {
            "endpoint": "vulnerabilities",
            "table_name": "ep_vulnerabilities",
            "pagesize": 8000,
        },
        "machines": {
            "endpoint": "machines",
            "table_name": "ep_machines",
            "pagesize": 5000,
        },
        "software_inventory": {
            "endpoint": "machines/SoftwareInventoryByMachine",
            "table_name": "ep_software_inventory",
            "pagesize": 200000,
        },
        "non_product_software_inventory": {
            "endpoint": "machines/SoftwareInventoryNoProductCodeByMachine",
            "table_name": "ep_non_product_software_inventory",
            "pagesize": 200000,
        },
        "remediation_tasks": {
            "endpoint": "remediationTasks",
            "table_name": "ep_remediation_tasks",
            "pagesize": 5000,
        },
        "alerts": {
            "endpoint": "alerts",
            "table_name": "ep_alerts",
            "pagesize": 5000,
        },
        "device_authenticated_scan_definitions": {
            "endpoint": "DeviceAuthenticatedScanDefinitions",
            "table_name": "ep_device_authenticated_scan_definitions",
            "pagesize": 100,
        },
        "device_authenticated_scan_agents": {
            "endpoint": "DeviceAuthenticatedScanAgents",
            "table_name": "ep_device_authenticated_scan_agents",
            "pagesize": 100,
        },
        "browser_extensions_inventory": {
            "endpoint": "Machines/BrowserExtensionsInventoryByMachine",
            "table_name": "ep_browser_extensions_inventory",
            "pagesize": 1000,
        },
        "browser_extensions_permissions": {
            "endpoint": "browserextensions/permissionsinfo",
            "table_name": "ep_browser_extensions_permissions",
            "pagesize": 1000,
        },
        "investigations": {
            "endpoint": "investigations",
            "table_name": "ep_investigations",
            "pagesize": 1000,

        },
        "certificate_assessments": {
            "endpoint": "machines/certificateAssessmentByMachine",
            "table_name": "ep_certificate_assessments",
            "pagesize": 100000,
        },
        "indicators": {
            "endpoint": "indicators",
            "table_name": "ep_indicators",
            "pagesize": 1000,
        },
        "info_gathering": {
            "endpoint": "Machines/InfoGatheringExport",
            "table_name": "ep_info_gathering",
            "pagesize": 1000,
        },
        "library_files": {
            "endpoint": "libraryfiles",
            "table_name": "ep_library_files",
            "pagesize": 1000,

        },
        "machine_actions": {
            "endpoint": "machineactions",
            "table_name": "ep_machine_actions",
            "pagesize": 1000,
        },
        "exposure_score_by_machine_groups": {
            "endpoint": "exposureScore/ByMachineGroups",
            "table_name": "ep_exposure_score_by_machine_groups",
            "columns": [
                "time", "score", "rbacGroupName"
            ],
            "pagesize": 1000,
            "unique_key": ["time"],
            "deduplicate_on": ["time"],
        },
        "exposure_score": {
            "endpoint": "exposureScore",
            "table_name": "ep_exposure_score",
            "columns": [
                "id", "time", "score"
            ],
            "pagesize": 1000,
            "unique_key": "id",
            "deduplicate_on": "id"
        },
        "configuration_score": {
            "endpoint": "configurationScore",
            "table_name": "ep_device_secure_score",
            "pagesize": 1000,
        },
        "baseline_compliance_assessment": {
            "endpoint": "machines/baselineComplianceAssessmentByMachine",
            "table_name": "ep_baseline_compliance_assessment",
            "pagesize": 5000,
        },
        "baseline_profiles": {
            "endpoint": "baselineProfiles",
            "table_name": "ep_baseline_profiles",
            "pagesize": 1000,
        },
        "baseline_configurations": {
            "endpoint": "baselineConfigurations",
            "table_name": "ep_baseline_configurations",
            "pagesize": 1000,
        },
        "software": {
            "endpoint": "Software",
            "table_name": "ep_software",
            "pagesize": 5000,
        },
        "software_vulnerabilities_by_machine": {
             "endpoint": "machines/SoftwareVulnerabilitiesByMachine",
             "table_name": "ep_software_vulnerabilities_by_machine",
             "pagesize": 100000,
        },
        "secure_config_assessment": {
             "endpoint": "machines/SecureConfigurationsAssessmentByMachine",
             "table_name": "ep_secure_config_assessment",
             "pagesize": 100000,
        }
    }