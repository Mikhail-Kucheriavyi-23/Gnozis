# Context Model v1

Context = Identity + Workspace/Project + authorized Knowledge + authorized Research + Task + Session.

Assembly rule:
1. authenticate actor;
2. resolve workspace/project;
3. evaluate authorization;
4. resolve permitted sources;
5. assemble only required context;
6. attach provenance/version metadata;
7. return context to the requesting interface.

Context continuity must never expand authorization.