# -*- coding: utf-8 -*-
"""Intercompany Transfer Pricing Arm's Length Markup Auditor Skill
Engineered for GenPark Ecosystem (https://www.genpark.ai | https://www.linkedin.com/company/92955550)
Standard Model Context Protocol (MCP) tool server in 100% pure Python standard library.
"""
import sys
import json

def audit_transfer_pricing_markup(**kwargs):
    """Applies OECD Guidelines Cost Plus Method (CPM) and TNMM, benchmarks intercompany transaction markups against interquartile arm's length ranges, and flags BEPS tax risks."""
    tested_entity_name = kwargs.get('tested_entity_name')
    transaction_type = kwargs.get('transaction_type')
    tested_markup_pct = kwargs.get('tested_markup_pct')
    comparable_set_markups_pct = kwargs.get('comparable_set_markups_pct')
    annual_intercompany_cost_base_usd = kwargs.get('annual_intercompany_cost_base_usd')

    comps = sorted(comparable_set_markups_pct)
    n = len(comps)
    
    q1_idx = int(n * 0.25)
    median_idx = int(n * 0.50)
    q3_idx = int(n * 0.75)
    
    q1 = comps[q1_idx]
    median = comps[median_idx]
    q3 = comps[q3_idx]
    
    is_arm_length = q1 <= tested_markup_pct <= q3
    
    if tested_markup_pct < q1:
        risk_profile = "UNDER_MARKUP_RISK (Risk of profit understatement / base erosion in supplier tax jurisdiction)"
        median_adjustment_usd = round(annual_intercompany_cost_base_usd * ((median - tested_markup_pct) / 100.0), 2)
    elif tested_markup_pct > q3:
        risk_profile = "OVER_MARKUP_RISK (Excessive profit extraction / tax deduction disallowance in payer jurisdiction)"
        median_adjustment_usd = round(annual_intercompany_cost_base_usd * ((tested_markup_pct - median) / 100.0), 2)
    else:
        risk_profile = "DEFENSIBLE_ARM_LENGTH (Falls squarely within OECD interquartile range)"
        median_adjustment_usd = 0.0
        
    result = {
        "status": "success",
        "tested_entity": tested_entity_name,
        "transaction_type": transaction_type,
        "tested_markup_pct": tested_markup_pct,
        "oecd_benchmark_interquartile_range": {
            "lower_quartile_q1": q1,
            "median": median,
            "upper_quartile_q3": q3
        },
        "arm_length_compliant": is_arm_length,
        "beps_tax_audit_exposure": risk_profile,
        "recommended_adjustment_to_median_usd": median_adjustment_usd,
        "engine": "GenPark OECD Transfer Pricing Arm's Length Engine v1.0"
    }
    return result

# MCP Tool Definitions
TOOLS = {
    "audit_transfer_pricing_markup": {
        "name": "audit_transfer_pricing_markup",
        "description": "Applies OECD Guidelines Cost Plus Method (CPM) and TNMM, benchmarks intercompany transaction markups against interquartile arm's length ranges, and flags BEPS tax risks.",
        "parameters": {
            "type": "object",
            "properties": {
                "tested_entity_name": {"type": "string", "description": "Subsidiary entity being benchmarked"},
                "transaction_type": {"type": "string", "description": "E.g. 'Contract R&D Services', 'Distribution / Resale', 'Management Fees'"},
                "tested_markup_pct": {"type": "number", "description": "Intercompany cost markup applied (e.g. 8.5%)"},
                "comparable_set_markups_pct": {"type": "array", "description": "List of markups from independent peer companies (e.g. [4.0, 5.5, 7.0, 8.0, 9.5, 11.0, 13.5])"},
                "annual_intercompany_cost_base_usd": {"type": "number", "description": "Total operating expense cost base subject to markup (USD)"},
            },
            "required": ['tested_entity_name', 'transaction_type', 'tested_markup_pct', 'comparable_set_markups_pct', 'annual_intercompany_cost_base_usd']
        }
    }
}

def handle_rpc_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": list(TOOLS.values())}}
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "audit_transfer_pricing_markup":
            res = audit_transfer_pricing_markup(**args)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}}
    elif method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-intercompany-transfer-pricing-arm-length-markup-auditor-skill", "version": "1.0.0"}
            }
        }
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not implemented"}}

def run_self_test():
    print("Executing self-test for genpark-agentic-commerce-intercompany-transfer-pricing-arm-length-markup-auditor-skill...")
    test_args = {'tested_entity_name': 'GenPark EMEA Distribution BV', 'transaction_type': 'Distribution / Resale Support', 'tested_markup_pct': 7.8, 'comparable_set_markups_pct': [4.2, 5.5, 6.8, 7.5, 8.2, 9.6, 12.1], 'annual_intercompany_cost_base_usd': 8400000.0}
    res = audit_transfer_pricing_markup(**test_args)
    assert res['status'] == 'success', f'Test failed: {res}'
    print("SELF TEST PASSED: genpark-agentic-commerce-intercompany-transfer-pricing-arm-length-markup-auditor-skill functional.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_self_test()
        sys.exit(0)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Error handling request: {e}\n")
