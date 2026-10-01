import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Skip headers/footers on page 1 (Cover / Title)
        if self._pageNumber > 1:
            # Header
            self.drawString(54, 750, "EventHub — System Problem Statement & Project Charter")
            self.drawRightString(558, 750, "SLIIT SE2020 Assignment")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.75)
            self.line(54, 742, 558, 742)

            # Footer
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(558, 40, page_text)
            self.drawString(54, 40, "Confidential — Sri Lanka Institute of Information Technology (SLIIT)")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.75)
            self.line(54, 52, 558, 52)

        self.restoreState()

def create_problem_statement_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    PRIMARY = colors.HexColor("#4F46E5")     # Indigo
    DARK = colors.HexColor("#0F172A")        # Slate 900
    TEXT_COLOR = colors.HexColor("#334155")  # Slate 700
    LIGHT_BG = colors.HexColor("#F8FAFC")    # Slate 50
    BORDER_COLOR = colors.HexColor("#E2E8F0")
    ACCENT_GREEN = colors.HexColor("#059669")
    ACCENT_RED = colors.HexColor("#DC2626")

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=DARK,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=PRIMARY,
        spaceAfter=14
    )

    meta_label = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=DARK
    )

    meta_val = ParagraphStyle(
        'MetaVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=TEXT_COLOR
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=DARK,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyMain',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=TEXT_COLOR,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletMain',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=TEXT_COLOR,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3
    )

    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=14,
        textColor=DARK
    )

    table_header = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    table_cell = ParagraphStyle(
        'TC',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=TEXT_COLOR
    )

    table_cell_bold = ParagraphStyle(
        'TCB',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=DARK
    )

    story = []

    # ==========================
    # TITLE & METADATA SECTION
    # ==========================
    story.append(Spacer(1, 10))
    story.append(Paragraph("PROJECT PROBLEM STATEMENT & CHARTER", subtitle_style))
    story.append(Paragraph("EventHub: Campus & Community Event Management Platform", title_style))
    story.append(Paragraph("A Full-Stack Event Orchestration, Digital Ticketing, and Concurrency-Safe Reservation System", body_style))
    story.append(Spacer(1, 8))

    # Meta Table
    meta_data = [
        [Paragraph("Module:", meta_label), Paragraph("Web & Mobile Application Technologies (SE2020)", meta_val),
         Paragraph("Institution:", meta_label), Paragraph("Sri Lanka Institute of Information Technology (SLIIT)", meta_val)],
        [Paragraph("Target Architecture:", meta_label), Paragraph("React Native / Expo Web + Node.js + MongoDB Atlas", meta_val),
         Paragraph("Document Status:", meta_label), Paragraph("Final Academic Release (v1.0)", meta_val)],
        [Paragraph("Author:", meta_label), Paragraph("lakshan (SE2020 Student Developer)", meta_val),
         Paragraph("Academic Year:", meta_label), Paragraph("2026/2027", meta_val)]
    ]
    meta_table = Table(meta_data, colWidths=[80, 172, 85, 167])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 0.75, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # ==========================
    # 1. EXECUTIVE SUMMARY
    # ==========================
    story.append(Paragraph("1. Executive Summary", h1_style))
    exec_text = (
        "In contemporary tertiary academic institutions and community ecosystems, extracurricular, professional, "
        "and technical events serve as crucial catalysts for student growth and collaborative networking. However, "
        "the logistical coordination of campus events remains plagued by decentralized communication channels, manual "
        "ticket issuance, and fragmented administrative oversight. <b>EventHub</b> is an engineering response to these "
        "systemic inefficiencies. By combining an intuitive React Native mobile and web client with a secure, concurrency-controlled "
        "RESTful API powered by Node.js, Express, and MongoDB Atlas, EventHub consolidates event discovery, real-time "
        "capacity allocation, and digital ticketing into a single, unified enterprise ecosystem."
    )
    story.append(Paragraph(exec_text, body_style))
    story.append(Spacer(1, 10))

    # ==========================
    # 2. BACKGROUND & CONTEXT
    # ==========================
    story.append(Paragraph("2. Background & Industry Context", h1_style))
    bg_text = (
        "Educational campuses regularly host conferences, hackathons, guest lectures, cultural concerts, and academic "
        "workshops. Conventionally, organizers rely on disparate tools: social media channels for announcements, "
        "generic survey forms for participant registration, and manual physical check-ins on paper rosters. "
        "While seemingly simple, this disjointed workflow fails rapidly when participant interest scales beyond "
        "a few dozen individuals. There is no automated synchronization between the number of available physical seats "
        "and inbound booking requests, resulting in administrative chaos, venue fire-code violations, and severe student frustration."
    )
    story.append(Paragraph(bg_text, body_style))
    story.append(Spacer(1, 10))

    # ==========================
    # 3. DETAILED PROBLEM STATEMENT
    # ==========================
    story.append(Paragraph("3. Detailed Problem Statement", h1_style))
    intro_problem = (
        "Empirical analysis of existing campus event workflows reveals four principal failure points that hinder operational "
        "effectiveness and degrade user experience:"
    )
    story.append(Paragraph(intro_problem, body_style))

    story.append(Paragraph("3.1 Information Silos & Fragmented Discovery", h2_style))
    p1 = (
        "• <b>Lack of a Centralized Repository:</b> Event notices are scattered across social media feeds, chat groups, and physical "
        "corkboards. Prospective attendees frequently miss registration deadlines or fail to discover events relevant to their career goals.<br/>"
        "• <b>Static and Non-Interactive Catalogs:</b> Existing promotional mechanisms do not provide category filtering, search capabilities, "
        "or dynamic calendar timeline alignment, creating high discovery friction."
    )
    story.append(Paragraph(p1, bullet_style))

    story.append(Paragraph("3.2 Inventory Race Conditions & Overbooking Hazards", h2_style))
    p2 = (
        "• <b>Uncontrolled Concurrent Submissions:</b> When high-demand events open registration, hundreds of users apply simultaneously. "
        "Without strict atomic inventory counters, registration forms continue accepting submissions long after venue capacity is exceeded.<br/>"
        "• <b>Physical Safety & Venue Compliance:</b> Overbooked venues force organizers to either deny entry to registered attendees at the door "
        "or breach university occupational safety regulations by packing lecture halls beyond capacity."
    )
    story.append(Paragraph(p2, bullet_style))

    story.append(Paragraph("3.3 Paper-Based Inefficiencies & Fraud Susceptibility", h2_style))
    p3 = (
        "• <b>High Ecological & Monetary Cost:</b> Printing hundreds of paper ticket stubs or wristbands consumes financial resources and "
        "generates unneeded paper waste for short-duration events.<br/>"
        "• <b>Counterfeit Vulnerabilities:</b> Paper passes lack cryptographic validation or digital tracking, making them prone to duplication, "
        "loss, or unauthorized transfer without organizer knowledge."
    )
    story.append(Paragraph(p3, bullet_style))

    story.append(Paragraph("3.4 Absence of Self-Service Cancellation & Capacity Recirculation", h2_style))
    p4 = (
        "• <b>Ghost Bookings:</b> A significant percentage of attendees who register are subsequently unable to attend. In existing systems, "
        "there is no self-service mechanism for attendees to cancel a booking.<br/>"
        "• <b>Permanent Capacity Lock:</b> Unattended tickets remain permanently allocated in spreadsheets, blocking motivated attendees "
        "on waiting lists from claiming valid vacant seats."
    )
    story.append(Paragraph(p4, bullet_style))
    story.append(Spacer(1, 10))

    # ==========================
    # 4. THE PROPOSED SOLUTION
    # ==========================
    story.append(Paragraph("4. The Proposed Solution: EventHub Architecture", h1_style))
    sol_text = (
        "<b>EventHub</b> addresses each identified challenge through an integrated, cloud-native software architecture:"
    )
    story.append(Paragraph(sol_text, body_style))

    # Solution Callout Box
    sol_points = [
        "<b>1. Unified Event Discovery Portal:</b> A sleek, category-driven mobile and web interface enabling instantaneous search and filtering across Tech, Music, Workshops, Sports, and Business events.",
        "<b>2. Atomic Seat Decrement Logic:</b> An ACID-compliant reservation engine that dynamically checks <code>tickets &le; availableSeats</code> and decrements seat inventory atomically during transactions, guaranteeing 0% overbooking.",
        "<b>3. Automated Seat Restoration:</b> One-tap booking cancellations that instantaneously restore reserved seats to the public inventory, eliminating ghost bookings.",
        "<b>4. Digital Ticket Pass Generation:</b> Generation of interactive, authenticated digital passes containing booking reference IDs, user credentials, and event metadata directly within the attendee's personal wallet.",
        "<b>5. Creator Authorization Engine:</b> Granular role-based controls allowing event creators to modify event parameters or safely cancel events while preventing unauthorized administrative tampering."
    ]
    for sp in sol_points:
        story.append(Paragraph(f"• {sp}", bullet_style))

    story.append(Spacer(1, 10))

    # ==========================
    # 5. SMART OBJECTIVES TABLE
    # ==========================
    story.append(Paragraph("5. Project Objectives (SMART Criteria)", h1_style))
    
    obj_data = [
        [Paragraph("Objective", table_header), Paragraph("Target Metric", table_header), Paragraph("SMART Alignment", table_header)],
        [
            Paragraph("<b>Eliminate Overbooking</b>", table_cell_bold),
            Paragraph("0% overbooking rate across all concurrent booking operations", table_cell),
            Paragraph("Specific & Measurable through server-side capacity checks and atomic reservation locks.", table_cell)
        ],
        [
            Paragraph("<b>Sub-Second Response</b>", table_cell_bold),
            Paragraph("API response time &lt; 500ms for event browsing and bookings", table_cell),
            Paragraph("Achievable via optimized MongoDB indexing and lean JSON payloads.", table_cell)
        ],
        [
            Paragraph("<b>Paperless Operations</b>", table_cell_bold),
            Paragraph("100% digital pass delivery on mobile/web profiles", table_cell),
            Paragraph("Relevant to modern sustainability standards and instant user gratification.", table_cell)
        ],
        [
            Paragraph("<b>Self-Service Workflow</b>", table_cell_bold),
            Paragraph("&lt; 5 seconds to cancel and automatically restore seat capacity", table_cell),
            Paragraph("Time-bound, automated database updates on state changes.", table_cell)
        ],
        [
            Paragraph("<b>Cross-Platform Reach</b>", table_cell_bold),
            Paragraph("Single unified codebase running on Android, iOS, and Web", table_cell),
            Paragraph("Realized through React Native and Expo web bundler architecture.", table_cell)
        ]
    ]

    obj_table = Table(obj_data, colWidths=[120, 184, 200])
    obj_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('BOX', (0,0), (-1,-1), 0.75, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(obj_table)
    story.append(Spacer(1, 14))

    # ==========================
    # 6. STAKEHOLDER & USER PERSONAS
    # ==========================
    story.append(Paragraph("6. Stakeholder & Target Audience Analysis", h1_style))
    stake_text = (
        "The system serves three primary user personas, each with distinct interaction patterns:"
    )
    story.append(Paragraph(stake_text, body_style))

    story.append(Paragraph("• <b>Student Attendees (Consumers):</b> Seek effortless event discovery, transparent seat availability counts, frictionless 1-tap bookings, and easy access to digital ticket passes without printing requirements.", bullet_style))
    story.append(Paragraph("• <b>Event Organizers (Producers):</b> Require an intuitive authoring dashboard to publish events with banner artwork, establish seat quotas, monitor real-time ticket sales, and manage event schedules.", bullet_style))
    story.append(Paragraph("• <b>Campus Administration (Auditors):</b> Need compliance assurance that event capacities do not exceed physical hall limits and that student engagement records are secure and verifiable.", bullet_style))
    story.append(Spacer(1, 10))

    # ==========================
    # 7. SCOPE OF THE PROJECT
    # ==========================
    story.append(Paragraph("7. Scope of the Implementation", h1_style))
    
    scope_data = [
        [Paragraph("Functional Module", table_header), Paragraph("In-Scope Capabilities (Implemented)", table_header), Paragraph("Future Roadmap (Out-of-Scope)", table_header)],
        [
            Paragraph("<b>Identity Management</b>", table_cell_bold),
            Paragraph("JWT Token issuance, Bcrypt password hashing (10 salt rounds), persistent AsyncStorage session.", table_cell),
            Paragraph("OAuth2 Single Sign-On (Google/SLIIT MS Account), biometric fingerprint login.", table_cell)
        ],
        [
            Paragraph("<b>Event Management</b>", table_cell_bold),
            Paragraph("Full CRUD operations, Multer multipart image uploads, category classification, creator authorization checks.", table_cell),
            Paragraph("Recurring multi-day schedules, multi-speaker agenda tables.", table_cell)
        ],
        [
            Paragraph("<b>Booking & Inventory</b>", table_cell_bold),
            Paragraph("Seat availability checking, atomic decrement logic, automatic capacity restoration upon cancellation.", table_cell),
            Paragraph("Paid payment gateway (Stripe/PayHere), tiered VIP/standard seating tiers.", table_cell)
        ],
        [
            Paragraph("<b>Verification</b>", table_cell_bold),
            Paragraph("Unique MongoDB ObjectId ticket identifiers, real-time status badges (Confirmed, Cancelled).", table_cell),
            Paragraph("Camera-based QR code ticket scanning at physical hall entrances.", table_cell)
        ]
    ]

    scope_table = Table(scope_data, colWidths=[110, 204, 190])
    scope_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('BOX', (0,0), (-1,-1), 0.75, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(scope_table)
    story.append(Spacer(1, 14))

    # ==========================
    # 8. TECHNICAL FEASIBILITY & STACK
    # ==========================
    story.append(Paragraph("8. Technical Architecture & Feasibility", h1_style))
    tech_text = (
        "The project demonstrates technical feasibility through a validated, enterprise-grade open-source technology stack:"
    )
    story.append(Paragraph(tech_text, body_style))

    story.append(Paragraph("• <b>Frontend Layer:</b> Built with React Native and Expo SDK 57, enabling universal deployment across native Android/iOS and responsive Web. Features customized HSL tokens, smooth micro-interactions, and secure AsyncStorage tokens.", bullet_style))
    story.append(Paragraph("• <b>Backend Layer:</b> Node.js runtime with Express.js routing engine. Employs modular architecture (Controllers, Middleware, Models, Routes) with centralized error interceptors.", bullet_style))
    story.append(Paragraph("• <b>Persistence Layer:</b> MongoDB Atlas cloud database with Mongoose ODM. Implements referenced schemas with relational population (<code>Event.createdBy &rarr; User</code>, <code>Booking.eventId &rarr; Event</code>).", bullet_style))
    story.append(Paragraph("• <b>Deployment:</b> Continuous deployment pipeline hosted on Render cloud infrastructure, serving both the RESTful API endpoints and the compiled single-page application bundle.", bullet_style))
    story.append(Spacer(1, 10))

    # ==========================
    # 9. EXPECTED IMPACT & CONCLUSION
    # ==========================
    story.append(Paragraph("9. Expected Impact & Value Realization", h1_style))
    impact_text = (
        "The deployment of EventHub transforms campus event administration from a reactive, labor-intensive manual task "
        "into a proactive, autonomous digital experience. Organizers achieve 100% capacity control without manual spreadsheet "
        "reconciliation, while students enjoy instant, paperless reservations directly on their mobile devices. "
        "In academic evaluations, the platform validates mastery of full-stack engineering, asynchronous API protocols, "
        "state synchronization, and database integrity."
    )
    story.append(Paragraph(impact_text, body_style))
    story.append(Spacer(1, 12))

    # Sign-off box
    sign_data = [
        [Paragraph("<b>Prepared By:</b> lakshan", meta_val), Paragraph("<b>Verified By:</b> SLIIT Academic Supervisor", meta_val)],
        [Paragraph("<b>Signature:</b> ___________________________", meta_val), Paragraph("<b>Signature:</b> ___________________________", meta_val)],
        [Paragraph("<b>Date:</b> October 2026", meta_val), Paragraph("<b>Status:</b> Approved for Implementation", meta_val)]
    ]
    sign_table = Table(sign_data, colWidths=[252, 252])
    sign_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 0.75, PRIMARY),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(sign_table)

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated: {output_path}")

if __name__ == "__main__":
    out_file = os.path.join(os.path.dirname(__file__), "Problem_Statement.pdf")
    create_problem_statement_pdf(out_file)
