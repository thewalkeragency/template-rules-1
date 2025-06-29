# Product Requirements Document: [Feature/Product Name]

**Version:** 1.0
**Last Updated:** YYYY-MM-DD
**Author/Owner:** {{author_name}}
**Status:** Draft | In Review | Approved

## 1. Introduction & Purpose

*   **What is this product/feature?** (High-level overview)
*   **What problem does it solve for the user?**
*   **What are the primary goals and objectives?**
*   **Who is the target audience?**

## 2. Goals & Objectives

*   **Business Goals:** (e.g., Increase user engagement by X%, Reduce support tickets by Y%)
*   **User Goals:** (e.g., Allow users to easily achieve Z, Simplify process A for users)
*   **Success Metrics:** (How will we measure success? e.g., Daily active users, task completion rate, conversion rate)

## 3. Target Users & Use Cases

*   **User Personas:** (Brief description of key user types, if applicable)
    *   *Persona 1:* Description, needs, pain points.
    *   *Persona 2:* Description, needs, pain points.
*   **Key Use Cases / User Stories:** (Describe how users will interact with the feature)
    *   **UC-001:** As a [type of user], I want to [perform an action] so that [I can achieve a goal].
        *   *Acceptance Criteria:* (Bullet points of conditions that must be met for the story to be complete)
    *   **UC-002:** ...

## 4. Requirements

### 4.1. Functional Requirements

*   (Detailed list of what the system must do. Number them FR-001, FR-002, etc.)
*   **FR-001:** The system shall allow users to register for an account using email and password.
*   **FR-002:** The system shall validate password strength according to [specific criteria].
*   ...

### 4.2. Non-Functional Requirements

*   **NFR-001 (Performance):** The [specific action, e.g., page load, API response] must complete within X seconds under Y concurrent users.
*   **NFR-002 (Scalability):** The system must be able to handle Z [requests/users/data volume] per [time unit] without degradation.
*   **NFR-003 (Availability):** The system shall have an uptime of X.XX%.
*   **NFR-004 (Security):**
    *   All sensitive data must be encrypted at rest and in transit.
    *   The system must comply with [specific security standards, e.g., OWASP Top 10, internal security rules defined in `.ai_rules/`].
    *   Authentication must use [specific mechanism, e.g., OAuth 2.0, JWT].
*   **NFR-005 (Usability):** The feature must be intuitive and require minimal training for target users.
*   **NFR-006 (Accessibility):** The UI must adhere to WCAG 2.1 Level AA guidelines.
*   **NFR-007 (Maintainability):** Code must follow guidelines in `.ai_rules/rules/` and be well-documented.
*   ...

### 4.3. Data Requirements (If applicable)

*   What data needs to be stored?
*   Data formats, schemas (link to data models if separate).
*   Data retention policies.

### 4.4. Integration Requirements (If applicable)

*   Interaction with other systems, APIs (internal or external).
*   Data exchange formats.

## 5. Design & UX Considerations (Optional - Link to separate design docs if extensive)

*   High-level wireframes or mockups (or links to Figma, Sketch, etc.).
*   Key UI/UX principles to follow.
*   Branding guidelines.

## 6. Assumptions & Dependencies

*   **Assumptions:** (Things believed to be true that might impact the project if false)
*   **Dependencies:** (External factors, teams, or technologies this project relies on)

## 7. Out of Scope / Future Considerations

*   Features explicitly not being built in this version.
*   Potential future enhancements.

## 8. Open Questions

*   (List any unresolved questions that need answers before or during development)

## 9. Revision History

| Version | Date       | Author          | Changes                                      |
|---------|------------|-----------------|----------------------------------------------|
| 0.1     | YYYY-MM-DD | {{author_name}} | Initial Draft                                |
| 1.0     | YYYY-MM-DD | {{author_name}} | Approved version after review                |

---

**Guidance for AI Agents (especially Memex):**
*   This template should be used as a starting point when a new Product Requirements Document is needed.
*   The "Architect Persona" (Memex) is typically responsible for ensuring a PRD exists and is sufficiently detailed before major development tasks are initiated.
*   Refer to this PRD when decomposing features into Tasks, Sub-tasks, and Prompts as per the Universal Workflow.
*   Non-Functional Requirements, especially security, should reference the rules defined in the `.ai_rules/` directory.
