{
  "project_name": "Text RPG Engine",

  "engine_version": "1.0.0",
  "spec_version": "1.3.0",
  "structure_version": "1.2.0",

  "governance_mode": "Lock + Controlled Evolution",
  "structure_anchor": "DD-004",

  "engine_phase": "Phase D.3 Complete – Effect DSL Governance Established",

  "schema_layer": {
    "completed": [
      "common",
      "condition",
      "effect",
      "event",
      "flags.registry",
      "content_manifest",
      "save",
      "monster",
      "item",
      "quest"
    ],
    "in_progress": [],
    "planned": []
  },

  "engine_layer_capabilities": {
    "state_ssot": "save.game_state = { flags, inventory, vars, current_location }",

    "effect_dispatcher": [
      "gold.add",
      "flag.set",
      "inventory.add",
      "inventory.remove",
      "flag.int_add",
      "var.add"
    ],

    "condition_support": [
      "flag.is_true",
      "flag.is_false",
      "flag.int_compare (eq/gt/gte/lt/lte)",
      "and (nested conditions)",
      "inventory.has"
    ],

    "quest_runtime": [
      "accept_condition evaluation",
      "complete_condition evaluation",
      "rewards.effects dispatch",
      "active quest guard",
      "completed_ids tracking"
    ],

    "cli_mvl_loop": [
      "interactive_loop",
      "load",
      "list",
      "accept",
      "progress",
      "check",
      "complete",
      "where",
      "locations",
      "move",
      "save",
      "reload"
    ],

    "runtime_context": [
      "session-scoped current_location (mirror of game_state)",
      "location validation (valid locations set)",
      "CLI-driven location control (where / move / locations)"
    ],

    "location_gating": [
      "quest completion gate (engine-side overlay)",
      "wrong location blocks completion",
      "correct location allows completion",
      "persistent location via save.game_state.current_location"
    ]
  },

  "validation": {
    "mvl_protocol_version": "1.0",
    "monster_mvl_status": "PASS",
    "item_mvl_status": "PASS",
    "quest_mvl_status": "PASS",
    "behavior_gate_status": "PASS",
    "location_gate_status": "PASS",
    "location_persistence_status": "PASS",
    "last_validation_date": "2026-04-12"
  },

  "validation_tools": {
    "location": "05_engine/validation/",
    "scripts": [
      "mvl_test_v1.py",
      "mvl_test_v2.py"
    ]
  },

  "official_fixture": {
    "monster": "03_data/monsters/test_*.json",
    "item": "03_data/items/test_*.json",
    "quest": "03_data/quests/test_*.json"
  },

  "notes": [
    "DD-020 established: Effect DSL Governance Charter (Naming / Boundary / Coverage)",
    "Canonical naming locked: flag.add_int (flag.int_add deprecated as non-canonical)",
    "Contract boundary enforced: var.add is engine-only (forbidden in content layer)",
    "Coverage validation introduced: Schema + Behavior dual-layer enforcement",
    "Negative enforcement active: non-canonical DSL and uncovered effects blocked from content",
    "Phase D.4 prepared: Registry–Schema sync + DSL alignment + coverage expansion"
  ],

  "next_targets": [
    "Evaluate extending location gating to accept / event / action flows",
    "Assess need for formal world/location schema (map / entity layer)",
    "Evaluate adjacency / movement constraints (graph or rule-based)",
    "Define Phase D.3 scope (location-aware interaction layer)",
    "Run full MVL Protocol regression under Spec 1.3.0"
  ]
}