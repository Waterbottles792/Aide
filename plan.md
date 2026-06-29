# Aide Project Plan

## Vision
Build Aide into a polished, desktop-friendly AI mentor for cybersecurity learning. The product should guide users through challenges step by step, encourage independent problem solving, and avoid spoiling solutions too early.

## Core Goals
- Provide a clean chat-based learning experience.
- Support multiple LLM providers through a simple configuration flow.
- Keep user data and API keys secure.
- Make the app progressively smarter over time with better context, hints, and learning modes.

## Product Principles
- Teach, don’t spoil.
- Be adaptive to the user’s skill level.
- Keep the experience simple and focused.
- Prefer clear guidance over raw answers.
- Make the tool useful for platforms like TryHackMe, HackTheBox, PortSwigger, and CTFs.

---

## Phase 0 — Foundation and Setup
### Objective
Establish a stable development baseline for both backend and frontend.

### Tasks
- Confirm project structure under the Aide app directory.
- Set up backend environment and dependency management.
- Set up frontend environment and local dev workflow.
- Create a reliable run process for both services.
- Document setup steps for future contributors.

### Deliverables
- Working local backend and frontend startup flow.
- Clear README instructions.
- Consistent development environment.

---

## Phase 1 — Core MVP
### Objective
Create the first usable version of the app.

### Tasks
- Implement a simple chat interface.
- Connect frontend to backend chat endpoint.
- Add provider configuration UI.
- Persist provider settings locally.
- Support secure storage for API keys.
- Add health check and basic backend routing.
- Ensure the app can run end to end locally.

### Deliverables
- A basic but usable chat experience.
- User-configurable LLM provider settings.
- Secure local persistence for provider data.

---

## Phase 2 — Learning Experience Improvements
### Objective
Make the assistant feel more like a mentor than a generic chatbot.

### Tasks
- Add a system prompt that emphasizes progressive guidance.
- Introduce hint levels: beginner, intermediate, advanced.
- Add support for structured responses such as:
  - hint
  - next step
  - explanation
  - recap
- Encourage the assistant to ask guiding questions instead of giving direct answers.
- Add a “challenge context” mode where the user can describe the current task.

### Deliverables
- More guided and educational responses.
- Better tone and behavior for mentoring.
- A stronger distinction between tutoring and answer-spoiling.

---

## Phase 3 — Context and Session Memory
### Objective
Make the assistant remember the current learning context across turns.

### Tasks
- Track the current challenge or topic.
- Preserve conversation context within a session.
- Add optional session summaries.
- Persist sessions to disk so they survive restarts.
- Allow the user to reset or start a new learning session.
- Keep context compact and relevant.

### Deliverables
- Session-aware conversations.
- Session persistence across app reloads.
- Better continuity and less repetitive guidance.
- Cleaner state handling in the app.

---

## Phase 4 — Challenge-Aware Modes
### Objective
Support different learning environments and challenge types.

### Tasks
- Add modes such as:
  - general mentoring
  - CTF walkthrough
  - web security challenge
  - network security challenge
  - scripting help
- Let the user choose a mode before chatting.
- Tailor prompts and hints depending on the selected mode.

### Deliverables
- A more specialized and useful mentor experience.
- Better adaptation to different learning scenarios.

---

## Phase 5 — User Experience Polish
### Objective
Improve usability, clarity, and presentation.

### Tasks
- Improve the visual design of the frontend.
- Add chat history and message styling.
- Add loading states and error handling.
- Improve empty states and onboarding.
- Add clear labels for provider setup and connection status.
- Improve accessibility where possible.

### Deliverables
- A smoother and more professional UI.
- Better first-time user experience.

---

## Phase 6 — Persistence and Safety
### Objective
Make the app more robust and safer to use.

### Tasks
- Improve storage handling for settings and sessions.
- Add safe error handling around provider failures.
- Prevent accidental leakage of secrets in logs.
- Add basic validation for provider configuration.
- Support backup/restore of local settings if needed.

### Deliverables
- More reliable local data handling.
- Safer configuration and runtime behavior.

---

## Phase 7 — Advanced Features
### Objective
Expand the product beyond a simple chat assistant.

### Tasks
- Add optional workspace context such as notes or challenge descriptions.
- Support uploading task context or screenshots later.
- Add recommended next-step suggestions.
- Add progress tracking or skill progression features.
- Consider integration with external learning resources.

### Deliverables
- A richer mentor experience.
- Stronger long-term learning value.

---

## Phase 8 — Deployment and Distribution
### Objective
Make the app easier to use outside the local environment.

### Tasks
- Package the backend and frontend for deployment.
- Consider Docker support.
- Add environment-based configuration.
- Prepare production-safe settings.
- Document deployment steps.

### Deliverables
- A deployable version of the project.
- Clear production setup path.

---

## Suggested Development Order
1. Finish and stabilize Phase 1.
2. Focus on Phase 2 and Phase 3 to make the assistant feel like a mentor.
3. Improve UX in Phase 5.
4. Add resilience and advanced features in later phases.

---

## Immediate Next Steps
- Refine the chat experience and message handling.
- Improve the system prompt for guided tutoring.
- Add a simple session context model.
- Start implementing Phase 2 features.
