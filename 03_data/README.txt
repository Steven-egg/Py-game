Combat Vertical Slice Patch (Beginner Village) — Lock Mode (safe)

Adds:
- Items: slime_gel, wolf_pelt
- Monsters: m.village.slime_01, m.village.wolf_01
- Quest: q.side.slime_hunt_3 (kill 3 slimes -> reward potion_small)

Registry updates:
- flags: add flg.quest.side.slime_hunt_3.completed, flg.kill.wolf.count

How to test (repo root):
  python 05_engine/cli_mvl.py load
  python 05_engine/cli_mvl.py accept q.side.slime_hunt_3
  python 05_engine/cli_mvl.py progress kill slime 3
  python 05_engine/cli_mvl.py complete
  python 05_engine/cli_mvl.py show

Optional: simulate loot into inventory (MVL has no loot roll yet)
  python 05_engine/cli_mvl.py progress item slime_gel 3
