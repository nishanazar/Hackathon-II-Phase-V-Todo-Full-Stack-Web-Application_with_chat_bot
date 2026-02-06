---
id: 3
title: floating-chat-widget-tasks
stage: tasks
date: 2026-01-17
surface: agent
model: Qwen
feature: floating-chat-widget
branch: 007-floating-chat-widget
user: USER
command: sp.tasks
labels: ["tasks", "chat", "widget", "frontend", "api"]
links:
  spec: "specs/001-floating-chat-widget/spec.md"
  plan: "specs/007-floating-chat-widget/plan.md"
  ticket: null
  adr: null
  pr: null
files:
  - specs/007-floating-chat-widget/tasks.md
tests:
  - specs/007-floating-chat-widget/tasks.md
---

## Prompt

$ARGUMENTS

Context for task generation: Install ChatKit JS Agent npm install @openai/chatkit-jsagent Add environment variable: NEXT_PUBLIC_OPENAI_DOMAIN_KEY=pk_xxxxx Confirm production domain is added to OpenAI domain allowlist Component Creation Create new client component FloatingChat.tsx Add "use client" directive Embed <Chat /> from ChatKit Set apiEndpoint={/api/${user_id}/chat} Set theme="auto" Add floating chat icon in component Position using Tailwind CSS: fixed bottom-4 right-4 Toggle open/close panel Global Mount Mount FloatingChat in layout/root provider Ensures it renders on all pages Do not modify existing Phase II pages Authentication Check user authentication (Better Auth + JWT) before showing widget If user is unauthenticated: Hide widget or Prompt login via existing /login page UX / Styling Smooth slide-in / slide-out animation Responsive layout for desktop & mobile Dark mode compatible (theme="auto") Loading indicators & error handling handled by ChatKit Integration Ensure messages reach backend: /api/{user_id}/chat Verify existing Phase II dashboard and tasks remain unchanged Documentation / References Add reference to ChatKit GitHub: https://github.com/openai/chatkit-jsagent Include environment variable notes in README / docs

## Response snapshot

Created a comprehensive tasks.md file for the floating AI chat widget feature with 42 tasks organized across 6 phases:

1. Phase 1: Setup (4 tasks) - Environment setup and dependency installation
2. Phase 2: Foundational Components (4 tasks) - Core component creation
3. Phase 3: User Story 1 (9 tasks) - Core functionality implementation
4. Phase 4: User Story 2 (7 tasks) - Security and authentication
5. Phase 5: User Story 3 (9 tasks) - Responsive design and UX enhancements
6. Phase 6: Polish & Cross-Cutting Concerns (9 tasks) - Final validation and documentation

Tasks follow the required checklist format with proper IDs, story labels, and file paths. Identified parallel execution opportunities and dependencies between user stories.

## Outcome

- ✅ Impact: Successfully created a complete task breakdown that follows all requirements
- 🧪 Tests: Tasks include validation steps for each user story
- 📁 Files: Generated tasks.md with 42 properly formatted tasks
- 🔁 Next prompts: Ready for implementation phase
- 🧠 Reflection: The task breakdown follows the template structure and addresses all core requirements while maintaining independence between user stories

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to implementation phase