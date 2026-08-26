# Token Trail pricing catalog

This repository publishes Token Trail's reviewed, effective-dated AI model pricing catalog.

The weekly monitor hashes the visible text of the official OpenAI and Anthropic pricing/model pages. A source change opens a pull request for human review; scraped content is never published directly as pricing. When a price changes, close the prior period with `effectiveUntil`, add the new period with `effectiveFrom`, increment `catalogVersion`, and update `updatedAt`. New models receive their own entry and source.

Token Trail checks the raw catalog once every 24 hours, validates it, caches the latest valid version, and falls back to its bundled catalog offline.
