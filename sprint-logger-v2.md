About Sprint Logger

```
| Feature / Dimension    | **v1 (Integrated)**                                                              | **v2 (Prototype)**                                                       |
| ---------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| **Location in repo**   | `grove-sprint-logger/` (top-level)                                                | `prototypes/sprint-logger-v2/`                                            |
| **UI**                 | Single-page form (HTML + CSS)                                                     | Multi-step wizard-like flow                                               |
| **Inputs captured**    | Name, date, duration, goal, modules, start time, summary, reflections, next steps | Same + structured module focus + tags                                     |
| **Output format**      | Markdown (`sessions/YYYY-MM-DD-sprint-name.md`)                                   | Markdown to `logs/YYYY-MM-DD-sprint-name.md` (consistent naming enforced) |
| **Export / Save**      | Copy from `<pre>` block                                                           | Auto-save to repo path, optional export                                   |
| **OpenAI integration** | GPT-4 formatting, temperature = 0.5                                               | GPT-4 + module-specific prompts (planned)                                 |
| **Modules support**    | Free-text only                                                                    | Predefined time-boxed modules (Prompt Engine, Visualizer, etc.)           |
| **Preview**            | Shown after submit                                                                | Live preview while typing                                                 |
| **Collaboration**      | Single-user                                                                       | Planned team sync / async multi-user support                              |
| **Tagging / metadata** | Manual in text                                                                    | Auto-tag: module focus, sprint type, status                               |
| **Design**             | Basic form, minimal Inter font styling                                            | Improved UX polish, structured flow, more interactive                     |
| **Roadmap link**       | Manual mention                                                                    | Planned: flag logs against roadmap items                                  |
```
---

Sprint Logger Features

- [x] Today’s date
- [x] Duration field updates in real-time
- [x] Current start time (HH:MM)
- [x] Filename in logs/YYYY-MM-DD-sprint-name.md with versioning (-v1, -v2, etc.) →
- [x] Ensures multiple sprints per day will never overwrite existing logs
- [x] Markdown auto-saves locally 
- [x] Tracking exact elapsed time automatically
- [x] Timer info integrated with auto-save and versioned filenames
- [x] One-click auto-start sprint timer →
	- [x] Start Sprint Timer button (Automatically updates Duration field as time passes. Stops timer when form is submitted). 
	- [x] Auto-stop and auto-submit after the set sprint duration

- [x] Repeat Last Session button: (carries over Next Critical Step to new Goal)
	- [x] Loads last session values
	- [x] Updates:
		- [x] Goal with previous “Next Critical Step”
		- [x] Date and start time
	- [x] Fully repeatable iterative workflow without overwriting previous files

- [x] Defaults:
	- [x] Default name/initials
	- [x] Default duration (e.g., 60 min) 
	- [x] Default modules focused
	- [x] Default goal template
	- [x] Default TL;DR summary
	- [x] Default Reflections
	- [x] Default Next Steps / Next Critical Step

---

Sprint Logger Style Guide
- **Concise & clear** → 1–2 sentences per field is enough.  
- **Markdown-first** → all logs are stored as `.md`.  
- **Structure** → follow the sections: TL;DR, Reflections, Next Steps.  
- **Async-friendly** → write so others can quickly catch up.  

---

File Structure
- `grove-sprint-logger.html` → main logger interface (form + API link).  
- `logs/` → saved sprint logs (one per session).  
- `modules/` → focused module logs (e.g. Time-boxed experiments). 

---