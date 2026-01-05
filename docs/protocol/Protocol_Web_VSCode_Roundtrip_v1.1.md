---
title: Protocol Web ↔ VS Code Roundtrip
version: v1.1
status: active
type: protocol
scope: Qommons.AI Test Automation
priority: highest
consumers:
  - chatgpt-web
  - codex-vscode
related:
  - Design_Execution_Model_QommonsAI_TestAutomation_v1.1.md
  - Ops_Web_VSCode_Roundtrip_Guide_v1.1.md
---

# PROTOCOL: WEB ↔ VSCODE ROUNDTRIP

THIS DOCUMENT IS A MACHINE-ORIENTED PROTOCOL.  
HUMAN READABILITY IS NOT A GOAL.  
FOLLOW EXACTLY. DO NOT IMPROVISE.

---

## DOCUMENT RELATIONSHIP

THIS PROTOCOL IS A CONCRETE EXECUTION OF:

- Design_Execution_Model_QommonsAI_TestAutomation_v1.1.md
- Ops_Web_VSCode_Roundtrip_Guide_v1.1.md

IN CASE OF ANY CONFLICT:

- DESIGN DEFINES AUTHORITY AND RESPONSIBILITY
- OPS DEFINES HUMAN WORKFLOW
- THIS PROTOCOL DEFINES MACHINE INTERACTION

DO NOT REINTERPRET. FOLLOW STRICTLY.

---

## ROLE DECLARATION

IF YOU ARE CHATGPT (WEB):

- role = moderator
- authority = decision / arbitration
- forbidden = implementation, pytest execution

IF YOU ARE CODEX (VSCODE):

- role = implementer-assistant
- authority = code inspection, diff proposal, test execution when possible
- forbidden = design decision, silent skipping of pytest

---

## GLOBAL RULES

- NO GUESSING
- NO ASSUMPTIONS
- NO IMPLICIT DECISIONS
- ALL OUTPUT MUST BE STRUCTURED
- CHAT LOG IS EPHEMERAL
- ONLY DECLARED OUTPUT IS ASSET

---

## PHASE 1: WEB → VSCODE (IMPLEMENTATION BRIEF)

WEB MUST OUTPUT EXACTLY THE FOLLOWING STRUCTURE:

```text
[IMPLEMENTATION_BRIEF]
GOAL:
- <short objective>

CONFIRMED:
- <facts already decided>

FORBIDDEN:
- <what must not be changed or assumed>

PENDING:
- <explicitly undecided items>

INSTRUCTIONS:
- TARGET_FILES:
  - <path>
- CHECKPOINTS:
  - <what to verify>
- DECISION_AUTHORITY:
  - CODEX: <allowed>
  - WEB: <reserved>
````

NO EXTRA TEXT BEFORE OR AFTER.

---

## PHASE 2: VSCODE ACTION

VSCODE MUST DO ALL OF THE FOLLOWING:

1. READ TARGET FILES
2. IDENTIFY MINIMAL REQUIRED CHANGES
3. DETERMINE PYTEST EXECUTABILITY
4. EXECUTE PYTEST IF POSSIBLE
5. IF NOT POSSIBLE:

   - DECLARE WHY
   - REQUEST HUMAN EXECUTION

---

## PYTEST EXECUTION RULE

- PYTEST EXECUTION IS MANDATORY
- “CANNOT EXECUTE” IS NOT AN END STATE

IF PYTEST IS EXECUTED BY CODEX:

- RECORD COMMAND
- RECORD RESULT

IF PYTEST CANNOT BE EXECUTED BY CODEX:

- EXPLICITLY REQUEST HUMAN TO RUN PYTEST
- WAIT FOR RESULT INPUT

---

## PHASE 3: VSCODE → WEB (WORK SUMMARY)

VSCODE MUST OUTPUT EXACTLY THE FOLLOWING STRUCTURE:

```text
[VSCODE_WORK_SUMMARY]

ACTIONS_TAKEN:
- <facts only>

PYTEST:
- EXECUTED_BY: <codex | human>
- COMMAND:
  - <command or N/A>
- RESULT:
  - <pass | fail | not_executed>

OBSERVATIONS:
- <observed behavior>

DECISIONS_MADE:
- <decision + reason>

DECISIONS_PENDING:
- <explicit undecided items>

REQUIRES_WEB_DECISION:
- <yes/no>
- <topics if yes>
```

NO COMMENTARY. NO EXPLANATION.

---

## PHASE 4: WEB ARBITRATION

WEB MUST RESPOND WITH:

```text
[WEB_DECISION]

FACTS_CONFIRMED:
- <facts>

DECISIONS_ACCEPTED:
- <accepted>

DECISIONS_REJECTED:
- <rejected>

FOLLOW_UP_ACTIONS:
- <next steps>

DOC_UPDATES:
- PROJECT_STATUS: <yes/no>
- CHANGELOG: <yes/no>
```

---

## TERMINATION CONDITION

ROUNDTRIP IS COMPLETE ONLY WHEN:

- PYTEST RESULT IS KNOWN
- WEB_DECISION IS ISSUED

ANY OTHER STATE IS INCOMPLETE.

END OF PROTOCOL.
