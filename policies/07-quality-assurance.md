# Quality Assurance Policy

## Purpose
Quality assurance at Code 5 Developers ensures software is useful, reliable, secure, accessible, and ready for client use. QA is a shared responsibility between engineers, project leads, designers, and client stakeholders.

## Test Planning
Each project must identify critical workflows, user roles, integrations, data scenarios, permissions, and acceptance criteria before release. The test plan should focus on the highest business and technical risks.

## Automated Testing
Automated tests are required for important business rules, API contracts, authentication, authorization, payment flows, data processing, and critical user journeys. Test coverage should expand when a defect reveals a missing safety check.

## Manual Testing
Manual testing should validate usability, layout, copy, cross-browser behavior, mobile responsiveness, edge cases, and workflow fit. Testers should record steps, environment, expected result, actual result, screenshots, and severity.

## User Acceptance Testing
Client user acceptance testing is required before major launches. The project lead provides a release summary, test accounts, known limitations, and a clear approval request. UAT approval must be recorded before production release.

## Defect Severity
Critical defects block release when they prevent core workflows, expose data, break authentication, corrupt data, or create major financial or reputational risk. Minor defects may be scheduled after launch if the client accepts the risk.

## Release Readiness
A release is ready when critical tests pass, open defects are reviewed, deployment steps are documented, rollback is understood, monitoring is prepared, and the client or release owner gives approval.

