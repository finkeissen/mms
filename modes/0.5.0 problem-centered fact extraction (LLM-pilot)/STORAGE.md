# MMS — Storage Strategy (GitHub → large scale)

## Goal
Keep MMS repos small and stable while datasets can grow without GitHub becoming the bottleneck.

---

## Rule 1 — Repos contain specs + code, not bulk data
### MMS (core)
- schemas
- contracts
- scripts
- documentation
- small examples only

### Datasets (bulk)
- domains
- subdomains
- problems
- facts
- matrices
- run artifacts

Bulk data is never stored in the MMS core repo.

---

## Rule 2 — Introduce a Dataset Registry
MMS references datasets via a registry file (paths/URIs + version + hash).

### Registry file
`mms/datasets/registry.json`

Each dataset entry provides:
- `dataset_id`
- `storage` (local / git / s3 / gcs / azure / http)
- `uri`
- `version`
- `sha256` (integrity)
- `schema` reference

---

## Rule 3 — Storage tiers
### Tier A (small, GitHub OK)
- domains (80)
- subdomains (1.700)
Store as a separate `mms-datasets` repo or inside MMS under `datasets/`.

### Tier B (medium, Git LFS optional)
- pilot problems (10–1,000)
- pilot runs (reports)
May be stored with Git LFS or in a separate repo.

### Tier C (large, not GitHub)
- problemfields (~100,000)
- atomic problems (~10,000,000)
- facts (>> 10M)
- matrices (>> 10M rows)
Store in object storage:
- S3-compatible (MinIO)
- AWS S3
- GCS
- Azure Blob
- or plain HTTP file server

GitHub holds only:
- registry pointers
- schemas
- checksums
- tooling

---

## Rule 4 — Data format + partitioning
All bulk data must be:
- append-only
- partitioned
- content-addressable when possible

Recommended layout (object storage):
`<bucket>/mms-data/<dataset_id>/<version>/part-00000.jsonl.gz`

Partition keys (choose one):
- domain/subdomain
- problem_id prefix
- date/run_id

Compression:
- `.jsonl.gz` mandatory at Tier C

---

## Rule 5 — Versioning policy
### Core
- semantic versions (0.x.y)
- tagged releases

### Datasets
- dataset versions independent of core
- use `YYYY-MM-DD` or incrementing `v000123`
- always store `sha256`

---

## Registry schema (minimal)
`mms/datasets/registry.json`

```json
{
  "registry_version": "0.1.0",
  "datasets": [
    {
      "dataset_id": "domains",
      "schema": "datasets/schema/domain.schema.json",
      "storage": "git",
      "uri": "git:https://github.com/<org>/mms-datasets",
      "version": "v000001",
      "sha256": "sha256:..."
    },
    {
      "dataset_id": "atomic-problems",
      "schema": "mms/versions/0.4.0/problem/problem.schema.json",
      "storage": "s3",
      "uri": "s3://<bucket>/mms-data/atomic-problems/v000001/",
      "version": "v000001",
      "sha256": "sha256:..."
    }
  ]
}

