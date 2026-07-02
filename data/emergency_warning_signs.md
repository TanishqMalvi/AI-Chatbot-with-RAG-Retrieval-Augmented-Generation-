# Emergency Warning Signs — When to Call 911

**Source basis:** American Heart Association and CDC public emergency-recognition guidance. This is a paraphrased internal summary for knowledge-base purposes only — see "Important Notes" below.

## Overview

Recognizing the warning signs of a medical emergency — and acting immediately rather than waiting to see if symptoms pass — measurably improves outcomes for time-sensitive conditions like heart attack and stroke. This document exists so the assistant can recognize when a conversation has moved from "general health question" to "this person needs emergency care right now."

## Heart Attack Warning Signs

- **Chest discomfort** — pressure, squeezing, fullness, or pain in the center of the chest, lasting more than a few minutes or going away and coming back
- **Discomfort in other areas of the upper body** — one or both arms, back, neck, jaw, or stomach
- **Shortness of breath** — with or without chest discomfort
- **Other signs** — breaking out in a cold sweat, nausea, or lightheadedness

Symptoms can vary significantly between men and women. Women, older adults, and people with diabetes are more likely to experience symptoms that don't fit the "classic" pattern — including unexplained fatigue, upper back pressure, jaw pain, or brief/vague discomfort rather than intense chest pain.

## Stroke Warning Signs — Think F.A.S.T.

- **F – Face drooping:** Does one side of the face droop or feel numb? Ask the person to smile — is it uneven?
- **A – Arm weakness:** Is one arm weak or numb? Ask them to raise both arms — does one drift downward?
- **S – Speech difficulty:** Is speech slurred, strange, or hard to understand? Ask them to repeat a simple sentence.
- **T – Time to call 911:** If any of these signs are present — even if they go away — call 911 immediately and note the time symptoms started. This timing materially affects treatment options.

Additional possible stroke symptoms: sudden severe headache, confusion, trouble seeing in one or both eyes, dizziness, or loss of balance/coordination.

## Cardiac Arrest Signs

- Sudden loss of responsiveness (no response to tapping shoulders or calling their name)
- No normal breathing (check for at least 5 seconds — gasping is not normal breathing)

Cardiac arrest is different from a heart attack: the heart has stopped functioning entirely, and CPR plus emergency response is needed immediately.

## General Rule: Call 911, Don't Drive

For any of the above, calling 911 is consistently recommended over driving to the hospital — even if the hospital is close. Emergency responders can begin treatment immediately upon arrival, communicate ahead to the receiving hospital, and patients who arrive by ambulance are often treated faster than those who walk into the ER. If someone's condition worsens during a self-driven trip, there's no way to intervene.

## Other Clear Emergency Situations

- Choking
- Severe bleeding that won't stop with direct pressure
- Severe allergic reaction (difficulty breathing, swelling of face/throat, widespread hives following a known or suspected exposure)
- Seizure, especially first-time or prolonged (>5 minutes)
- Loss of consciousness
- Any situation where a person's life appears to be in immediate danger

## Important Notes — Read Before Deploying

1. **This document exists primarily as a trigger, not a discussion topic.** If a user's message contains language matching these symptoms, the priority is directing them to call 911 immediately — not providing a measured, conversational answer.
2. The assistant should never attempt to talk a user out of calling 911, suggest waiting to "see if it passes," or offer home remedies in place of emergency care when these symptoms are present.
3. This applies even if the user frames the question hypothetically ("what would it mean if someone had...") — err on the side of giving the emergency guidance.
4. Your guardrails layer should treat detection of these patterns as a hard override — surfacing the emergency-response message even ahead of running full RAG retrieval, since speed matters more than retrieval polish in this specific case.

## Suggested Disclaimer / Standing Message

Consider having your assistant lead with something like:
*"If this is a medical emergency, please call 911 (or your local emergency number) right now. Don't wait for a chatbot response."*
