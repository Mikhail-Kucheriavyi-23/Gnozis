# Context Contract v1

A user's working context is persistent, permission-aware state assembled from authorized sources. It is not owned by an AI session or device.

## Context layers
1. identity
2. workspace/project
3. knowledge
4. research
5. task
6. session

## Requirements
- Every context item has an owner or governing workspace.
- Every item has provenance and version information.
- Access is evaluated before inclusion in an assembled context.
- Context may cross devices and interfaces without copying the entire private store to a client.
- Revocation must prevent future unauthorized inclusion.
- AI clients receive least-privilege context for the current task.
- Disconnecting a source removes it from active project context without implying deletion of the source itself.
