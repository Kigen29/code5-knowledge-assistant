from __future__ import annotations

from pathlib import Path
from textwrap import wrap


ROOT = Path(__file__).resolve().parents[1]
POLICY_DIR = ROOT / "policies"
PAGE_WIDTH = 612
PAGE_HEIGHT = 792
LEFT = 54
TOP = 738
MAX_CHARS = 92
LINES_PER_PAGE = 48


PDFS = [
    {
        "filename": "11-code5-company-handbook.pdf",
        "title": "Code 5 Developers Company Handbook",
        "pages": 18,
        "sections": [
            ("Company Mission", "Code 5 Developers designs, builds, maintains, and improves software systems that help clients operate more efficiently and serve their users better."),
            ("Service Lines", "Core services include custom software development, systems development, platform maintenance, technical consulting, integrations, automation, DevOps, quality assurance, and ongoing support."),
            ("Delivery Principles", "Teams should communicate clearly, protect client trust, build maintainable systems, document decisions, and ship work that can be supported after launch."),
            ("Professional Standards", "Team members must use respectful communication, accurate reporting, careful handling of client information, and timely escalation when risks appear."),
            ("Client Trust", "Client trust is protected by reliable delivery, honest status reporting, secure engineering, and ownership of issues through resolution."),
        ],
    },
    {
        "filename": "12-software-project-playbook.pdf",
        "title": "Software Project Playbook",
        "pages": 20,
        "sections": [
            ("Project Intake", "Project intake captures business goals, user groups, existing systems, pain points, deadlines, budget boundaries, integrations, and decision makers."),
            ("Backlog Management", "Backlogs must show priorities, acceptance criteria, dependencies, estimates, risk notes, and client decisions that affect delivery."),
            ("Sprint Delivery", "Sprint delivery includes planning, implementation, review, testing, demo, and retrospective actions when the project uses an agile cadence."),
            ("Client Demo", "Demos should focus on working software, business outcomes, known limitations, decisions needed, and next delivery steps."),
            ("Release Closure", "Release closure confirms acceptance, deployment notes, support transition, open defects, documentation, and improvement backlog."),
        ],
    },
    {
        "filename": "13-systems-development-manual.pdf",
        "title": "Systems Development Manual",
        "pages": 18,
        "sections": [
            ("System Design", "System design must identify user roles, data flows, integrations, permission boundaries, scalability needs, reporting requirements, and operational constraints."),
            ("API Design", "APIs should use clear resource names, predictable status codes, validation errors, authentication requirements, versioning rules, and example payloads."),
            ("Integration Design", "Integrations must document ownership, credentials, rate limits, retries, failure handling, logging, data mapping, and reconciliation steps."),
            ("Data Modeling", "Data models should protect integrity, support reporting, avoid unnecessary duplication, and include migration plans for production changes."),
            ("Maintainability", "Systems should be designed so another Code 5 Developers engineer can understand, run, troubleshoot, and extend them."),
        ],
    },
    {
        "filename": "14-maintenance-operations-manual.pdf",
        "title": "Maintenance Operations Manual",
        "pages": 18,
        "sections": [
            ("Maintenance Scope", "Maintenance may include monitoring, dependency updates, bug fixes, performance tuning, backup checks, compatibility updates, and small enhancements."),
            ("Support Queue", "Support queues must be triaged by severity, client impact, contractual response target, affected system, and required technical owner."),
            ("Patch Windows", "High-risk patches should be scheduled during agreed maintenance windows and communicated before execution."),
            ("Handover Checklist", "Maintenance handover includes architecture notes, runbooks, credentials location, deployment steps, support contacts, known issues, and monitoring links."),
            ("Monthly Review", "Managed support projects should receive monthly review of incidents, completed maintenance, open risks, upcoming renewals, and recommended improvements."),
        ],
    },
    {
        "filename": "15-devops-cloud-runbook.pdf",
        "title": "DevOps and Cloud Runbook",
        "pages": 16,
        "sections": [
            ("Cloud Accounts", "Cloud accounts must identify owner, billing contact, environments, access groups, regions, backup approach, and escalation contacts."),
            ("Deployment Pipeline", "Deployment pipelines should build, test, package, migrate, deploy, and verify applications with clear failure messages."),
            ("Secrets Management", "Secrets belong in approved secret stores and must not be committed, emailed, logged, or pasted into public tools."),
            ("Observability", "Production systems need health checks, logs, alerts, metrics, and clear ownership for alert response."),
            ("Disaster Recovery", "Recovery plans must identify backup frequency, restore steps, recovery time expectations, and test schedule."),
        ],
    },
    {
        "filename": "16-quality-assurance-handbook.pdf",
        "title": "Quality Assurance Handbook",
        "pages": 16,
        "sections": [
            ("QA Strategy", "Quality strategy begins with risk. The team identifies critical workflows, permissions, integrations, data changes, browsers, devices, and launch constraints."),
            ("Test Cases", "Test cases should include preconditions, steps, expected results, test data, user role, environment, and pass or fail status."),
            ("Regression Testing", "Regression testing checks that existing workflows still work after new features, fixes, dependency updates, or infrastructure changes."),
            ("Accessibility", "Client-facing interfaces should be reviewed for keyboard access, contrast, labels, focus states, readable errors, and responsive layout."),
            ("Release Signoff", "Release signoff confirms test results, open defects, accepted risks, deployment plan, rollback plan, and approval owner."),
        ],
    },
    {
        "filename": "17-security-and-data-protection-manual.pdf",
        "title": "Security and Data Protection Manual",
        "pages": 18,
        "sections": [
            ("Secure Access", "Repository, cloud, database, and admin access must follow least privilege and be removed when project need ends."),
            ("Client Data", "Client data must be minimized, protected, retained only as long as needed, and deleted when the approved purpose ends."),
            ("Security Reviews", "Security reviews are required for authentication, payment flows, sensitive data, admin features, public APIs, and third-party integrations."),
            ("Vulnerability Response", "Critical vulnerabilities must be triaged immediately and remediated or mitigated as quickly as the client environment allows."),
            ("Incident Evidence", "During security incidents, teams preserve logs, screenshots, commits, deployment records, and communication timelines."),
        ],
    },
    {
        "filename": "18-client-handover-and-training-guide.pdf",
        "title": "Client Handover and Training Guide",
        "pages": 14,
        "sections": [
            ("Handover Package", "The handover package includes system overview, repository links, deployment notes, admin guide, support process, credentials location, and known limitations."),
            ("Training Sessions", "Training should demonstrate key workflows, role permissions, common errors, reporting, support requests, and operational responsibilities."),
            ("Admin Guide", "Admin guides explain user management, configuration, content updates, data export, backups, and escalation paths."),
            ("Support Transition", "Support transition identifies who receives incidents, expected response times, maintenance scope, and how change requests are handled."),
            ("Client Acceptance", "Client acceptance confirms that required documents, training, production access, and support arrangements are complete."),
        ],
    },
    {
        "filename": "19-ai-automation-and-integration-guide.pdf",
        "title": "AI Automation and Integration Guide",
        "pages": 14,
        "sections": [
            ("Automation Fit", "Automation is recommended when work is repetitive, rules are clear, data quality is sufficient, and the client can define success criteria."),
            ("AI Use", "AI features must include human review where outcomes affect clients, payments, legal obligations, security, or sensitive decisions."),
            ("Integration Safety", "Integrations must handle retries, idempotency, rate limits, partial failure, monitoring, and reconciliation."),
            ("Data Boundaries", "AI and automation systems must respect client data boundaries and avoid sending sensitive data to unapproved providers."),
            ("Evaluation", "Automation and AI work should be evaluated for accuracy, latency, failure rate, user acceptance, and operational cost."),
        ],
    },
    {
        "filename": "20-internal-operations-and-growth-plan.pdf",
        "title": "Internal Operations and Growth Plan",
        "pages": 14,
        "sections": [
            ("Operating Rhythm", "Code 5 Developers uses regular planning, delivery reviews, support reviews, finance checks, and technical learning sessions to keep operations predictable."),
            ("Knowledge Sharing", "Teams should document reusable patterns, lessons learned, client constraints, deployment notes, and troubleshooting guides."),
            ("Capacity Planning", "Leads review workload, project deadlines, support obligations, skills, and hiring needs before accepting major new commitments."),
            ("Continuous Improvement", "Retrospectives identify process gaps, quality issues, tooling improvements, and training needs."),
            ("Growth Areas", "Growth priorities include software products, systems modernization, cloud operations, AI automation, cybersecurity, and long-term maintenance partnerships."),
        ],
    },
]


def pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def make_lines(title: str, sections: list[tuple[str, str]], page_number: int) -> list[str]:
    lines = [title, f"Code 5 Developers - Page {page_number}", ""]
    for heading, body in sections:
        lines.append(heading)
        expanded = (
            f"{body} This page is part of the Code 5 Developers knowledge library and supports "
            f"software development, systems development, maintenance, and technology operations."
        )
        lines.extend(wrap(expanded, width=MAX_CHARS))
        lines.append("")
    while len(lines) < LINES_PER_PAGE:
        lines.extend(
            wrap(
                "Operational note: use the documented process, keep client decisions visible, protect client data, "
                "and escalate delivery, security, or production risks before they become client-impacting issues.",
                width=MAX_CHARS,
            )
        )
        lines.append("")
    return lines[:LINES_PER_PAGE]


def content_stream(lines: list[str]) -> bytes:
    commands = ["BT", "/F1 10 Tf", f"{LEFT} {TOP} Td", "14 TL"]
    for index, line in enumerate(lines):
        if index:
            commands.append("T*")
        commands.append(f"({pdf_escape(line)}) Tj")
    commands.append("ET")
    return ("\n".join(commands) + "\n").encode("latin-1")


def write_pdf(path: Path, title: str, sections: list[tuple[str, str]], pages: int) -> None:
    objects: list[bytes] = []
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    page_refs = " ".join(f"{3 + (page * 2)} 0 R" for page in range(pages))
    objects.append(f"<< /Type /Pages /Kids [{page_refs}] /Count {pages} >>".encode("latin-1"))

    for page in range(pages):
        page_obj = 3 + page * 2
        stream_obj = page_obj + 1
        lines = make_lines(title, rotate_sections(sections, page), page + 1)
        stream = content_stream(lines)
        objects.append(
            (
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] "
                f"/Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >> "
                f"/Contents {stream_obj} 0 R >>"
            ).encode("latin-1")
        )
        objects.append(
            f"<< /Length {len(stream)} >>\nstream\n".encode("latin-1")
            + stream
            + b"endstream"
        )

    pdf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{number} 0 obj\n".encode("latin-1"))
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")
    xref_start = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("latin-1"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("latin-1"))
    pdf.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_start}\n%%EOF\n"
        ).encode("latin-1")
    )
    path.write_bytes(bytes(pdf))


def rotate_sections(sections: list[tuple[str, str]], page: int) -> list[tuple[str, str]]:
    shift = page % len(sections)
    return sections[shift:] + sections[:shift]


def main() -> None:
    POLICY_DIR.mkdir(exist_ok=True)
    for old_pdf in POLICY_DIR.glob("*.pdf"):
        old_pdf.unlink()
    for spec in PDFS:
        path = POLICY_DIR / spec["filename"]
        write_pdf(path, spec["title"], spec["sections"], spec["pages"])
        print(f"Wrote {path.relative_to(ROOT)} ({spec['pages']} pages)")


if __name__ == "__main__":
    main()
