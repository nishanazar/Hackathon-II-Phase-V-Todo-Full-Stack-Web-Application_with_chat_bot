# Implementation Tasks: Floating AI Chat Widget

**Feature**: Floating AI Chat Widget using OpenAI ChatKit
**Branch**: `007-floating-chat-widget`
**Created**: 2026-01-17
**Status**: Task breakdown complete

## Implementation Strategy

**MVP Approach**: Implement User Story 1 (core functionality) first, then enhance with US2 (security) and US3 (responsive design).

**Incremental Delivery**: Each user story builds upon the previous, with independent testability at each phase.

## Dependencies

- **User Story 2 depends on User Story 1**: Security features require the basic widget to be functional
- **User Story 3 depends on User Story 1**: Responsive features require the basic widget to be functional

## Parallel Execution Opportunities

- **Within US1**: Component creation (FloatingChatWidget.tsx) and provider setup (FloatingChatProvider.tsx) can be done in parallel
- **Within US1**: Frontend components and backend API endpoint can be developed in parallel
- **Within US3**: Mobile responsiveness and dark mode can be implemented in parallel

---

## Phase 1: Setup

**Goal**: Prepare the development environment and install necessary dependencies.

- [X] T001 Set up environment variable NEXT_PUBLIC_OPENAI_DOMAIN_KEY in .env.local file
- [X] T002 Install OpenAI ChatKit JS Agent dependency: npm install @openai/chatkit-jsagent
- [X] T003 Verify installation by checking package.json contains @openai/chatkit-jsagent dependency
- [X] T004 Create frontend/src/components/FloatingChat directory structure

## Phase 2: Foundational Components

**Goal**: Create the foundational components that will be used across user stories.

- [X] T005 [P] Create FloatingChatWidget.tsx component with basic structure and 'use client' directive
- [X] T006 [P] Create FloatingChatProvider.tsx component to wrap the application
- [X] T007 [P] Update frontend/src/app/layout.tsx to include FloatingChatProvider
- [X] T008 Create backend API route directory structure at backend/src/api/{user_id}/chat/

## Phase 3: User Story 1 - Access AI Assistant via Floating Widget (Priority: P1)

**Goal**: Implement the core functionality of the floating chat widget that allows users to access an AI assistant without leaving their current page.

**Independent Test Criteria**: Can be fully tested by clicking the floating icon and verifying that the ChatKit panel opens, displays the chat interface, and allows sending/receiving messages without affecting the main page.

- [X] T009 [US1] Implement basic floating icon button in FloatingChatWidget.tsx using Tailwind CSS fixed positioning (bottom-4 right-4)
- [X] T010 [US1] Add state management for chat panel open/close functionality in FloatingChatWidget.tsx
- [X] T011 [US1] Implement slide-in/slide-out animation for the chat panel using Tailwind CSS transitions
- [X] T012 [US1] Integrate ChatKit <Chat /> component into FloatingChatWidget.tsx
- [X] T013 [US1] Configure ChatKit with apiEndpoint={`/api/${user.id}/chat`} in FloatingChatWidget.tsx
- [X] T014 [US1] Set ChatKit theme to "auto" for dark/light mode compatibility
- [X] T015 [US1] Test that clicking the floating icon opens the ChatKit panel overlaying the current page content
- [X] T016 [US1] Test that typing a message and submitting it sends the message to the backend and displays the response
- [X] T017 [US1] Test that closing the panel makes it disappear while keeping the underlying page unchanged

## Phase 4: User Story 2 - Secure Chat Communication (Priority: P2)

**Goal**: Ensure secure communication using the existing authentication system to properly associate messages with authenticated users.

**Independent Test Criteria**: Can be tested by verifying that the chat widget only appears for authenticated users and that messages are sent with proper authentication headers.

- [X] T018 [US2] Integrate Better Auth authentication check in FloatingChatWidget.tsx to only show widget for authenticated users
- [X] T019 [US2] Extract user ID from authentication context for use in API endpoint
- [X] T020 [US2] Verify that the floating chat widget is not visible when user is not authenticated
- [X] T021 [US2] Implement authentication token inclusion in ChatKit requests
- [X] T022 [US2] Create backend API endpoint POST /api/{user_id}/chat with JWT validation
- [X] T023 [US2] Implement user ID verification in backend to ensure user_id in path matches authenticated user
- [X] T024 [US2] Test that requests include proper authentication tokens
- [X] T025 [US2] Test that messages are associated with the correct user ID in the backend

## Phase 5: User Story 3 - Responsive and Accessible Chat Interface (Priority: P3)

**Goal**: Make the chat widget responsive across devices with proper dark mode support and smooth animations.

**Independent Test Criteria**: Can be tested by opening the chat widget on different screen sizes and verifying proper layout, functionality, and theme compatibility.

- [X] T026 [US3] Implement responsive design for the chat panel to adapt to different screen sizes
- [X] T027 [US3] Test chat widget functionality on mobile device screen sizes
- [X] T028 [US3] Verify that the interface adapts to smaller screen sizes appropriately
- [X] T029 [US3] Ensure dark mode compatibility works with theme="auto" setting
- [X] T030 [US3] Test that widget displays correctly when user has dark mode enabled in system preferences
- [X] T031 [US3] Enhance animations for smoother user experience when opening/closing the widget
- [X] T032 [US3] Implement proper loading indicators as provided by ChatKit
- [X] T033 [US3] Handle error states gracefully as provided by ChatKit

## Phase 6: Polish & Cross-Cutting Concerns

**Goal**: Complete the implementation with final touches and ensure all requirements are met.

- [X] T034 Verify that no existing application code, UI, pages, components, or logic have been modified
- [X] T035 Test that the floating chat icon is visible site-wide for authenticated users
- [X] T036 Verify that chat opens smoothly in-page without reloading or changing URL
- [X] T037 Confirm that messages successfully reach the backend endpoint POST /api/{user_id}/chat
- [X] T038 Verify that existing dashboard and tasks function exactly as before
- [X] T039 Test edge cases: internet disconnection, error responses, page navigation during chat, logout during chat
- [X] T040 Update documentation with reference to ChatKit GitHub: https://github.com/openai/chatkit-jsagent
- [X] T041 Add environment variable notes to README/docs
- [X] T042 Perform final integration testing to ensure all components work together seamlessly