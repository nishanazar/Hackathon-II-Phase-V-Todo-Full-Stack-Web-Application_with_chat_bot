# API Contract: Cloud Provider Interface for Kubernetes Cluster Management

## Overview
This document defines the interface between our cluster management system and the Oracle Cloud Infrastructure (OCI) API for managing Kubernetes clusters. This contract ensures consistent interactions with the cloud provider's API regardless of the specific cloud platform used (Oracle OKE, Azure AKS, or Google GKE).

## Base URL
- Oracle OKE: `https://containerengine.{region}.oraclecloud.com`
- Azure AKS: `https://management.azure.com`
- Google GKE: `https://container.googleapis.com/v1`

## Authentication
All API requests require authentication using the respective cloud provider's authentication mechanism:
- Oracle OKE: OCI Signature-based authentication
- Azure AKS: Azure AD OAuth 2.0
- Google GKE: Google OAuth 2.0

## API Operations

### 1. Get Cluster Information
**Endpoint**: `GET /clusters/{clusterId}`
**Description**: Retrieves detailed information about a specific Kubernetes cluster.

**Request**:
- Headers: Authorization header with valid token
- Path Parameter: clusterId (the unique identifier of the cluster)

**Response**:
- Status: 200 OK
- Body: Cluster object with properties:
  - id: string (cluster identifier)
  - name: string (cluster name)
  - status: string (current status of the cluster)
  - kubernetesVersion: string (version of Kubernetes)
  - endpoint: string (API server endpoint)
  - caCertificate: string (base64-encoded CA certificate)
  - nodeCount: integer (number of worker nodes)
  - createdTime: string (ISO 8601 timestamp)

### 2. Create Cluster
**Endpoint**: `POST /clusters`
**Description**: Creates a new Kubernetes cluster with the specified configuration.

**Request**:
- Headers: Authorization header with valid token, Content-Type: application/json
- Body: Cluster configuration object with properties:
  - name: string (desired cluster name)
  - kubernetesVersion: string (desired Kubernetes version)
  - nodePool: object (configuration for the initial node pool)
    - name: string (node pool name)
    - nodeShape: string (shape of the compute instances)
    - nodeCount: integer (initial number of nodes)
    - nodeImage: string (OS image for the nodes)

**Response**:
- Status: 202 Accepted
- Body: Operation object with properties:
  - id: string (operation identifier)
  - status: string (current status of the operation)
  - targetResource: string (resource being operated on)

### 3. Get Cluster Status
**Endpoint**: `GET /operations/{operationId}`
**Description**: Checks the status of a cluster creation or modification operation.

**Request**:
- Headers: Authorization header with valid token
- Path Parameter: operationId (the unique identifier of the operation)

**Response**:
- Status: 200 OK
- Body: Operation object with properties:
  - id: string (operation identifier)
  - status: string (current status of the operation)
  - progress: integer (percentage complete)
  - error: object (error details if operation failed)

### 4. List Nodes
**Endpoint**: `GET /clusters/{clusterId}/nodes`
**Description**: Lists all nodes in the specified cluster.

**Request**:
- Headers: Authorization header with valid token
- Path Parameter: clusterId (the unique identifier of the cluster)

**Response**:
- Status: 200 OK
- Body: Array of node objects with properties:
  - id: string (node identifier)
  - name: string (node name)
  - status: string (current status of the node)
  - shape: string (compute instance shape)
  - image: string (OS image)

### 5. Delete Cluster
**Endpoint**: `DELETE /clusters/{clusterId}`
**Description**: Initiates the deletion of a Kubernetes cluster.

**Request**:
- Headers: Authorization header with valid token
- Path Parameter: clusterId (the unique identifier of the cluster)

**Response**:
- Status: 202 Accepted
- Body: Operation object with properties:
  - id: string (operation identifier)
  - status: string (current status of the operation)

## Error Handling
All API operations follow standard HTTP error response codes:
- 400: Bad Request - Invalid request parameters
- 401: Unauthorized - Invalid or expired authentication token
- 403: Forbidden - Insufficient permissions
- 404: Not Found - Resource does not exist
- 429: Too Many Requests - Rate limit exceeded
- 500: Internal Server Error - Unexpected server error
- 503: Service Unavailable - Service temporarily unavailable

## Rate Limits
Each cloud provider has specific rate limits for API requests:
- Oracle OKE: 100 requests per minute per tenant
- Azure AKS: 12,000 requests per hour per subscription
- Google GKE: 1,200 requests per minute per project

## Security Considerations
- All API communications must use HTTPS
- Authentication tokens should have minimal required permissions
- Tokens should be rotated regularly
- API requests should be logged for audit purposes