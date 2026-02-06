# Research: Floating AI Chat Widget

## Decision: OpenAI ChatKit Integration Approach
**Rationale**: Using OpenAI's official ChatKit JS Agent provides a ready-made chat interface that meets our requirements without custom UI development. It handles the chat UI, loading states, and error handling automatically.
**Alternatives considered**: 
- Building a custom chat interface from scratch (more time-consuming and error-prone)
- Using third-party chat solutions (potentially less compatible with OpenAI services)

## Decision: Global Provider Pattern
**Rationale**: Implementing the chat widget as a global provider ensures it appears on all pages without modifying existing components, meeting the requirement of not changing existing code.
**Alternatives considered**:
- Per-page integration (violates the no-modification requirement)
- Higher-order components (more complex than necessary)

## Decision: Authentication Integration
**Rationale**: Leveraging the existing Better Auth + JWT system ensures consistency with the application's security model and maintains user isolation.
**Alternatives considered**:
- Separate authentication for chat (creates security inconsistencies)
- Anonymous chat access (violates user isolation requirements)

## Decision: Positioning and Styling
**Rationale**: Using Tailwind CSS with fixed positioning places the widget consistently in the bottom-right corner across all pages and devices.
**Alternatives considered**:
- CSS modules (adds complexity without benefit)
- Inline styles (harder to maintain)

## Decision: API Endpoint Structure
**Rationale**: Following the existing pattern of `/api/{user_id}/chat` maintains consistency with the established API structure and ensures proper user isolation.
**Alternatives considered**:
- Different endpoint patterns (would break consistency)
- Shared endpoints without user_id (violates user isolation)

## Technology Research: OpenAI ChatKit JS Agent
- **Installation**: `npm install @openai/chatkit-jsagent`
- **Usage**: Provides a `<Chat />` component that handles UI and communication
- **Configuration**: Supports theme="auto" for dark/light mode compatibility
- **Authentication**: Can be configured to send JWT tokens with requests
- **API Endpoint**: Accepts apiEndpoint prop to specify backend URL

## Technology Research: Next.js 16+ App Router Integration
- **Global Components**: Can be integrated at the root layout level using providers
- **Client Components**: Use "use client" directive for interactivity
- **Environment Variables**: NEXT_PUBLIC_OPENAI_DOMAIN_KEY for domain authorization
- **Styling**: Compatible with Tailwind CSS for responsive design

## Technology Research: Better Auth + JWT Integration
- **Session Access**: Can check authentication status client-side
- **Token Transmission**: JWT tokens can be attached to ChatKit requests
- **User Identification**: User ID available for API endpoint construction
- **Security**: Maintains stateless authentication as required