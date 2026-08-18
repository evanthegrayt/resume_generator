from resume_generator.models import (
    Company,
    Contact,
    Education,
    Resume,
    Role,
    SkillRow,
    Variant,
    VariantText,
)

CONTACT = Contact(
    name="Evan Gray",
    location="Edmond, OK",
    phone="",
    email="",
    linkedin="linkedin.com/in/evanthegrayt",
    github="github.com/evanthegrayt",
)

VARIANTS = {
    "general": Variant(
        name="general",
        stem="evan-gray-resume-general",
        headline="Senior Software Engineer | Legacy Modernization, Backend Systems, and Product Delivery",
        summary=(
            "Senior Software Engineer focused on backend systems, object-oriented design, and product-minded legacy modernization. "
            "Known for joining stalled, high-risk software efforts, creating technical and product clarity, adding testing and delivery safeguards, "
            "and shipping maintainable releases across Ruby/Rails, .NET, React, Python/Django, SQL Server, and PostgreSQL environments. "
            "11+ years building production software and 20+ years across IT, systems, support, and software delivery."
        ),
    ),
    "rails": Variant(
        name="rails",
        stem="evan-gray-resume-rails",
        headline="Senior Software Engineer | Ruby/Rails, Legacy Modernization, and Product Delivery",
        summary=(
            "Senior Software Engineer focused on Ruby/Rails, object-oriented design, and product-minded legacy modernization. "
            "Known for joining stalled, high-risk software efforts, creating technical and product clarity, adding testing and delivery safeguards, "
            "and shipping maintainable releases. 11+ years building production software and 20+ years across IT, systems, support, and software "
            "delivery, with deep experience in Rails APIs, data-heavy workflows, stakeholder discovery, production support, and mentoring."
        ),
    ),
}


def skill_rows(variant):
    shared = [
        SkillRow("Languages", "Ruby, SQL, JavaScript/TypeScript, Python, PHP, C#, Shell Scripting, VimScript"),
        SkillRow("Frameworks", "Ruby on Rails 5-8, React, Hotwire/Turbo/Stimulus, Django, Laravel, .NET, Graphiti"),
    ]
    focused = [
        SkillRow("Rails", "ActiveJob, ActionCable, Devise, Pundit, CanCanCan, Sidekiq, Resque, Rake tasks, Bullet, RubyGems")
    ]
    general = [
        SkillRow("Backend", "Ruby/Rails, REST APIs, background jobs, Rake tasks, RubyGems, authorization, service/data modeling")
    ]
    return [
        *shared,
        *(focused if variant == "rails" else general),
        SkillRow("Data/APIs", "PostgreSQL, MySQL, SQL Server, Redis, Elasticsearch, MongoDB, GraphQL/Hasura, DBML/data modeling"),
        SkillRow("Cloud/DevOps", "AWS (S3, application hosting, logging), Docker, Vagrant, Git, GitHub, GitLab, Azure DevOps, CI/CD"),
        SkillRow("Testing", "RSpec, Minitest, Test::Unit, Jest, Cypress, PHPUnit, Bats, CI linting, smoke testing"),
        SkillRow("Security", "SOC 2 environments, PII/SSN data handling, role-based permissions, production data scrubbing"),
        SkillRow("Leadership", "architecture, mentoring, product ownership, Scrum, stakeholder discovery, RCA writing, AI-assisted development"),
    ]


EXPERIENCE = [
    Company(
        "Yolk Labs",
        "Austin, TX",
        [
            Role(
                "Senior Software Engineer, Remote Contract",
                "Jun. 2026 - Present",
                [
                    "Modernized a mature oil and gas platform by upgrading end-of-life React, Node.js, and .NET versions back to supported LTS releases, reducing technical debt and improving maintainability.",
                    "Took ownership of a stale web-app feature after more than a year of slow feedback cycles, led stakeholder/end-user discovery, and helped ship it within the first month.",
                    "Deliver full-stack enhancements across React, C#/.NET, and SQL Server while consolidating legacy Oracle-backed workflows into a centralized application.",
                    "Provide production support through a direct senior-user feedback channel, often turning urgent product feedback into same-hour fixes; introduce smoke testing to make legacy changes safer.",
                ],
            )
        ],
    ),
    Company(
        "Benefitbay",
        "Kansas City, MO",
        [
            Role(
                "Engineering Manager, Remote Full Time",
                "Mar. 2025 - Oct. 2025",
                [
                    "Managed delivery for an enterprise Ruby on Rails application serving 80,000+ users, leading 3 US engineers, 1 QA engineer, 3 EU contract engineers, and 1 EU DevOps engineer.",
                    "Owned feature-request translation with the Director of Engineering, introducing issue templates and scoped tickets that made PRs smaller, reviews more consistent, and releases more predictable.",
                    "Operated as a hands-on engineering/product leader across production support, on-call escalation, RCA writeups, bug fixes, PR review, architecture discussions, and product design meetings.",
                    "Led engineering standardization sessions around design patterns, AI-assisted development, and review practices to improve shared technical judgment across a distributed team.",
                    "Implemented user acceptance testing and AI-assisted development standards, bringing decision-maker feedback and approved agent/tool practices into delivery without bypassing engineering review.",
                ],
            )
        ],
    ),
    Company(
        "Mortgage Connect Risk Solutions",
        "Edmond, OK",
        [
            Role(
                "Senior Software Engineer, Product-Focused, Remote Full Time",
                "Apr. 2024 - Mar. 2025",
                [
                    "Served as technical/product lead for contractors replacing mission-critical C/Motif systems with modular Django, NuxtJS, and AWS applications spanning internal operations, reporting, and file workflows.",
                    "Decomposed tightly coupled legacy workflows into modular replacement paths, preserving accuracy across business-critical internal operations such as reporting, accounting, payroll, and file processing.",
                    "Migrated developers and internal stakeholders to Azure DevOps, Scrum, issue templates, PR guidelines, and code standards, reducing unreviewable change sets and improving first-release correctness.",
                    "Owned backlog priority, user stories, code quality, and delivery alignment for a client-facing Ruby on Rails application with 100,000+ users.",
                    "Partnered with executives and offshore contractors on architecture, roadmap alignment, RCA writeups, Scrum ceremonies, and post-launch technical ownership for PII-sensitive workflows.",
                ],
            )
        ],
    ),
    Company(
        "Public Strategies",
        "Oklahoma City, OK",
        [
            Role(
                "Product Software Engineer & Data Team Manager, Hybrid Full Time",
                "Apr. 2023 - Mar. 2024",
                [
                    "Promoted to manage delivery across a 6-person data/product group, including 4 direct reports, MS Dynamics engineers, a Power BI specialist, and PM/BA partners.",
                    "Took over an underused Microsoft Dynamics investment, introduced Scrum/discovery process, and enabled CRM adoption, custom application delivery, and migration of marketing workflows from Mailchimp.",
                    "Oversaw Rails and Microsoft Dynamics work for permission-sensitive participant data, CMS/CRM, reporting, event management, and custom applications supporting 3 programs and several thousand users.",
                ],
            ),
            Role(
                "Senior Software Engineer, Hybrid Full Time",
                "Aug. 2022 - Apr. 2023",
                [
                    VariantText(
                        "Took over a stalled participant mobile-app backend after roughly 2 years of slow progress, finished the API/database work, and supported release within 6 months.",
                        "Took over a stalled participant mobile-app backend after roughly 2 years of slow progress, finished the Rails API/database work, and supported release within 6 months.",
                    ),
                    "Delivered backend APIs and data models for participant engagement features including workshop schedules, attendance tracking, rewards, gas-card workflows, and program content.",
                    VariantText(
                        "Designed data architecture with DBML/dbdiagram.io, added CI/linting and test-readiness safeguards, and used Bullet to identify N+1 queries before refactoring data-heavy flows.",
                        "Designed Rails data architecture with DBML/dbdiagram.io, added CI/linting and test-readiness safeguards, and used Bullet to identify N+1 queries before refactoring data-heavy flows.",
                    ),
                    VariantText(
                        "Partnered with DevOps on application/AWS integration, including secrets, CI readiness, Rake tasks, data/schema dumps, imports, CSV seeding, and developer tooling.",
                        "Partnered with DevOps on Rails/AWS integration, including secrets, CI readiness, Rake tasks, data/schema dumps, imports, CSV seeding, and developer tooling.",
                    ),
                ],
            ),
        ],
    ),
    Company(
        "Weedmaps",
        "Irvine, CA",
        [
            Role(
                "Software Engineer III, Remote Full Time",
                "Feb. 2022 - Aug. 2022",
                [
                    "Supported ad campaign creation and management for a high-volume marketplace with 1,000,000+ active users.",
                    "Built a Graphiti REST adapter around a GraphQL/Hasura advertisement platform, allowing REST clients to consume ad-server CRUD operations through a safer, consistent API layer.",
                    "Unblocked deadline-risk Best of Weedmaps 2022 work by clearing campaign technical debt and making yearly winner/trophy data reusable across web and native experiences.",
                ],
            )
        ],
    ),
    Company(
        "Public Strategies",
        "Oklahoma City, OK",
        [
            Role(
                "Software Engineer, Hybrid Full Time",
                "Aug. 2019 - Feb. 2022",
                [
                    "Helped move a non-version-controlled PHP/SFTP production workflow into Laravel and then Ruby on Rails, eliminating direct production-file overwrites and improving maintainability.",
                    "Built Rails APIs, Rails admin interfaces, and React + TypeScript front ends for reporting, data visualization, event calendars, webinar/podcast content, and client-managed organizational profiles.",
                    "Built Planter as an internal Rails seeding/import framework for CSV-driven data setup, then extracted it into an open-source RubyGem.",
                ],
            )
        ],
    ),
    Company(
        "ADFITECH, Inc.",
        "Edmond, OK",
        [
            Role(
                "Desktop and Web Application Developer, Hybrid Full Time",
                "Sep. 2015 - Aug. 2019",
                [
                    "Built Ruby/GTK workflow applications for roughly 300 internal users, routing loan data, images, audit findings, and department handoffs through Ruleby-based business rules and Redis-backed processing.",
                    "Single-handedly rebuilt a rigid C-based loan selection process in Ruby, moving selection criteria into configuration and reducing the workflow from 3+ people to one part-time user.",
                    "Built Redis-backed background jobs for reports and asynchronous workflows; maintained legacy C/PHP systems and data scrubbers for PII/SSN-safe lower environments.",
                    "Trained junior developers in object-oriented Ruby, GitLab merge requests, command-line workflows, and common development practices; earlier roles included Jr. System Administrator, Technical Support, and Data/Image Import Specialist.",
                ],
            )
        ],
    ),
]

OPEN_SOURCE = [
    "Maintain 30+ documented, installable open-source projects at github.com/evanthegrayt, emphasizing developer productivity, automation, testing, and clear installation/usage documentation.",
    "Built Planter, a Rails seeding/import RubyGem extracted from production work, and cdc, a zsh/bash directory-jump plugin with tab completion and session history.",
    "Build and publish small developer tools, Vim plugins, shell utilities, and AI-agent workflow templates to reduce repetitive work and share practical patterns with other developers.",
]

EDUCATION = Education(
    school="University of Central Oklahoma",
    location="Edmond, OK",
    details="Studied Psychology",
)


def build_resume_data(variant):
    variant_config = VARIANTS[variant]
    return Resume(
        contact=CONTACT,
        variant=variant_config,
        skills=skill_rows(variant),
        experience=[company.resolve(variant) for company in EXPERIENCE],
        open_source=OPEN_SOURCE,
        education=EDUCATION,
    )
