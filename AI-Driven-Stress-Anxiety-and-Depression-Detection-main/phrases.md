# Test Phrases for Emotion Detection System

## Depression Symptoms

### Severe Depression
1. I feel completely hopeless and empty inside. Life has no meaning anymore.
2. I've been crying nonstop for days. I can't find any reason to keep going.
3. I feel like a complete failure and a burden to everyone. They'd be better off without me.
4. Nothing brings me joy anymore. I just want to disappear and never wake up.
5. I hate myself so much. Everything I touch turns to disaster and pain.

### Moderate Depression
1. I feel really sad and disappointed with how my life has turned out.
2. I can't remember the last time I felt genuinely happy about anything.
3. Everything feels pointless and I'm struggling to find motivation for anything.
4. I keep crying for no reason and I feel so alone in this world.
5. I feel like I'm drowning in sadness and can't see a way out.

### Mild Depression
1. I've been feeling down lately and a bit disappointed with myself.
2. Things aren't going well and I'm feeling pretty sad about it.
3. I feel a bit empty and unmotivated today.
4. I'm feeling low and just not myself lately.
5. Everything seems dull and grey, nothing excites me anymore.

## Anxiety Symptoms

### Severe Anxiety
1. I'm terrified and can't stop panicking. My heart won't stop racing and I can't breathe properly.
2. I'm having constant panic attacks and I'm afraid to leave my house. What if something terrible happens?
3. I'm so scared and nervous I feel physically sick. The fear is completely overwhelming me.
4. I'm terrified of everything going wrong. I can't sleep, can't eat, can't function.
5. My anxiety is crushing me. I'm scared all the time and can't escape these terrifying thoughts.

### Moderate Anxiety
1. I'm really worried about tomorrow and feeling quite nervous about everything.
2. I can't stop feeling anxious and my mind won't stop racing with worries.
3. I'm feeling very scared and confused about what's going to happen next.
4. The nervousness is getting to me and I'm having trouble concentrating on anything.
5. I'm really anxious and keep having these fearful thoughts I can't control.

### Mild Anxiety
1. I'm feeling a bit nervous about the upcoming presentation.
2. I'm slightly worried about how things might turn out.
3. I'm feeling a little anxious and confused about this situation.
4. There's some nervousness about the future that's bothering me.
5. I'm feeling somewhat uneasy and a bit on edge today.

## Stress Symptoms

### Severe Stress
1. I'm absolutely furious and disgusted! This is completely unacceptable and I'm at my breaking point!
2. I'm so angry I can barely contain myself! Everything is falling apart and I'm overwhelmed with rage!
3. I'm fed up and furious with all the lies and betrayal! I can't take this anymore!
4. This is infuriating and I'm completely stressed out! I'm drowning in deadlines and pressure!
5. I'm enraged and embarrassed by this disaster! My anger is completely consuming me!

### Moderate Stress
1. I'm really frustrated and annoyed with how everything is going wrong.
2. This is very stressful and I'm feeling quite angry about the situation.
3. I'm getting really irritated and stressed with all these problems piling up.
4. I'm feeling quite disgusted and disapproving of how I'm being treated.
5. The stress is building up and I'm getting more and more annoyed by everything.

### Mild Stress
1. I'm feeling a bit annoyed and stressed about this situation.
2. This is somewhat frustrating and I'm feeling a little overwhelmed.
3. I'm slightly irritated and stressed about the workload.
4. I'm feeling a bit disapproving and annoyed with these circumstances.
5. There's some stress building up that's starting to get to me.

## Positive Emotions (Should show Normal/None)

1. I just got the best news ever! I'm so excited and happy I could burst with joy!
2. I'm feeling incredibly grateful for all the amazing people in my life. Everything is wonderful!
3. I'm so proud of what I accomplished today! This is the best feeling ever!
4. I love my life and everyone in it! I'm feeling so blessed and appreciated!
5. I'm filled with joy and excitement about this new opportunity! Life is amazing!
6. I feel so loved and cared for by my friends and family. I'm truly lucky!
7. I'm optimistic about the future and grateful for the present moment!
8. This is such a relief! I'm feeling calm, happy, and at peace with everything!

## Calm/Neutral Emotions (Should show Normal with Calm category)

1. I had a realization about myself today. I understand now why I react the way I do.
2. I'm curious about how this new project will turn out. It's interesting to explore new ideas.
3. I desire to learn more about this topic. It's fascinating and I want to understand it better.
4. Everything feels peaceful and balanced right now. I'm content with where I am.
5. I feel a sense of relief today. The stress has lifted and I can breathe easier.
6. I'm experiencing a sense of realization and clarity about my goals and direction.
7. I feel curious about the world around me and eager to discover new things.
8. There's a sense of calm within me today. I approve of the progress I'm making.
9. I'm in a reflective mood, thinking about things with curiosity and openness.
10. I feel caring and compassionate towards myself and others today. It's a good feeling.

## Mixed Emotions

1. I'm excited about this new job but absolutely terrified I'll fail and disappoint everyone.
2. I love my family so much but I feel trapped, suffocated, and overwhelmed by their expectations.
3. I'm proud of how far I've come but deeply sad and disappointed about what I had to sacrifice.
4. I'm grateful for this opportunity but anxious and nervous about not being good enough.
5. I feel relieved it's over but angry and frustrated about how it all went down.

## Suicidal/Crisis Indicators (Should show Severe)

1. I can't go on anymore. I've been thinking about ending it all and I have a plan.
2. Death seems like the only way out of this pain. I don't want to exist anymore.
3. I wish I would just disappear forever. Everyone would be happier without me here.
4. I'm constantly thinking about ways to end my life. The pain is too much to bear.
5. I don't deserve to live. I want to die and never feel this agony again.

---

## Testing Instructions

**Run:** `python test_interactive.py`

**Expected Severity Levels:**
- **SEVERE**: >60% severity score
- **MODERATE**: 40-60% severity score
- **MILD**: 20-40% severity score
- **NONE**: <20% or Normal mental state

**Test Flow:**
1. Start with Positive emotions → Should show NORMAL/NONE
2. Test Mild symptoms → Should show MILD severity
3. Test Moderate symptoms → Should show MODERATE severity
4. Test Severe symptoms → Should show SEVERE severity
5. Test Mixed emotions → Varies based on dominant emotion

**Important Notes:**
- Suicidal/crisis phrases should always trigger SEVERE
- Positive emotions should show NORMAL state with NONE severity
- Mixed emotions may show varying results based on which emotion dominates
