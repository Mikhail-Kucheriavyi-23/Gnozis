# External Entry Point Inventory v1

## Inventory scope

Known externally reachable surfaces identified in the current repository:

1. `gnosis-terminal-bridge/src/chat_server.py`
   - HTTP /chat
   - HTTP /v1/handshake
   - HTTP /v1/exchange
2. `gnosis-terminal-bridge/src/internet_port.py`
   - transport/session boundary
3. `gnosis-terminal-bridge/src/core_chat.py`
   - CoreChat.send() adapter path
4. Canonical Core surfaces
   - CanonicalExecutor.step/evolve()
   - Uroboros.canonical / step()
5. Compatibility surfaces
   - Uroboros.evolutionary()
   - LegacyEngine

## Findings

The terminal bridge currently validates transport/session/provenance semantics but its `/v1/exchange` handler returns an accepted transport result without constructing an Information object or invoking the new authorization boundary. Therefore transport acceptance is NOT equivalent to Core authorization.

`CoreChat.send()` is an adapter path using the compatibility Engine/State surface and is not yet an authorized external-information path under Market Information Loop v1.

CanonicalExecutor and Uroboros canonical paths remain internal Core authority surfaces. They must not be exposed directly to external information.

## Required boundary

Future external information flow:

HTTP / plugin / repository / connector
-> transport validation
-> Information
-> Authorization
-> AuthorizedExecution
-> CanonicalExecutor

No external surface may skip Information + Authorization.

## Current non-bypass status

GLOBAL NON-BYPASS: NOT PROVEN.

Known gaps:
- /v1/exchange is transport-only and not yet connected to Information authorization.
- /chat uses a compatibility adapter and requires explicit classification before it can be treated as Market Information Loop input.
- Static inventory cannot prove absence of future or indirect call paths.

## Acceptance for next phase

1. Connect /v1/exchange to the Information + Authorization boundary.
2. Define whether /chat is in or out of Market Information Loop v1; if in, route it through the same boundary.
3. Add adversarial tests proving unauthorized HTTP inputs cannot reach canonical execution.
4. Preserve existing transport replay/session protections.
5. Do not claim global non-bypass until external adapters and reachable call paths have adversarial evidence.
