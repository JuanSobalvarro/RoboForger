

### Understanding `fine` vs. `zone` in RAPID

In RAPID (the programming language for ABB robots), **"fine"** refers to the **Zone Data (`zonedata`)** argument in a move instruction.

#### 1. `fine` (Stop Point)

When a move instruction is executed with the **"fine"** zone data, it indicates that the robot should move to the target position with high precision, stopping exactly at the specified point without any overshoot or blending with subsequent movements.

* **Use Case:** Critical precise positioning (e.g., assembly tasks, welding start/stop points, picking up delicate components).

#### 2. `z1`, `z10`, `z50`... (Zone / Fly-by Points)

These are called **Fly-by points**. When you use a zone (e.g., `z10`), you tell the robot: *"Aim for this point, but you don't need to stop. As soon as you are within 10mm of the target, start curling towards the next point."*

* **Precision:** Approximate. The robot "cuts the corner."
* **Speed:** Faster. The robot maintains momentum and flows smoothly between points.
* **Logic:** Crucially, the robot controller often looks ahead ("pre-fetch"). Logic placed after a zone point might execute *while* the robot is rounding the corner, not exactly *at* the corner.

---

### Comparison Table

| Feature | `fine` | `z10` / `z50` (Zone) |
| --- | --- | --- |
| **Motion** | Stop-and-Go | Continuous / Smooth |
| **Velocity at Point** | 0 mm/s | Non-zero (maintains speed) |
| **Path Shape** | Sharp corner (exact angle) | Rounded corner (fillet) |
| **Logic Timing** | Strict (happens after stop) | Approximate (happens near the zone) |
| **Wear & Tear** | High (jerky motion) | Low (smooth motion) |

---

### Code Examples

**Example 1: FINE Point**
The robot moves to `p10`, comes to a complete stop, and *then* executes the logic to open the gripper.

```rapid
MoveL p10, v1000, fine, tool0;
SetDO gripper_open, 1;

```

**Example 2: ZONE Point**
The robot moves towards `p20`. Once it gets close (within 50mm), it immediately starts curving toward `p30` without stopping.

```rapid
MoveL p20, v1000, z50, tool0;
MoveL p30, v1000, z50, tool0;

```