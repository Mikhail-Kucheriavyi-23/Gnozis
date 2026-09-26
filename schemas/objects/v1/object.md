# Gnozis Object Contract v1

Every persistent domain object has a stable identity and controlled lifecycle.

Required conceptual fields:
- id
- type
- version
- status
- owner
- visibility
- license
- payload
- relations
- provenance
- integrity

Visibility values:
public, restricted, private, confidential

Visibility and license are independent dimensions.

An object is not considered verified merely because it exists. Evidence and validation status must be represented explicitly where applicable.
