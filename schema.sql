CREATE TABLE IF NOT EXISTS research_projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    full_title TEXT NOT NULL,
    display_order INTEGER
);

CREATE TABLE IF NOT EXISTS programming_projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    full_title TEXT NOT NULL,
    display_order INTEGER
);

CREATE TABLE IF NOT EXISTS contact (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    question TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS site_profile (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    name TEXT NOT NULL,
    headline TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    location TEXT NOT NULL,
    introduction TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS project_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section TEXT NOT NULL,
    project_id INTEGER NOT NULL,
    image_path TEXT NOT NULL,
    caption TEXT DEFAULT '',
    sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_project_images_section_project
ON project_images(section, project_id, sort_order, id);

-- ponytail: seed only fresh DBs; admin-managed DBs keep their own project rows.
INSERT INTO research_projects (id, title, content, full_title, display_order)
SELECT * FROM (
    SELECT 1, 'Binder Jetting', 'Process development work on binder jetting for metal additive manufacturing. I studied how powder behaviour, binder flow, spreading, and particle movement affect process stability and part quality. The work connects powder scale mechanisms with practical build outcomes.', 'Binder jetting process development', 1
    UNION ALL SELECT 2, 'Powder Spreading', 'Powder spreading research for metal additive manufacturing. I studied how particle flow, layer uniformity, and segregation affect the next build step. The work helps explain why a stable recoating process is important before printing starts.', 'Powder spreading in additive manufacturing', 2
    UNION ALL SELECT 3, 'Laser Powder-Bed Fusion', 'Laser powder-bed fusion research on process parameters and defect formation. I focused on how melt pool behaviour, spatter, and process settings affect build stability. The work supports better parameter selection for metal parts.', 'Laser powder-bed fusion process research', 3
    UNION ALL SELECT 4, 'Spatter Mitigation', 'Research on spatter mitigation and parameter tuning in laser powder-bed fusion. I studied how process settings change spatter behaviour and how that affects build stability. The goal was to reduce defects without treating the result as a one-off lab case.', 'Spatter mitigation and process optimisation', 4
    UNION ALL SELECT 5, 'Filament-Deposition Modelling', 'Filament-deposition modelling work for additive manufacturing. I studied how material behaviour, geometry control, and deposition conditions affect repeatability. The work links simulation and process understanding with more predictable part quality.', 'Filament-deposition modelling', 5
    UNION ALL SELECT 6, 'Injection-Mould Tooling', 'Injection-mould tooling work using additive manufacturing. I looked at how tool design, manufacturing route, and production constraints interact. The work is useful for cases where lab fabrication has to meet practical tooling needs.', 'Injection-mould tooling with additive manufacturing', 6
    UNION ALL SELECT 7, 'Acoustic Signal Emissions', 'In-situ acoustic-emission sensing for process monitoring. I built workflows that capture process signals during manufacturing and connect them with changes in process dynamics. The work supports faster review of quality issues during production.', 'Acoustic-emission sensing for process monitoring', 7
    UNION ALL SELECT 8, 'Final-Year Project Tutoring', 'Supervision of undergraduate final-year projects. I guide students on experimental design, data analysis, and technical communication. This work keeps the research process practical and helps students turn experiments into clear engineering conclusions.', 'Final-year project tutoring', 8
) WHERE NOT EXISTS (SELECT 1 FROM research_projects);

INSERT INTO programming_projects (id, title, content, full_title, display_order)
SELECT * FROM (
    SELECT 1, 'Multi-Factor Stock Screener', 'Multi-factor stock screener for public-company research. The workflow combines Refinitiv fundamentals with sector-specific factor weights so I can create shortlists for deeper review. It is meant to support research selection, not replace company analysis.', 'Multi-Factor Stock Screener', 1
    UNION ALL SELECT 2, 'Agentic Company-Analysis Workflow', 'Company analysis workflow that turns filings, reports, and transcripts into structured research notes. It uses LLM-assisted extraction and review to prepare summaries, themes, and questions for diligence. The output helps make a messy source set easier to audit.', 'Agentic Company-Analysis Workflow', 2
    UNION ALL SELECT 3, 'Real-Time News Intelligence Engine', 'News intelligence workflow for portfolio and watchlist monitoring. It scores headlines, groups related items, and ranks the items that need review first. The goal is to reduce noise while keeping the original news source visible.', 'Real-Time News Intelligence Engine', 3
    UNION ALL SELECT 4, 'Interactive Macro Dashboard', 'Interactive macro dashboard built in Python Dash. It lets the user filter countries and time series so macro indicators can be reviewed before an allocation or sector discussion. The dashboard is a research context tool rather than a trading signal.', 'Interactive Macro Dashboard', 4
    UNION ALL SELECT 5, 'Systematic Trading-Signal Framework', 'Research framework for rule-based trading signals. It supports experiments on signal generation, evaluation, and execution logic. I use it as a sandbox for testing ideas before deciding whether a signal is worth deeper work.', 'Systematic Trading-Signal Framework', 5
    UNION ALL SELECT 6, 'Web-Scraping Pipelines', 'Web-scraping pipelines for collecting research data from public web sources. The work covers repeatable extraction, cleaning, and storage so the same data can be checked again later. It supports monitoring tasks where manual collection would be slow.', 'Web-scraping pipelines', 6
    UNION ALL SELECT 7, 'Account-Tracking Module', 'Account-tracking module for personal portfolio records. It stores account activity and P&L in a structured way so performance can be reviewed over time. The module keeps tracking separate from research notes and external data collection.', 'Account-tracking module', 7
) WHERE NOT EXISTS (SELECT 1 FROM programming_projects);

UPDATE research_projects
SET content = CASE id
    WHEN 1 THEN 'Process development work on binder jetting for metal additive manufacturing. I studied how powder behaviour, binder flow, spreading, and particle movement affect process stability and part quality. The work connects powder scale mechanisms with practical build outcomes.'
    WHEN 2 THEN 'Powder spreading research for metal additive manufacturing. I studied how particle flow, layer uniformity, and segregation affect the next build step. The work helps explain why a stable recoating process is important before printing starts.'
    WHEN 3 THEN 'Laser powder-bed fusion research on process parameters and defect formation. I focused on how melt pool behaviour, spatter, and process settings affect build stability. The work supports better parameter selection for metal parts.'
    WHEN 4 THEN 'Research on spatter mitigation and parameter tuning in laser powder-bed fusion. I studied how process settings change spatter behaviour and how that affects build stability. The goal was to reduce defects without treating the result as a one-off lab case.'
    WHEN 5 THEN 'Filament-deposition modelling work for additive manufacturing. I studied how material behaviour, geometry control, and deposition conditions affect repeatability. The work links simulation and process understanding with more predictable part quality.'
    WHEN 6 THEN 'Injection-mould tooling work using additive manufacturing. I looked at how tool design, manufacturing route, and production constraints interact. The work is useful for cases where lab fabrication has to meet practical tooling needs.'
    WHEN 7 THEN 'In-situ acoustic-emission sensing for process monitoring. I built workflows that capture process signals during manufacturing and connect them with changes in process dynamics. The work supports faster review of quality issues during production.'
    WHEN 8 THEN 'Supervision of undergraduate final-year projects. I guide students on experimental design, data analysis, and technical communication. This work keeps the research process practical and helps students turn experiments into clear engineering conclusions.'
END
WHERE (id, content) IN (
    VALUES
    (1, 'Process-development work on binder jetting, linking powder behaviour, process stability, and part quality for metal additive manufacturing.'),
    (2, 'Powder spreading research focused on flow behaviour, layer uniformity, and the process physics that affect downstream build quality.'),
    (3, 'Laser powder-bed fusion work covering process parameters, defect formation, and practical routes to more stable metal additive manufacturing.'),
    (4, 'Research on spatter mitigation and parameter tuning, focused on process robustness rather than isolated lab demonstrations.'),
    (5, 'Filament-deposition modelling work connecting material behaviour, geometry control, and process repeatability.'),
    (6, 'Injection-mould tooling work that connects additive manufacturing, tooling design, and practical production constraints.'),
    (7, 'In-situ acoustic-emission sensing workflows for monitoring process dynamics at production speed and supporting quality assurance.'),
    (8, 'Supervision of undergraduate capstones with emphasis on experimental design, data analysis, and technical communication.')
);

UPDATE programming_projects
SET content = CASE id
    WHEN 1 THEN 'Multi-factor stock screener for public-company research. The workflow combines Refinitiv fundamentals with sector-specific factor weights so I can create shortlists for deeper review. It is meant to support research selection, not replace company analysis.'
    WHEN 2 THEN 'Company analysis workflow that turns filings, reports, and transcripts into structured research notes. It uses LLM-assisted extraction and review to prepare summaries, themes, and questions for diligence. The output helps make a messy source set easier to audit.'
    WHEN 3 THEN 'News intelligence workflow for portfolio and watchlist monitoring. It scores headlines, groups related items, and ranks the items that need review first. The goal is to reduce noise while keeping the original news source visible.'
    WHEN 4 THEN 'Interactive macro dashboard built in Python Dash. It lets the user filter countries and time series so macro indicators can be reviewed before an allocation or sector discussion. The dashboard is a research context tool rather than a trading signal.'
    WHEN 5 THEN 'Research framework for rule-based trading signals. It supports experiments on signal generation, evaluation, and execution logic. I use it as a sandbox for testing ideas before deciding whether a signal is worth deeper work.'
    WHEN 6 THEN 'Web-scraping pipelines for collecting research data from public web sources. The work covers repeatable extraction, cleaning, and storage so the same data can be checked again later. It supports monitoring tasks where manual collection would be slow.'
    WHEN 7 THEN 'Account-tracking module for personal portfolio records. It stores account activity and P&L in a structured way so performance can be reviewed over time. The module keeps tracking separate from research notes and external data collection.'
END
WHERE (id, content) IN (
    VALUES
    (1, 'Integrates Refinitiv fundamentals with sector-specific factor weightings and automated ranking logic to produce dynamic shortlists for deeper fundamental work.'),
    (2, 'Converts filings, reports, and transcripts into structured Markdown and agent-assisted diligence outputs, including summarisation, thematic synthesis, and investor-grade Q&A.'),
    (3, 'Combines sentiment scoring and LLM-assisted ranking to surface the highest-signal headlines for portfolio and watchlist names.'),
    (4, 'Built in Python Dash to visualise macro indicators with country and time-series filters, helping frame allocation decisions with current context.'),
    (5, 'Research sandbox for rule-based alpha generation, signal evaluation, and execution-logic testing.'),
    (6, 'Custom web-scraping pipelines that automate data collection for research, monitoring, and repeatable analysis workflows.'),
    (7, 'A secure account-tracking module for personal P&L monitoring and structured investment workflow support.')
);
