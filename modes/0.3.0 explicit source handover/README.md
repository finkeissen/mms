# MMS 0.3.0
## Explicit Handover & research-program 0.4 Compatibility

**Version:** 0.3.0  
**Status:** Decision & Responsibility Structuring System (Experimental)  
**Authority:** None

---

### What 0.3.0 establishes
This release makes one thing explicit and stable:

1) **Artifacts enter MMS only via explicit, versioned, traceable handover**.  
2) MMS remains **non-authoritative**: outputs are **system artifacts**, not truth claims.  
3) MMS aligns its handover/evaluation discipline with **research-program 0.4** as methodological baseline.

---

### Handover
The handover format is defined here:

- `handover/manifest.schema.json` — JSON Schema for a handover manifest
- `handover/manifest.example.json` — minimal valid example
- `handover/README.md` — rules/meaning (what is required, what must not be implicit)

---

### How to use this version
If you use MMS as a downstream integration space, treat the handover manifest as your **entry contract**:

- no implicit inheritance of assumptions/boundaries
- explicit limits and STOP reasons are first-class
- missing information and conflicts are allowed and must be preserved

---

### Release notes
See `RELEASE-0.3.0.md` and `CHANGELOG.md` in this version folder.
