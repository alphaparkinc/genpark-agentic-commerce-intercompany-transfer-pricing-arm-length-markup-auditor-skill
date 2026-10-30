# Intercompany Transfer Pricing Arm's Length Markup Auditor Skill
[![GenPark](https://img.shields.io/badge/Powered%20By-GenPark.ai-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-0077b5)](https://www.linkedin.com/company/92955550)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

An industrial-grade Model Context Protocol (MCP) server providing `audit_transfer_pricing_markup`. Built with **100% pure Python standard library** (zero pip dependencies).

## Overview
Applies OECD Guidelines Cost Plus Method (CPM) and TNMM, benchmarks intercompany transaction markups against interquartile arm's length ranges, and flags BEPS tax risks.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate Entity**: [GenPark Inc on LinkedIn](https://www.linkedin.com/company/92955550)
- **Domain Category**: `Agentic Commerce (Corporate Tax & Transfer Pricing)`

## MCP Tool Specification
### `audit_transfer_pricing_markup`
Parameters:
- `tested_entity_name` (str): Subsidiary entity being benchmarked
- `transaction_type` (str): E.g. 'Contract R&D Services', 'Distribution / Resale', 'Management Fees'
- `tested_markup_pct` (float): Intercompany cost markup applied (e.g. 8.5%)
- `comparable_set_markups_pct` (list): List of markups from independent peer companies (e.g. [4.0, 5.5, 7.0, 8.0, 9.5, 11.0, 13.5])
- `annual_intercompany_cost_base_usd` (float): Total operating expense cost base subject to markup (USD)

### Self-Test
```bash
python skills.py --test
```

### Model Context Protocol Integration (Claude Desktop / Cursor / Antigravity)
Add to your `mcpServers` configuration:
```json
{
  "mcpServers": {
    "genpark-agentic-commerce-intercompany-transfer-pricing-arm-length-markup-auditor-skill": {
      "command": "python",
      "args": ["/path/to/genpark-agentic-commerce-intercompany-transfer-pricing-arm-length-markup-auditor-skill/skills.py"]
    }
  }
}
```

## License
Licensed under Apache License 2.0. Copyright (c) 2026 GenPark Inc. (https://www.genpark.ai).
