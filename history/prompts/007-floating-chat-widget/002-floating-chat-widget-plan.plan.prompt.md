---
id: 2
title: floating-chat-widget-plan
stage: plan
date: 2026-01-17
surface: agent
model: Qwen
feature: floating-chat-widget
branch: 007-floating-chat-widget
user: USER
command: sp.plan
labels: ["plan", "chat", "widget", "frontend", "api"]
links:
  spec: "specs/001-floating-chat-widget/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - specs/007-floating-chat-widget/plan.md
  - specs/007-floating-chat-widget/research.md
  - specs/007-floating-chat-widget/data-model.md
  - specs/007-floating-chat-widget/quickstart.md
  - specs/007-floating-chat-widget/contracts/chat-api-contract.md
tests:
  - specs/007-floating-chat-widget/contracts/chat-api-contract.md
---

## Prompt

/sp.plan Floating AI Chat Widget using OpenAI ChatKit – Implementation Plan
Objective

Implement a floating AI chat widget at the bottom-right corner of the website using OpenAI ChatKit, without modifying any existing Phase II code or UI.

Phase I – Setup

Install ChatKit JS Agent

npm install @openai/chatkit-jsagent

Add environment variable

NEXT_PUBLIC_OPENAI_DOMAIN_KEY=pk_xxxxx

Confirm OpenAI domain allowlist includes production URL

Phase II – Create Floating Widget

Create new client component (e.g., FloatingChat.tsx)

Use "use client" directive

Embed ChatKit <Chat /> component

Set apiEndpoint={/api/${user_id}/chat}

Set theme="auto" for dark/light mode

Add floating icon button (bottom-right)

Toggles open/close of ChatKit panel

CSS: Tailwind fixed positioning (fixed bottom-4 right-4)

No existing page modifications needed

Phase III – Mount Globally

Wrap application root or layout with floating chat provider

Ensures Chat widget appears on all pages without touching existing Phase II code

Phase IV – Authentication

Use existing Better Auth + JWT session

Display chat only if user is authenticated

Otherwise:

Hide chat icon or

Prompt login modal (existing /login page)

Phase V – UX / Styling

Smooth slide-in / slide-out animation

Responsive layout (desktop + mobile)

Loading indicators & error handling provided by ChatKit

Dark mode compatible
Success Criteria

Floating chat icon visible site-wide

Chat opens smoothly in-page

Backend communication works

Existing dashboard and tasks function exactly as before

Fully judge-friendly, production-ready

## Response snapshot

Created a comprehensive implementation plan for the floating AI chat widget including:
- Technical context with language, dependencies, and platform details
- Constitution check confirming compliance with project standards
- Project structure outlining the component files to be created
- Research document covering technology decisions and approaches
- Data model defining the entities and state transitions
- Quickstart guide with implementation steps
- API contract for the chat endpoint

## Outcome

- ✅ Impact: Successfully created a complete implementation plan that meets all requirements
- 🧪 Tests: Created API contract to ensure proper backend communication
- 📁 Files: Generated plan.md, research.md, data-model.md, quickstart.md, and API contract
- 🔁 Next prompts: Ready for task breakdown phase (/sp.tasks)
- 🧠 Reflection: The plan follows the template structure and addresses all core requirements while maintaining compliance with the project constitution

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to task breakdown phase