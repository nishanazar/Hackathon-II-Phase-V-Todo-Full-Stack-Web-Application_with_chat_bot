# Research: Helm Charts for Phase IV Kubernetes Deployment

**Feature**: 012-helm-charts-deployment

## Decision Log

### Decision 1: Single Chart vs Separate Charts

**Decision**: Use a single Helm chart for both frontend and backend services

**Rationale**: 
- Simplifies deployment process for hackathon judges and developers
- Reduces operational overhead with a single deployment unit
- Easier to manage versioning and upgrades
- Aligns with the success criteria specifying a single chart

**Alternatives considered**:
- Separate charts for frontend and backend: Would increase complexity with multiple deployments and coordination
- Monolithic chart with everything combined: Already the chosen approach

### Decision 2: Replica Count

**Decision**: Use 1 replica for both frontend and backend services

**Rationale**:
- Appropriate for hackathon/demo environment
- Reduces resource consumption on local Minikube clusters
- Simplifies debugging and monitoring
- Matches the target audience's needs (judges and developers)

**Alternatives considered**:
- Multiple replicas (2+): Would be more production-ready but unnecessary for demo purposes
- Auto-scaling: Overkill for hackathon environment

### Decision 3: Service Type

**Decision**: Use ClusterIP service type for both frontend and backend

**Rationale**:
- Appropriate for internal communication within the cluster
- Secure by default (not exposed externally)
- Allows for easy load balancing within the cluster
- Can be exposed externally via ingress or port-forwarding as needed

**Alternatives considered**:
- NodePort: Would expose services directly on the node's IP
- LoadBalancer: Would require cloud provider integration
- ExternalIP: More complex configuration

### Decision 4: Environment Variable Handling

**Decision**: Pass environment variables through values.yaml file

**Rationale**:
- Maintains flexibility for different environments
- Follows Helm best practices
- Allows for easy customization without rebuilding charts
- Secure handling of sensitive information

**Alternatives considered**:
- Hardcoding in templates: Less flexible and secure
- Using Kubernetes Secrets separately: More complex but could be layered on later

### Decision 5: Chart Generation Tool

**Decision**: Use kubectl-ai or kagent to generate initial chart structure

**Rationale**:
- Aligns with the constraint to prefer kubectl-ai/kagent for generation
- Accelerates development process
- Ensures proper Kubernetes resource structure
- Reduces manual errors

**Alternatives considered**:
- Manual creation: More time-consuming and error-prone
- Helm create command: Valid alternative but doesn't leverage AI tools as specified

## Technical Unknowns Resolved

### Unknown 1: Helm version compatibility

**Resolution**: Helm 3+ is confirmed as the target version based on the feature requirements. This is the current standard and offers the required functionality.

### Unknown 2: Image registry access

**Resolution**: The chart will be designed to work with the existing Docker images (todo-frontend:latest, todo-backend:latest) that are already available. No additional registry setup is required as part of this feature.

### Unknown 3: Resource requirements

**Resolution**: For the hackathon/demo environment, default resource requests and limits will be used initially. These can be adjusted later based on actual performance testing.

## Best Practices Applied

### Helm Chart Best Practices

1. **Template Structure**: Organized templates in a logical directory structure
2. **Value Validation**: Used semantic versioning in Chart.yaml
3. **Documentation**: Included NOTES.txt for post-installation instructions
4. **Naming Conventions**: Followed Helm naming conventions for resources
5. **Dependency Management**: No external dependencies required for this chart

### Kubernetes Best Practices

1. **Resource Labels**: Consistent labeling across all resources
2. **Health Checks**: Include readiness and liveness probes in deployments
3. **Security Context**: Apply appropriate security contexts
4. **Config Management**: Use values.yaml for configuration parameters
5. **Service Discovery**: Proper service naming for internal communication