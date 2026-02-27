# Core System Workflow Documentation

This document provides a detailed visual and textual breakdown of the Hospital Assistant Robot's core processes. It explains what data enters each process, how it is processed, what logic is implemented, and how decisions are made.

---

## 1. Main Orchestrator (`main.py`)

**Input Data**: System startup commands and periodic timer checks (every 5 seconds).  
**Output Data**: Health status logging, spawning of process blocks, and global shutdown signals sent downstream across inter-process communication (IPC) mechanisms.

**Processing Logic**:
- **Initialization**: Sets up essential IPC queues (`audio_queue`, `motor_queue`, `audio_feedback_queue`) and globally accessible events (`shutdown_flag`, `audio_playing_flag`).
- **Orchestration**: Instantiates multiprocessing wrappers for the four main sub-systems (Vision, Interaction, Audio Player, Motor Controller) and starts them asynchronously.
- **Supervision**: Runs a continuous health loop checking if `interaction_process.py` and `pyaudio_player.py` remain alive.

**Decision Making**:
-   **If** an essential process terminates unexpectedly -> Broadcasts the termination event via `shutdown_flag`.
-   **If** a KeyboardInterrupt comes in -> Immediately sends `shutdown` strings to respective queues and attempts robust fallback joins.

```mermaid
graph TD
    Start[System Start] --> CheckHealth[Run Health Check against Dependencies]
    CheckHealth -- Pass --> InitIPC[Initialize Queues & Multiprocess Events]
    CheckHealth -- Fail --> Abort[Abort Startup Sequence]
    
    InitIPC --> SpawnProc[Spawn Vision, Interaction, Audio, Motor]
    SpawnProc --> MonitorLoop[Supervision Loop check every 5s]
    
    MonitorLoop --> IsAlive{Are Essential Processes Alive?}
    IsAlive -- Yes --> MonitorLoop
    IsAlive -- No --> TriggerShutdown[Set shutdown_flag Event]
    TriggerShutdown --> Terminate[Gracefully Terminate All Child Processes]
```

---

## 2. Vision Pipeline (`vision_process.py`)

**Input Data**: Real-time video frames accessed from the Raspberry Pi camera module via Picamera2 (outputted as RGB888 matrix).  
**Output Data**: File play requests pushed into the `audio_queue` and visual matrices relayed to a local `cv2.imshow` window for debugging.

**Processing Logic**:
1.  **Detection**: The YOLOv8n AI model evaluates each incoming frame to detect 'person' bounding boxes requiring > 50% confidence.
2.  **Tracking (Centroid Calculation)**: Translates four-point bounding coordinates into a central `(x, y)` dot mapping the physical position estimation.
3.  **Heuristic Analysis**:
    -   *Crowd Depth*: Counts the absolute number of people inside the frame.
    -   *Social Distancing*: Computes Euclidean distance arrays between every captured dot.
    -   *Queue Detection*: Funnels matrix coordinates into SciPy hierarchical clustering libraries (`linkage`, `fcluster`), isolating localized structures indicating a line.

**Decision Making**:
-   **If** Overcrowding (Count > 25) -> Request `overcrowding.mp3`
-   **If** Dangerously Close Clusters -> Request `close_proximity.mp3`
-   **If** Queue Structure formed (>= 5 people tightly lined) -> Request `queue_forming.mp3`
-   **Gatekeeping Rule**: Before sending *any* sound constraint to the audio engine, the vision process checks `audio_playing_flag`. If audio is already active from an interaction session, the vision trigger aborts safely.

```mermaid
graph TD
    FrameInput[Picamera2 RGB Frame] --> YOLO[YOLOv8 Detection Engine]
    YOLO --> BBoxes[Extract 'Person' Bounding Boxes]
    BBoxes --> Centroids[Compute Euclidean Centroids x,y]
    
    Centroids --> Distance[Generate Matrix distances]
    Centroids --> Clus[Execute SciPy Clustering]
    BBoxes --> Count[Assess Count Density]
    
    Distance --> SDCheck{Violations Detected?}
    Clus --> QCheck{Cluster > Queue Threshold?}
    Count --> CrowdCheck{Count > Capacity?}
    
    SDCheck -- Yes --> AudioPlayFlag{audio_playing_flag Set?}
    QCheck -- Yes --> AudioPlayFlag
    CrowdCheck -- Yes --> AudioPlayFlag
    
    AudioPlayFlag -- No --> Cooldown{Has Time Cooldown Passed?}
    Cooldown -- Yes --> SendAudioRequest[Put warning mp3 alert in audio_queue]
```

---

## 3. Interaction Pipeline (`interaction_process.py`)

**Input Data**: Ambient microphone frequencies transformed into PCM data byte streams.  
**Output Data**: Synthesized `gTTS` speech files queued for playback (`audio_queue`) and deterministic structural angles queued for robot joints (`motor_queue`).

**Processing Logic**:
1.  **Background Callback**: Monitors raw sound energy (dB). Spikes above calculated ambient volume are categorized natively as non-verbal noise (coughing/sneezing).
2.  **Speech Candidate Scoring**: Audio snippets are transcribed concurrently across En, Hi, and Te via Google APIs. Output strings are mathematically weighted based on language-specific sentence 'anchors' (e.g., specific grammar words) and keyword presence.
3.  **Intent Parsing & Safety Tiers**:
    -   *Tier 1 (Harm Prevention)*: Filters text explicitly against medical prescription nouns and disease diagnosis verbs.
    -   *Tier 2 (Database Match)*: Uses `difflib` algorithms to measure Levenshtein distances against expected FAQ inputs.
4.  **Generative AI Pipeline**: In absence of deterministic matches, formats user requests alongside the entire hospital knowledge base subset and ships via API to the strict Groq Llama-3.1 router to deduce classification IDs.

**Decision Making**:
-   **If** Med Trigger Word (i.e., 'symptoms of') -> Deny and warn dynamically.
-   **If** Exit keyword found -> Shut down system gracefully.
-   **If** LLM Engine identifies strict internal ID -> Output corresponding pre-written path context.
-   **If** LLM Hallucinates -> Deny. 
-   **Simultaneously**: The process automatically dispatches `turn_to:XX` rotational commands to the motor pipeline mirroring conversational engagement.

```mermaid
graph TD
    Mic[Microphone Input Audio Buffers] --> SPL[Decibel Spike Check]
    Mic --> STT[Parallel API Request: En/Hi/Te]
    
    SPL -- dB > Threshold --> Cough[Dispatch sudden sound fx]
    
    STT --> Scoring[Aggregate Translation Arrays & Weight Confidence]
    Scoring --> MedCheck{Does it violate Medical Policy?}
    
    MedCheck -- Yes --> Block[Dispatch Local Warning MP3]
    MedCheck -- No --> ExitCheck{Is it a shutdown sequence?}
    
    ExitCheck -- Yes --> Term[Queue Goodbye & Global Terminate]
    ExitCheck -- No --> KBCheck{Does difflib identify FAQ/Dept?}
    
    KBCheck -- Yes --> FormatAns[Extract String Match]
    KBCheck -- No --> LLM[Llama 3.1 Strict Classification Query]
    
    LLM --> VerifyLLM{Did AI output valid ID?}
    VerifyLLM -- Yes --> FormatAns
    VerifyLLM -- No --> Fallback[Safe Unknown Catch]
    
    FormatAns --> TTS[Compile response logic & ping TTS generator]
    Fallback --> TTS
    Block --> TTS
    
    TTS --> QueueA[Drop output hash in audio_queue]
    QueueA --> MotorQ[Dispatch randomized gaze mapping in motor_queue]
```

---

## 4. Audio Engine (`pyaudio_player.py`)

**Input Data**: Dictionaries specifying playback commands (like `{'command': 'play', 'file': 'xyz.mp3'}`).  
**Output Data**: Raw continuous stereo output frames broadcast over initialized speakers.

**Processing Logic**:
- Checks native hardware to query which bitrates and device indexes are actively supported.
- Captures highly compressed MP3 data out of the `audio_cache` cache filesystem.
- Recalculates frequency domain via `PyDub` to downsample/upsample the audio buffer to comply strictly with the connected hardware format restrictions (like jumping from 24kHz -> 48kHz seamlessly).

**Decision Making**:
-   **If** `play` task is received via queue while another is being handled -> Truncates current audio completely overriding the output stream directly in memory.
-   **If** Track Ends -> Inserts a `{'status': 'finished'}` log into `audio_feedback_queue` so the orchestration pipeline unblocks the system microphones.

```mermaid
graph LR
    AQ[Dequeue packet from audio_queue] --> Parse{Determine Command}
    Parse -- play --> MP3Load[Index MP3 File Descriptor]
    Parse -- stop --> StreamClose[Kill active PyAudio Stream Frame]
    
    MP3Load --> Resample[Resample via PyDub to match Device Profile]
    Resample --> WavByte[Export into RAM bound WAV IO]
    WavByte --> StreamWrite[PyAudio writeframes execution chunk]
    
    StreamWrite -- Complete --> FQ[Inform audio_feedback_queue of track kill]
    StreamWrite -- Error --> FQ_Err[Alert audio_feedback_queue of Hardware IO dropout]
```

---

## 5. Motor Pipeline (`motor_control_process.py`)

**Input Data**: Formatted strings fetched serially from `motor_queue` like `turn_to:30`.  
**Output Data**: Encoded ASCII payload chars communicated through Python Serial over standard hardware GPIO `/dev/ttyAMA0`.

**Processing Logic**:
- Integrates a real-time hard-limiter constraint (`time.time()`) blocking consecutive motor executions firing under 0.5s intervals mitigating physical mechanical gear grind.
- Strips incoming numerical degrees down to generic direction strings to conform to firmware rules on the motor controller board.

**Decision Making**:
-   **If** angle > 5 degrees -> Forward logic `R` (Right Move Protocol).
-   **If** angle < -5 degrees -> Forward logic `L` (Left Move Protocol).
-   **Else** (-5 <= angle <= 5) -> Forward logic `C` (Force structural centering).

```mermaid
graph TD
    MQ[Dequeue IPC motor_queue] --> ParseMotor[Sub-string parsing on ':']
    ParseMotor --> CheckRate{Check Temporal Delta < 0.5s ?}
    
    CheckRate -- Yes --> BlockRate[Process sleeps dynamically to buffer gap]
    CheckRate -- No --> Evaluate[Process Motor Degrees]
    BlockRate --> Evaluate
    
    Evaluate -- Angle > 5 --> SendR[Serial Encode 'R']
    Evaluate -- Angle < -5 --> SendL[Serial Encode 'L']
    Evaluate -- Base Offset --> SendC[Serial Encode 'C']
    
    SendR --> UpdateTimestamp[Update hardware sync time]
    SendL --> UpdateTimestamp
    SendC --> UpdateTimestamp
```
