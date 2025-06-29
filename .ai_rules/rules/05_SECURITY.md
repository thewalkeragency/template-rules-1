# Part 3 (subset): Security Agent Persona Rules & Comprehensive Security Guidelines

## Security Agent Responsibilities:
Auditing code, enforcing security best practices, managing secrets, and promoting a security-first mindset throughout the development lifecycle.

## Secure Vibe Coding Guide (Principles for AI Interaction):

1.  **Two-Stage Prompting for Security Review:**
    *   **Stage 1: Code Generation:** Generate the initial code based on the functional requirements.
    *   **Stage 2: Security Audit Prompt:** In a new, distinct prompt, instruct the AI to review its *own* generated code specifically for security vulnerabilities, adherence to best practices, and potential flaws.
        *   Example Audit Prompt: "Review the Python FastAPI endpoint code you just generated in `[filename].py` for common web vulnerabilities like OWASP Top 10 (SQLi, XSS, Insecure Deserialization, etc.), race conditions, insecure direct object references, and any issues related to authentication or authorization. Also check for hardcoded secrets or lack of input validation."

2.  **Security-by-Default in Prompts:**
    *   When prompting an AI to generate code, **explicitly request security features** and considerations. Do not assume the AI will include them by default.
    *   **Bad:** "Create an endpoint to upload files."
    *   **Good:** "Create a Python FastAPI endpoint to upload files. Ensure it sanitizes filenames to prevent path traversal, validates file types (allow only PNG, JPG, PDF), implements a strict file size limit of 5MB, and stores files in a secure, non-executable directory."

3.  **No Hardcoded Secrets:**
    *   **Absolute Rule:** All secrets, API keys, database credentials, tokens, and sensitive configuration values **must** be loaded from environment variables or a dedicated secrets management service (e.g., HashiCorp Vault, AWS Secrets Manager, Azure Key Vault).
    *   The AI must generate code that facilitates this (e.g., using `os.environ.get()` in Python, `process.env` in Node.js).
    *   A `.env.example` file should always be created with placeholders, and `.env` files must be in `.gitignore`.

4.  **Human-in-the-Loop for Critical Code:**
    *   All AI-generated code, especially code related to authentication, authorization, data validation, payment processing, or handling personally identifiable information (PII), **must be reviewed and approved by a human developer** before being merged into main branches or deployed to production.

5.  **Integrate SAST & Secret Scanning in CI/CD:**
    *   CI/CD pipelines **must** include steps for:
        *   **Static Analysis Security Testing (SAST):** Tools like Snyk, SonarQube, Bandit (Python), ESLint with security plugins (JavaScript/TypeScript) to analyze code for vulnerabilities.
        *   **Secret Scanning:** Tools like GitGuardian ggshield, TruffleHog, Gitleaks to detect accidental commits of secrets.
    *   Builds should fail if critical vulnerabilities or exposed secrets are detected.

## Comprehensive CI/CD & Development Security Guidelines
*(This section incorporates and expands upon the previous `SECURITY_GUIDELINES.md`)*

The core principle is to "shift left," meaning to integrate security considerations as early as possible in the development lifecycle.

## General Security & Privacy Principles

*   **User Data Privacy and Consent:**
    *   AI agents and systems **must** obtain explicit user consent before accessing, processing, storing, or transmitting any user data, especially Personally Identifiable Information (PII) or sensitive data.
    *   The scope of consent must be clear, and users should be able to revoke consent.
    *   Data handling practices must comply with relevant privacy regulations (e.g., GDPR, CCPA).
    *   Minimize data collection to only what is necessary for the task.
    *   Implement data anonymization or pseudonymization where appropriate.
*   **Secure Error Handling:**
    *   Error messages returned to users or logged externally **must not** reveal sensitive system details, internal paths, stack traces, or confidential information that could aid an attacker.
    *   Log detailed error information internally for debugging purposes, but provide generic, user-friendly error messages to the end-user.
*   **Tool Integration Security (Capability Declaration & Sampling):**
    *   Tools integrated via MCP or other mechanisms must explicitly declare their capabilities, including any data they access or modify.
    *   Operations involving sampling or automated decision-making by AI agents that have significant impact **must** require user approval by default, unless explicitly configured for autonomous operation in specific, trusted contexts.

### 1. Secure Your Source Code and Dependencies

*   **Secrets Management (Reiteration & Expansion):**
    *   As stated above: Never hardcode secrets. Use environment variables or dedicated secret managers.
    *   Utilize tools provided by your CI/CD platform for managing secrets within pipeline contexts (e.g., GitHub Actions secrets, GitLab CI/CD variables).
    *   Limit access to secrets based on the Principle of Least Privilege for both humans and automated processes.
    *   Implement regular rotation policies for all secrets.
    *   **Automated Secrets Scanning:** Integrate tools into pre-commit hooks and CI pipelines.

*   **Software Composition Analysis (SCA):**
    *   Use SCA tools (e.g., OWASP Dependency-Check, Snyk, Dependabot, Trivy, GitLab Dependency Scanning) to identify known vulnerabilities in your open-source and third-party libraries/dependencies.
    *   Regularly scan and update dependencies to patched versions.
    *   Establish a policy for handling vulnerable dependencies (e.g., update within X days, risk assessment for unpatchable vulns).
    *   Enable automated dependency updates where feasible (e.g., Dependabot).

*   **Static Application Security Testing (SAST):**
    *   Integrate SAST tools relevant to your programming languages into your CI pipeline and potentially into developer IDEs.
    *   These tools analyze source code (or compiled code) for potential security vulnerabilities without executing the code.
    *   Configure SAST to run on every commit or merge request.
    *   Triage and remediate findings promptly based on severity.

### 2. Secure Your CI/CD Pipeline Configuration

*   **Principle of Least Privilege (PoLP) for Pipeline Execution:**
    *   Ensure that CI/CD jobs, runners/agents, and any service accounts used by the pipeline have only the minimum necessary permissions to perform their tasks.
    *   Avoid using highly privileged accounts or overly broad permissions (e.g., admin access to cloud environments) for routine pipeline operations.
    *   Use distinct roles and permissions for different pipeline stages (e.g., build stage might need fewer permissions than a deployment stage).

*   **Secure Pipeline Definitions:**
    *   Store pipeline definitions (e.g., `Jenkinsfile`, `gitlab-ci.yml`, GitHub Actions workflows) in version control (Git).
    *   Require code reviews for changes to pipeline definitions, especially those involving deployment scripts, secret access, or security-sensitive environments.
    *   Be cautious with third-party actions, plugins, or scripts used in your pipeline. Vet them for security, pin them to specific versions, and keep them updated. Only use trusted sources.

*   **Protect the CI/CD Infrastructure:**
    *   Secure access to your CI/CD server/service (e.g., Jenkins master, GitLab instance, GitHub organization settings). Use strong authentication (MFA) for all users and admins.
    *   Regularly update your CI/CD software and its plugins/extensions to patch known vulnerabilities.
    *   Harden the operating systems and networks of your CI/CD runners/agents. Keep them patched.
    *   Isolate build environments to prevent cross-contamination between builds, especially if running untrusted code (e.g., from external PRs). Use ephemeral build agents or containerized builds.

### 3. Secure Your Build and Test Processes

*   **Dynamic Application Security Testing (DAST):**
    *   Integrate DAST tools (e.g., OWASP ZAP, Burp Suite (automated scans), Acunetix) to scan your running application in a dedicated test environment.
    *   DAST tools test the application from the outside, looking for runtime vulnerabilities.
    *   Typically run DAST scans after deployment to a staging or QA environment.

*   **Interactive Application Security Testing (IAST):**
    *   Consider IAST tools if your application and environment support them.
    *   IAST agents instrument the application from within while it runs (often during functional testing) to identify vulnerabilities with more context and accuracy.

*   **Infrastructure as Code (IaC) Scanning:**
    *   If you use IaC (e.g., Terraform, CloudFormation, Ansible, Helm charts, Pulumi), scan these configurations for security misconfigurations *before* deployment.
    *   Tools like `tfsec`, `terrascan`, `checkov`, `kube-score`, `terragrunt` with OPA policies can help.

*   **Container Image Scanning:**
    *   If you use containers (e.g., Docker), scan your container images for known vulnerabilities in the OS packages and application dependencies.
    *   Tools like Trivy, Clair, Snyk Container, Docker Scout, or cloud provider native scanners (e.g., AWS ECR Scan, Azure Defender for ACR) can be integrated into your CI pipeline.
    *   Scan images before pushing them to a registry and periodically scan images already in your registry.
    *   Use minimal base images and remove unnecessary packages.

### 4. Secure Your Deployment Process

*   **Secure Build Artifacts:**
    *   Store build artifacts (binaries, packages, container images) in a secure, access-controlled artifact repository (e.g., Nexus, Artifactory, GitLab Package Registry, GitHub Packages, cloud provider artifact registries).
    *   Consider digitally signing build artifacts to ensure their integrity and provenance.
    *   Implement retention policies to clean up old or unused artifacts.

*   **Controlled Deployments:**
    *   Implement approval gates (manual or automated based on checks) for deployments to sensitive environments (e.g., staging, production).
    *   Use deployment strategies like blue/green deployments, canary releases, or rolling updates to minimize the impact of a faulty or insecure deployment and allow for quick rollback.
    *   Log all deployment activities for auditability.

*   **Post-Deployment Verification & Configuration Management:**
    *   After deployment, run automated smoke tests and basic security checks to ensure the application is functioning correctly and securely in the new environment.
    *   Continuously monitor deployed application configurations for drift from secure baselines. Use configuration management tools (e.g., Ansible, Chef, Puppet, cloud provider config management) to enforce desired state.

### 5. Monitoring, Logging, and Compliance

*   **Runtime Security Monitoring & Infrastructure Scanning:**
    *   Continuously monitor your production environment for suspicious activity, intrusions, and emerging vulnerabilities.
    *   Use tools for intrusion detection/prevention (IDS/IPS), web application firewalls (WAF), security information and event management (SIEM), and vulnerability scanning of your production infrastructure.
    *   Implement robust logging for applications and infrastructure. Ensure logs are centralized, secured, and monitored for security events.

*   **Compliance Checks:**
    *   If applicable to your project (e.g., PCI DSS, HIPAA, SOC 2, GDPR), integrate automated checks and evidence gathering into your CI/CD pipeline and operational processes to ensure and demonstrate compliance.
    *   Maintain audit trails of all CI/CD activities, access controls, and security-related events.

*   **Regular Review and Updates:**
    *   Periodically review and update your CI/CD security practices, tools, configurations, and this document itself.
    *   Stay informed about new threats, vulnerabilities, and security best practices relevant to your technology stack and CI/CD tools.
    *   Conduct regular security training for developers and operations staff.

By implementing these guidelines, you can significantly improve the security posture of your software development lifecycle. Remember that security is an ongoing process, not a one-time setup.
