# AWS Networking and VPC

## Purpose

Defines standard networking practices and VPC configuration for AWS applications to ensure secure, scalable, and well-architected network infrastructure.

## Instructions

- ALWAYS use VPC for all AWS resources with proper subnet design (ID: USE_VPC)
- ALWAYS implement proper subnet design with public, private, and database subnets (ID: SUBNET_DESIGN)
- ALWAYS use AWS Transit Gateway for multi-VPC connectivity when appropriate (ID: USE_TRANSIT_GATEWAY)
- ALWAYS implement proper security groups with least privilege access (ID: SECURITY_GROUPS)
- ALWAYS use Network ACLs for additional network security layer (ID: USE_NACLS)
- ALWAYS implement proper NAT Gateway or NAT Instance for private subnet internet access (ID: NAT_GATEWAY)
- ALWAYS use AWS VPC Flow Logs for network monitoring and troubleshooting (ID: VPC_FLOW_LOGS)
- ALWAYS implement proper DNS resolution using Route 53 and VPC DNS (ID: DNS_RESOLUTION)
- ALWAYS use AWS PrivateLink for secure service-to-service communication (ID: USE_PRIVATELINK)
- ALWAYS implement proper VPC peering for cross-VPC communication when needed (ID: VPC_PEERING)
- ALWAYS use AWS Direct Connect for hybrid cloud connectivity (ID: USE_DIRECT_CONNECT)
- ALWAYS implement proper load balancing using Application Load Balancer or Network Load Balancer (ID: LOAD_BALANCING)
- ALWAYS use AWS CloudFront for global content delivery and caching (ID: USE_CLOUDFRONT)
- ALWAYS implement proper VPN connectivity for secure remote access (ID: VPN_CONNECTIVITY)
- ALWAYS use AWS Route 53 for DNS management and health checks (ID: USE_ROUTE53)
- ALWAYS implement proper network segmentation for different application tiers (ID: NETWORK_SEGMENTATION)
- ALWAYS use AWS WAF for web application firewall protection (ID: USE_AWS_WAF)
- ALWAYS implement proper network monitoring using CloudWatch and VPC Flow Logs (ID: NETWORK_MONITORING)
- ALWAYS use AWS Global Accelerator for improved application performance (ID: USE_GLOBAL_ACCELERATOR)
- ALWAYS implement proper network security using AWS Shield and DDoS protection (ID: NETWORK_SECURITY)
- ALWAYS use AWS VPC Endpoints for secure AWS service access (ID: USE_VPC_ENDPOINTS)
- ALWAYS implement proper network routing and route tables (ID: ROUTING_CONFIGURATION)
- ALWAYS use Terraform for network infrastructure as code (ID: NETWORK_IAC)
- ALWAYS implement proper network compliance and audit logging (ID: NETWORK_COMPLIANCE)
- ALWAYS use AWS Network Manager for centralized network management (ID: USE_NETWORK_MANAGER)

## Priority

High

## Error Handling

- If VPC is not suitable for the use case, document the alternative approach and security implications
- If Transit Gateway is not available, use VPC peering or other connectivity solutions
- If Direct Connect is not feasible, use VPN or other connectivity methods
- If network segmentation cannot be implemented, implement alternative security controls
- If network monitoring tools are not available, implement basic logging and plan for enhancement
