-- Drop existing tables if they exist to avoid conflicts
IF OBJECT_ID('dbo.ep_endpoint_execution_log', 'U') IS NOT NULL DROP TABLE dbo.ep_endpoint_execution_log;
IF OBJECT_ID('dbo.ep_vulnerabilities', 'U') IS NOT NULL DROP TABLE dbo.ep_vulnerabilities;
IF OBJECT_ID('dbo.ep_vulnerabilities_by_machine', 'U') IS NOT NULL DROP TABLE dbo.ep_vulnerabilities_by_machine;
IF OBJECT_ID('dbo.ep_device_av_info', 'U') IS NOT NULL DROP TABLE dbo.ep_device_av_info;
IF OBJECT_ID('dbo.ep_machines', 'U') IS NOT NULL DROP TABLE dbo.ep_machines;
IF OBJECT_ID('dbo.ep_secure_config_assessment', 'U') IS NOT NULL DROP TABLE dbo.ep_secure_config_assessment;
IF OBJECT_ID('dbo.ep_software_inventory', 'U') IS NOT NULL DROP TABLE dbo.ep_software_inventory;
IF OBJECT_ID('dbo.ep_non_product_software_inventory', 'U') IS NOT NULL DROP TABLE dbo.ep_non_product_software_inventory;
IF OBJECT_ID('dbo.ep_software_vulnerabilities_by_machine', 'U') IS NOT NULL DROP TABLE dbo.ep_software_vulnerabilities_by_machine;
IF OBJECT_ID('dbo.ep_remediation_tasks', 'U') IS NOT NULL DROP TABLE dbo.ep_remediation_tasks;
IF OBJECT_ID('dbo.ep_alerts', 'U') IS NOT NULL DROP TABLE dbo.ep_alerts;
IF OBJECT_ID('dbo.ep_device_authenticated_scan_definitions', 'U') IS NOT NULL DROP TABLE dbo.ep_device_authenticated_scan_definitions;
IF OBJECT_ID('dbo.ep_device_authenticated_scan_agents', 'U') IS NOT NULL DROP TABLE dbo.ep_device_authenticated_scan_agents;
IF OBJECT_ID('dbo.ep_browser_extensions_inventory', 'U') IS NOT NULL DROP TABLE dbo.ep_browser_extensions_inventory;
IF OBJECT_ID('dbo.ep_browser_extensions_permissions', 'U') IS NOT NULL DROP TABLE dbo.ep_browser_extensions_permissions;
IF OBJECT_ID('dbo.ep_investigations', 'U') IS NOT NULL DROP TABLE dbo.ep_investigations;
IF OBJECT_ID('dbo.ep_certificate_assessments', 'U') IS NOT NULL DROP TABLE dbo.ep_certificate_assessments;
IF OBJECT_ID('dbo.ep_indicators', 'U') IS NOT NULL DROP TABLE dbo.ep_indicators;
IF OBJECT_ID('dbo.ep_info_gathering', 'U') IS NOT NULL DROP TABLE dbo.ep_info_gathering;
IF OBJECT_ID('dbo.ep_library_files', 'U') IS NOT NULL DROP TABLE dbo.ep_library_files;
IF OBJECT_ID('dbo.ep_machine_actions', 'U') IS NOT NULL DROP TABLE dbo.ep_machine_actions;
IF OBJECT_ID('dbo.ep_exposure_score_by_machine_groups', 'U') IS NOT NULL DROP TABLE dbo.ep_exposure_score_by_machine_groups;
IF OBJECT_ID('dbo.ep_exposure_score', 'U') IS NOT NULL DROP TABLE dbo.ep_exposure_score;
IF OBJECT_ID('dbo.ep_device_secure_score', 'U') IS NOT NULL DROP TABLE dbo.ep_device_secure_score;
IF OBJECT_ID('dbo.ep_baseline_compliance_assessment', 'U') IS NOT NULL DROP TABLE dbo.ep_baseline_compliance_assessment;
IF OBJECT_ID('dbo.ep_baseline_profiles', 'U') IS NOT NULL DROP TABLE dbo.ep_baseline_profiles;
IF OBJECT_ID('dbo.ep_baseline_configurations', 'U') IS NOT NULL DROP TABLE dbo.ep_baseline_configurations;
IF OBJECT_ID('dbo.ep_software', 'U') IS NOT NULL DROP TABLE dbo.ep_software;
IF OBJECT_ID('dbo.ep_execution_log', 'U') IS NOT NULL DROP TABLE dbo.ep_execution_log;

-- 1. Execution log table (removed id column)
CREATE TABLE ep_endpoint_execution_log (
    endpoint NVARCHAR(255),
    tableName NVARCHAR(255),
    startTime NVARCHAR(255),
    endTime NVARCHAR(255),
    status NVARCHAR(50),
    recordsCount NVARCHAR(255),
    batchSize NVARCHAR(255),
    errorMessage NTEXT,
    additionalInfo NTEXT
);

-- 2. Vulnerabilities (removed id column)
CREATE TABLE ep_vulnerabilities (
    id NVARCHAR(255),
    name NVARCHAR(255),
    description NTEXT,
    severity NVARCHAR(50),
    cvssV3 NVARCHAR(255),
    cvssVector NTEXT,
    exposedMachines NVARCHAR(255),
    publishedOn NVARCHAR(255),
    updatedOn NVARCHAR(255),
    firstDetected NVARCHAR(255),
    patchFirstAvailable NVARCHAR(255),
    publicExploit NVARCHAR(50),
    exploitVerified NVARCHAR(50),
    exploitInKit NVARCHAR(50),
    exploitTypes NTEXT,
    exploitUris NTEXT,
    cveSupportability NVARCHAR(50),
    tags NTEXT,
    epss NVARCHAR(255)
);

-- 3. Vulnerabilities by Machine (removed id column)
CREATE TABLE ep_vulnerabilities_by_machine (
    cveId NVARCHAR(255),
    machineId NVARCHAR(255),
    fixingKbId NVARCHAR(255),
    productName NVARCHAR(255),
    productVendor NVARCHAR(255),
    productVersion NVARCHAR(50),
    severity NVARCHAR(50)
);

-- 4. Device AV Info (removed id column)
CREATE TABLE ep_device_av_info (
    id NVARCHAR(255),
    machineId NVARCHAR(255),
    computerDnsName NVARCHAR(255),
    osKind NVARCHAR(50),
    osPlatform NVARCHAR(50),
    osVersion NVARCHAR(50),
    avMode NVARCHAR(50),
    avSignatureVersion NVARCHAR(50),
    avEngineVersion NVARCHAR(50),
    avPlatformVersion NVARCHAR(50),
    lastSeenTime NVARCHAR(255),
    quickScanResult NVARCHAR(50),
    quickScanError NVARCHAR(50),
    quickScanTime NVARCHAR(255),
    fullScanResult NVARCHAR(50),
    fullScanError NVARCHAR(50),
    fullScanTime NVARCHAR(255),
    dataRefreshTimestamp NVARCHAR(255),
    avEngineUpdateTime NVARCHAR(255),
    avSignatureUpdateTime NVARCHAR(255),
    avPlatformUpdateTime NVARCHAR(255),
    avIsSignatureUpToDate NVARCHAR(255),
    avIsEngineUpToDate NVARCHAR(255),
    avIsPlatformUpToDate NVARCHAR(255),
    avSignaturePublishTime NVARCHAR(255),
    avSignatureDataRefreshTime NVARCHAR(255),
    cloudProtectionState NVARCHAR(255),
    avModeDataRefreshTime NVARCHAR(255),
    rbacGroupName NVARCHAR(255),
    rbacGroupId NVARCHAR(255)
);

-- 5. Machines (removed id column)
CREATE TABLE ep_machines (
    id NVARCHAR(255),
    mergedIntoMachineId NVARCHAR(255),
    isPotentialDuplication NVARCHAR(255),
    isExcluded NVARCHAR(255), 
    exclusionReason NVARCHAR(255),
    computerDnsName NVARCHAR(255),
    firstSeen NVARCHAR(255),
    lastSeen NVARCHAR(255),
    osPlatform NVARCHAR(50),
    osVersion NVARCHAR(255),
    osProcessor NVARCHAR(50),
    version NTEXT,
    lastIpAddress NVARCHAR(50),
    lastExternalIpAddress NVARCHAR(50),
    agentVersion NVARCHAR(255),
    osBuild NVARCHAR(255),
    healthStatus NVARCHAR(50),
    deviceValue NVARCHAR(255),
    rbacGroupId NVARCHAR(255),
    rbacGroupName NVARCHAR(255),
    riskScore NVARCHAR(255),
    exposureLevel NVARCHAR(255),
    isAadJoined NVARCHAR(255),
    aadDeviceId NVARCHAR(255),
    machineTags NVARCHAR(255),
    onboardingStatus NVARCHAR(255),
    osArchitecture NVARCHAR(255),
    managedBy NVARCHAR(255),
    managedByStatus NVARCHAR(255),
    ipAddresses NTEXT,
    vmMetadata NTEXT
);

-- 6. Secure Configuration Assessment (removed constraints)
CREATE TABLE ep_secure_config_assessment (
    deviceId NVARCHAR(255),
    rbacGroupId NVARCHAR(255),
    rbacGroupName NVARCHAR(255),
    deviceName NVARCHAR(255),
    osPlatform NVARCHAR(50),
    osVersion NVARCHAR(50),
    timestamp NVARCHAR(255),
    configurationId NVARCHAR(255),
    configurationCategory NVARCHAR(255),
    configurationSubcategory NVARCHAR(255),
    configurationImpact NVARCHAR(255),
    isCompliant NVARCHAR(255),
    isApplicable NVARCHAR(255),
    isExpectedUserImpact NVARCHAR(255),
    configurationName NVARCHAR(255),
    recommendationReference NVARCHAR(255)
);

-- 7. Software Inventory (removed id and constraints)
CREATE TABLE ep_software_inventory (
    deviceId NVARCHAR(255),
    rbacGroupId NVARCHAR(255),
    rbacGroupName NVARCHAR(255),
    deviceName NVARCHAR(255),
    osPlatform NVARCHAR(50),
    softwareVendor NVARCHAR(255),
    softwareName NVARCHAR(255),
    softwareVersion NVARCHAR(255),
    numberOfWeaknesses NVARCHAR(255),
    diskPaths NTEXT,
    registryPaths NTEXT,
    softwareFirstSeenTimestamp NVARCHAR(255),
    endOfSupportStatus NVARCHAR(255),
    endOfSupportDate NVARCHAR(255)
);

-- 8. Non-Product Software Inventory (removed constraints)
CREATE TABLE ep_non_product_software_inventory (
    deviceId NVARCHAR(255),
    rbacGroupId NVARCHAR(255),
    rbacGroupName NVARCHAR(255),
    deviceName NVARCHAR(255),
    osPlatform NVARCHAR(50),
    softwareVendor NVARCHAR(500),
    softwareName NVARCHAR(500),
    softwareVersion NVARCHAR(255),
    softwareLastSeenTimestamp NVARCHAR(255)
);

-- 9. Software Vulnerabilities by Machine (removed id column)
CREATE TABLE ep_software_vulnerabilities_by_machine (
    cveId NVARCHAR(255),
    deviceId NVARCHAR(255),
    deviceName NVARCHAR(255),
    diskPaths NTEXT,
    exploitabilityLevel NVARCHAR(50),
    firstSeenTimestamp NVARCHAR(255),
    lastSeenTimestamp NVARCHAR(255),
    osPlatform NVARCHAR(50),
    osVersion NVARCHAR(255),
    osArchitecture NVARCHAR(255),
    rbacGroupName NVARCHAR(255),
    recommendationReference NVARCHAR(255),
    recommendedSecurityUpdate NVARCHAR(255),
    recommendedSecurityUpdateId NVARCHAR(255),
    recommendedSecurityUpdateUrl NVARCHAR(255),
    registryPaths NTEXT,
    securityUpdateAvailable NVARCHAR(255),
    softwareName NVARCHAR(255),
    softwareVendor NVARCHAR(255),
    softwareVersion NVARCHAR(255),
    vulnerabilitySeverityLevel NVARCHAR(255),
    rbacGroupId NVARCHAR(255),
    endOfSupportStatus NVARCHAR(255),
    endOfSupportDate NVARCHAR(255),
    cvssScore NVARCHAR(255),
    cveMitigationStatus NVARCHAR(255)
);

-- 10. Remediation Tasks (removed id column)
CREATE TABLE ep_remediation_tasks (
    id NVARCHAR(255),
    title NVARCHAR(255),
    createdOn NVARCHAR(255),
    requesterId NVARCHAR(255),
    requesterEmail NVARCHAR(255),
    status NVARCHAR(50),
    statusLastModifiedOn NVARCHAR(255),
    description NTEXT,
    relatedComponent NVARCHAR(255),
    targetDevices NTEXT,
    rbacGroupNames NTEXT,
    fixedDevices NTEXT,
    requesterNotes NTEXT,
    dueOn NVARCHAR(255),
    category NVARCHAR(50),
    productivityImpactRemediationType NVARCHAR(50),
    priority NVARCHAR(50),
    completionMethod NVARCHAR(50),
    completerId NVARCHAR(255),
    completerEmail NVARCHAR(255),
    scid NVARCHAR(255),
    type NVARCHAR(50),
    productId NVARCHAR(255),
    vendorId NVARCHAR(255),
    nameId NVARCHAR(255),
    recommendedVersion NVARCHAR(50),
    recommendedVendor NVARCHAR(255),
    recommendedProgram NVARCHAR(255),
    recommendationReference NVARCHAR(255)
);

-- 11. Alerts (removed id column)
CREATE TABLE ep_alerts (
    id NVARCHAR(255),
    incidentId NVARCHAR(255),
    investigationId NVARCHAR(255),
    assignedTo NVARCHAR(255),
    severity NVARCHAR(50),
    status NVARCHAR(50),
    classification NVARCHAR(255),
    determination NVARCHAR(255),
    investigationState NVARCHAR(50),
    detectionSource NVARCHAR(255),
    detectorId NVARCHAR(255),
    category NVARCHAR(255),
    threatFamilyName NVARCHAR(255),
    title NVARCHAR(255),
    description NTEXT,
    alertCreationTime NVARCHAR(255),
    firstEventTime NVARCHAR(255),
    lastEventTime NVARCHAR(255),
    lastUpdateTime NVARCHAR(255),
    resolvedTime NVARCHAR(255),
    machineId NVARCHAR(255),
    computerDnsName NVARCHAR(255),
    rbacGroupName NVARCHAR(255),
    aadTenantId NVARCHAR(255),
    threatName NVARCHAR(255),
    mitreTechniques NTEXT,
    relatedUser NTEXT,
    loggedOnUsers NTEXT,
    comments NTEXT,
    evidence NTEXT,
    domains NTEXT
);

-- 12. Device Authenticated Scan Definitions (removed id column)
CREATE TABLE ep_device_authenticated_scan_definitions (
    id NVARCHAR(255),
    scanType NVARCHAR(50),
    scanName NVARCHAR(255),
    isActive NVARCHAR(255),
    target NTEXT,
    orgId NVARCHAR(255),
    intervalInHours NVARCHAR(255),
    createdBy NVARCHAR(255),
    targetType NVARCHAR(50),
    scanAuthenticationParams NTEXT,
    scannerAgent NTEXT,
    latestScan NTEXT,
    advancedActiveConfiguration NTEXT
);

-- 13. Device Authenticated Scan Agents (removed id column)
CREATE TABLE ep_device_authenticated_scan_agents (
    machineId NVARCHAR(255),
    lastSeen NVARCHAR(255),
    computerDnsName NVARCHAR(255),
    assignedApplicationId NVARCHAR(255),
    scannerSoftwareVersion NVARCHAR(50),
    lastCommandExecutionTimestamp NVARCHAR(255),
    mdeClientVersion NVARCHAR(50)
);

-- 14. Browser Extensions Inventory (removed constraints)
CREATE TABLE ep_browser_extensions_inventory (
    deviceId NVARCHAR(255),
    rbacGroupId NVARCHAR(255),
    rbacGroupName NVARCHAR(255),
    installationTime NVARCHAR(255),
    browserName NVARCHAR(255),
    extensionId NVARCHAR(255),
    extensionName NVARCHAR(255),
    extensionDescription NTEXT,
    extensionVersion NVARCHAR(50),
    extensionRisk NVARCHAR(50),
    extensionVendor NVARCHAR(255),
    isActivated NVARCHAR(255)
);

-- 15. Browser Extensions Permissions (removed id column)
CREATE TABLE ep_browser_extensions_permissions (
    [key] NVARCHAR(1000),
    permissionName NVARCHAR(1000), 
    description NVARCHAR(1000)
);

-- 16. Investigations (removed id column)
CREATE TABLE ep_investigations (
    startTime NVARCHAR(255),
    endTime NVARCHAR(255),
    state NVARCHAR(50),
    cancelledBy NVARCHAR(255),
    statusDetails NTEXT,
    machineId NVARCHAR(255),
    computerDnsName NVARCHAR(255),
    triggeringAlertId NVARCHAR(255)
);

-- 17. Certificate Assessments (removed constraints)
CREATE TABLE ep_certificate_assessments (
    deviceId NVARCHAR(255),
    deviceName NVARCHAR(255),
    thumbprint NVARCHAR(255),
    path NTEXT,
    signatureAlgorithm NVARCHAR(255),
    keySize NVARCHAR(50),
    expirationDate NVARCHAR(255),
    issueDate NVARCHAR(255),
    subjectType NVARCHAR(50),
    serialNumber NVARCHAR(255),
    issuedTo NTEXT,
    issuedBy NTEXT,
    keyUsage NTEXT,
    extendedKeyUsage NTEXT,
    rbacGroupId NVARCHAR(255),
    rbacGroupName NVARCHAR(255)
);

-- 18. Indicators (removed id column)
CREATE TABLE ep_indicators (
    id NVARCHAR(255),
    indicatorValue NVARCHAR(255),
    indicatorType NVARCHAR(50),
    action NVARCHAR(50),
    createdBy NVARCHAR(255),
    severity NVARCHAR(50),
    category NVARCHAR(255),
    application NVARCHAR(255),
    educateUrl NTEXT,
    bypassDurationHours NVARCHAR(50),
    title NVARCHAR(255),
    description NTEXT,
    recommendedActions NTEXT,
    creationTimeDateTimeUtc NVARCHAR(255),
    expirationTime NVARCHAR(255),
    lastUpdateTime NVARCHAR(255),
    lastUpdatedBy NVARCHAR(255),
    rbacGroupNames NTEXT,
    rbacGroupIds NTEXT,
    notificationId NVARCHAR(255),
    notificationBody NTEXT,
    version NVARCHAR(50),
    mitreTechniques NTEXT,
    historicalDetection NVARCHAR(50),
    lookBackPeriod NVARCHAR(50),
    generateAlert NVARCHAR(50),
    additionalInfo NTEXT,
    createdByDisplayName NVARCHAR(255),
    externalId NVARCHAR(255),
    createdBySource NVARCHAR(255),
    certificateInfo NTEXT
);

-- 19. Info Gathering (removed id column)
CREATE TABLE ep_info_gathering (
    exportFiles NTEXT,
    generatedTime NVARCHAR(255)
);

-- 20. Library Files (removed id column, kept sha256 as regular column)
CREATE TABLE ep_library_files (
    fileName NVARCHAR(255),
    sha256 NVARCHAR(255),
    description NTEXT,
    creationTime NVARCHAR(255),
    lastUpdatedTime NVARCHAR(255),
    createdBy NVARCHAR(255),
    hasParameters NVARCHAR(255),
    parametersDescription NTEXT
);

-- 21. Machine Actions (updated to match API data structure)
CREATE TABLE ep_machine_actions (
    id NVARCHAR(255),
    type NVARCHAR(255),
    title NVARCHAR(500),
    requestor NVARCHAR(255),
    requestorComment NTEXT,
    status NVARCHAR(255),
    machineId NVARCHAR(255),
    computerDnsName NVARCHAR(255),
    creationDateTimeUtc NVARCHAR(255),
    lastUpdateDateTimeUtc NVARCHAR(255),
    cancellationRequestor NVARCHAR(255),
    cancellationComment NTEXT,
    cancellationDateTimeUtc NVARCHAR(255),
    errorHResult NVARCHAR(255),
    scope NVARCHAR(255),
    externalId NVARCHAR(255),
    requestSource NVARCHAR(255),
    relatedFileInfo NVARCHAR(500),
    commands NTEXT,
    troubleshootInfo NTEXT
);

-- 22. Exposure Score by Machine Groups (removed constraints)
CREATE TABLE ep_exposure_score_by_machine_groups (
    time NVARCHAR(255),
    score NVARCHAR(255),
    rbacGroupName NVARCHAR(255),
    rbacGroupId NVARCHAR(255)
);

-- 23. Exposure Score (removed id column)
CREATE TABLE ep_exposure_score (
    time NVARCHAR(255),
    score NVARCHAR(255)
);

-- 24. Device Secure Score (removed id column)
CREATE TABLE ep_device_secure_score (
    time NVARCHAR(255),
    score NVARCHAR(255)
);

-- 25. Baseline Compliance Assessment (removed id column)
CREATE TABLE ep_baseline_compliance_assessment (
    id NVARCHAR(255),
    configurationId NVARCHAR(255),
    deviceId NVARCHAR(255),
    deviceName NVARCHAR(255),
    profileId NVARCHAR(255),
    osPlatform NVARCHAR(50),
    osVersion NVARCHAR(50),
    rbacGroupId NVARCHAR(255),
    rbacGroupName NVARCHAR(255),
    isApplicable NVARCHAR(255),
    isCompliant NVARCHAR(255),
    dataCollectionTimeOffset NVARCHAR(50),
    complianceCalculationTimeOffset NVARCHAR(50),
    recommendedValue NTEXT,
    currentValue NTEXT,
    source NTEXT,
    isExempt NVARCHAR(255),
    rawValue NTEXT
);

-- 26. Baseline Profiles (removed id column)
CREATE TABLE ep_baseline_profiles (
    id NVARCHAR(255),
    name NTEXT,
    description NTEXT,
    benchmark NTEXT,
    version NVARCHAR(50),
    operatingSystem NVARCHAR(50),
    operatingSystemVersion NVARCHAR(50),
    status NVARCHAR(50),
    complianceLevel NTEXT,
    settingsNumber NVARCHAR(255),
    createdBy NVARCHAR(255),
    lastUpdatedBy NVARCHAR(255),
    createdOnTimeOffset NVARCHAR(255),
    lastUpdateTimeOffset NVARCHAR(255),
    passedDevices NVARCHAR(255),
    totalDevices NVARCHAR(255),
    rbacGroupIdsProfileScope NTEXT,
    rbacGroupNamesProfileScope NTEXT,
    deviceTagsProfileScope NTEXT
);

-- 27. Baseline Configurations (removed id column)
CREATE TABLE ep_baseline_configurations (
    id NVARCHAR(255),
    uniqueId NVARCHAR(255),
    benchmarkName NTEXT,
    benchmarkVersion NVARCHAR(50),
    name NTEXT,
    description NTEXT,
    category NTEXT,
    complianceLevels NTEXT,
    cce NVARCHAR(255),
    rationale NTEXT,
    remediation NTEXT,
    recommendedValue NTEXT,
    source NTEXT,
    isCustom NVARCHAR(50),
    assessmentMethod NTEXT
);

-- 28. Software (updated to match API data structure)
CREATE TABLE ep_software (
    id NVARCHAR(255),
    name NVARCHAR(500),
    vendor NVARCHAR(500),
    weaknesses NTEXT,
    publicExploit NVARCHAR(50),
    activeAlert NVARCHAR(50),
    exposedMachines NTEXT,
    installedMachines NTEXT,
    impactScore NVARCHAR(50),
    isNormalized NVARCHAR(50),
    category NVARCHAR(255),
    distributions NTEXT
);

-- Create the execution log table
CREATE TABLE ep_execution_log (
    id INT IDENTITY(1,1) PRIMARY KEY,
    table_name NVARCHAR(255) NOT NULL,
    start_time_endpoint NVARCHAR(255) NOT NULL,
    end_time_endpoint NVARCHAR(255) NOT NULL,
    status NVARCHAR(50) NOT NULL,
    total_rows INT NULL,
    created_at DATETIME2(3) DEFAULT GETDATE(),
    updated_at DATETIME2(3) DEFAULT GETDATE()
);
GO
