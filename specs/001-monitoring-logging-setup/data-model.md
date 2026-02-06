# Data Model: Monitoring & Logging Setup for Phase V

## Monitoring Configuration Entity

**Name**: MonitoringConfiguration
- **Fields**:
  - id: string (unique identifier for the configuration)
  - name: string (name of the monitoring setup, e.g., "Production Monitoring")
  - prometheusEndpoint: string (URL to Prometheus server)
  - grafanaEndpoint: string (URL to Grafana dashboard)
  - alertmanagerEndpoint: string (URL to Alertmanager)
  - enabled: boolean (whether monitoring is enabled)
  - createdAt: timestamp (when the configuration was created)
  - updatedAt: timestamp (when the configuration was last updated)

**Validation Rules**:
- All endpoint URLs must be valid HTTP/HTTPS URLs
- Configuration name must be unique
- At least one endpoint must be specified

## Grafana Dashboard Entity

**Name**: GrafanaDashboard
- **Fields**:
  - id: string (unique identifier for the dashboard)
  - title: string (display title of the dashboard)
  - uid: string (unique identifier used by Grafana)
  - url: string (full URL to access the dashboard)
  - panels: array (list of panel configurations)
  - variables: object (dashboard variable configurations)
  - refreshInterval: string (auto-refresh interval, e.g., "5s", "1m")
  - tags: array (list of tags for categorization)

**Validation Rules**:
- UID must be unique within Grafana instance
- Title must be non-empty
- Panels must be a valid array of panel configurations

## Alert Rule Entity

**Name**: AlertRule
- **Fields**:
  - id: string (unique identifier for the alert rule)
  - name: string (name of the alert rule)
  - expr: string (PromQL expression that triggers the alert)
  - for: string (duration to wait before firing the alert, e.g., "5m", "1m")
  - labels: object (key-value pairs to attach to the alert)
  - annotations: object (key-value pairs with longer descriptions)
  - enabled: boolean (whether the alert rule is active)
  - createdAt: timestamp (when the rule was created)
  - updatedAt: timestamp (when the rule was last updated)

**Validation Rules**:
- Expression must be a valid PromQL query
- Name must be unique
- Duration format must be valid (e.g., "30s", "5m", "1h")

## Log Configuration Entity

**Name**: LogConfiguration
- **Fields**:
  - id: string (unique identifier for the log configuration)
  - serviceName: string (name of the service being logged)
  - logLevel: string (minimum log level to capture, e.g., "debug", "info", "warn", "error")
  - retentionDays: number (number of days to retain logs)
  - format: string (log format, e.g., "json", "text")
  - destination: string (where to send logs, e.g., "stdout", "file", "centralized")
  - enabled: boolean (whether logging is enabled for this service)

**Validation Rules**:
- Service name must correspond to an existing service
- Log level must be one of the allowed values
- Retention days must be a positive integer
- Format must be one of the supported formats

## Metrics Configuration Entity

**Name**: MetricsConfiguration
- **Fields**:
  - id: string (unique identifier for the metrics configuration)
  - serviceName: string (name of the service being monitored)
  - scrapeInterval: string (how often to scrape metrics, e.g., "15s", "30s", "1m")
  - path: string (path where metrics are exposed, typically "/metrics")
  - port: number (port where metrics are exposed)
  - enabled: boolean (whether metrics collection is enabled)
  - labels: object (additional labels to attach to metrics)

**Validation Rules**:
- Service name must correspond to an existing service
- Scrape interval must be a valid duration
- Port must be a valid port number (1-65535)
- Path must be a valid URL path