# Use Case Diagram

## Overview

This diagram describes the main interactions between users and the PathToGrad system. The system helps students create a study plan, check prerequisites, and track graduation progress. Academic advisors can review the student's plan and give feedback. Academic staff can maintain curriculum data.

## Actors

| Actor | Description |
|---|---|
| Student | Main user who creates and manages a study plan. |
| Academic Advisor | Reviews student plans and provides academic guidance. |
| Academic Staff | Maintains course, prerequisite, and curriculum data. |
| LLM Service | Supports study plan generation and explanation. |

## Use Case Diagram

```mermaid
flowchart LR
    Student[Student]
    Advisor[Academic Advisor]
    Staff[Academic Staff]
    LLM[LLM Service]

    subgraph System[PathToGrad System]
        UC1((Generate Study Plan))
        UC2((Check Prerequisites))
        UC3((Track Graduation Progress))
        UC4((Review Student Plan))
        UC5((Maintain Curriculum Data))
        UC6((Explain Recommendation))
    end

    Student --> UC1
    Student --> UC2
    Student --> UC3
    Student --> UC6

    Advisor --> UC4
    Advisor --> UC3

    Staff --> UC5

    UC1 --> UC2
    UC1 --> UC3
    UC1 --> UC6
    UC1 -. uses .-> LLM
    UC6 -. uses .-> LLM
