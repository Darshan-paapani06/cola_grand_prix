import time
import random
import os
import sys
import shutil

# ══════════════════════════════════════════════════════════════
#   COLORS
# ══════════════════════════════════════════════════════════════
R       = "\033[0m"
BOLD    = "\033[1m"
BLUE    = "\033[94m"
RED     = "\033[91m"
YELLOW  = "\033[93m"
GREEN   = "\033[92m"
CYAN    = "\033[96m"
WHITE   = "\033[97m"
MAGENTA = "\033[95m"

def move_cursor_up(n):
    sys.stdout.write(f"\033[{n}A")
    sys.stdout.flush()

def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def show_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

def clear():
    os.system("cls" if os.name == "nt" else "clear")

# ══════════════════════════════════════════════════════════════
#   ASCII CARS  —  names stamped on the body
#   Car is 6 rows tall, 20 chars wide
# ══════════════════════════════════════════════════════════════

PEPSI_CAR = [
    r"  .____________.",
    r" /  __      __  \ ",
    r"|  |  |    |  |  |",
    r"|    PEPSI        |",
    r" \______________/ ",
    r"  (@@)      (@@)  ",
]

COLA_CAR = [
    r"  .____________.",
    r" /  __      __  \ ",
    r"|  |  |    |  |  |",
    r"|   COCA-COLA     |",
    r" \______________/ ",
    r"  (@@)      (@@)  ",
]

CAR_HEIGHT = len(PEPSI_CAR)   # 6
CAR_WIDTH  = 20

# ══════════════════════════════════════════════════════════════
#   TRACK CONFIG  (auto-detect terminal width)
# ══════════════════════════════════════════════════════════════
TERM_WIDTH = min(shutil.get_terminal_size().columns - 2, 92)
TRACK_LEN  = TERM_WIDTH - CAR_WIDTH - 6

# ══════════════════════════════════════════════════════════════
#   RENDER HELPERS
# ══════════════════════════════════════════════════════════════

def render_lane(car_lines, pos, color, finish):
    """Return list of strings for one car's lane at position `pos`."""
    rendered = []
    for row_idx, car_row in enumerate(car_lines):
        total_w = finish + CAR_WIDTH + 6
        buf = list(" " * total_w)

        # Dotted ground on bottom row
        if row_idx == CAR_HEIGHT - 1:
            for x in range(finish + 4):
                if x % 5 == 0:
                    buf[x] = "·"

        # Finish line (all rows)
        fl = finish + CAR_WIDTH + 3
        if 0 <= fl < len(buf):
            buf[fl] = "║"

        # Car body
        start = pos
        for ci, ch in enumerate(car_row):
            idx = start + ci
            if 0 <= idx < len(buf):
                buf[idx] = ch

        raw = "".join(buf)

        # Split: pre-car  /  car  /  post-car
        pre  = raw[:start]
        mid  = raw[start : start + len(car_row)]
        post = raw[start + len(car_row):]

        rendered.append(
            f"{YELLOW}║{R} {pre}{color}{BOLD}{mid}{R}{post}{YELLOW}║{R}"
        )
    return rendered


def progress_bar(pos, finish, color, width=38):
    filled = int((min(pos, finish) / finish) * width)
    bar    = "█" * filled + "░" * (width - filled)
    pct    = int((min(pos, finish) / finish) * 100)
    return f"  {color}{BOLD}[{bar}]{R} {color}{pct:>3}%{R}"


def hline(char="─", color=YELLOW):
    w = TERM_WIDTH + 2
    return f"{color}{char * w}{R}"


# ══════════════════════════════════════════════════════════════
#   INTRO SCREEN
# ══════════════════════════════════════════════════════════════

def intro():
    clear()
    tw = TERM_WIDTH + 2
    print(f"\n{YELLOW}{BOLD}{'═' * tw}{R}")
    title = "🏁   C O L A   G R A N D   P R I X   🏁"
    print(f"{YELLOW}{BOLD}{title.center(tw)}{R}")
    print(f"{YELLOW}{BOLD}{'═' * tw}{R}\n")

    # Both cars side by side
    gap = 10
    for i in range(CAR_HEIGHT):
        p = f"{BLUE}{BOLD}{PEPSI_CAR[i]:<{CAR_WIDTH}}{R}"
        c = f"{RED}{BOLD}{COLA_CAR[i]:<{CAR_WIDTH}}{R}"
        print(f"      {p}{' ' * gap}{c}")

    print()
    print(f"  {BLUE}🔵  Lane 1  →  PEPSI        (Blue Racer){R}")
    print(f"  {RED}🔴  Lane 2  →  COCA-COLA    (Red  Racer){R}")
    print(f"\n  {YELLOW}Track length : {TRACK_LEN} units   |   Terminal width : {TERM_WIDTH} cols{R}")
    print(f"\n  {GREEN}{BOLD}Press  ENTER  to fire the engines ...{R}")
    input()


# ══════════════════════════════════════════════════════════════
#   COUNTDOWN
# ══════════════════════════════════════════════════════════════

def countdown():
    steps = [
        (RED,    "  3  "),
        (YELLOW, "  2  "),
        (GREEN,  "  1  "),
        (CYAN,   " GO! 🚀 "),
    ]
    for color, txt in steps:
        clear()
        box = "─" * 22
        print(f"\n\n\n   {color}{BOLD}{box}")
        print(f"   {txt.center(22)}")
        print(f"   {box}{R}\n\n")
        time.sleep(0.80)


# ══════════════════════════════════════════════════════════════
#   LIVE RACE  (smooth cursor-up re-draw)
# ══════════════════════════════════════════════════════════════

# Lines printed per frame:
#   header: 2
#   per lane: label(1) + car rows(CAR_HEIGHT) + progress(1) + divider(1) = CAR_HEIGHT+3
#   two lanes: 2*(CAR_HEIGHT+3)
#   status bar: 1
#   blank: 1
FRAME_LINES = 2 + 2 * (CAR_HEIGHT + 3) + 2
_first_frame = True


def draw_frame(pepsi_pos, cola_pos, event_msg=""):
    global _first_frame
    finish = TRACK_LEN

    lines = []
    lines.append(f"\n{YELLOW}{BOLD}  🏁  COLA GRAND PRIX  —  LIVE RACE  🏁{R}")
    lines.append(hline())

    # ── Pepsi ──
    lines.append(f"  {BLUE}{BOLD}🔵  PEPSI{R}")
    lines += render_lane(PEPSI_CAR, pepsi_pos, BLUE, finish)
    lines.append(progress_bar(pepsi_pos, finish, BLUE))
    lines.append(hline("·", CYAN))

    # ── Coca-Cola ──
    lines.append(f"  {RED}{BOLD}🔴  COCA-COLA{R}")
    lines += render_lane(COLA_CAR, cola_pos, RED, finish)
    lines.append(progress_bar(cola_pos, finish, RED))
    lines.append(hline())

    # ── Status ──
    ev_str = f"   {MAGENTA}{BOLD}{event_msg}{R}" if event_msg else ""
    lines.append(
        f"  {BLUE}Pepsi : {pepsi_pos:>3}/{finish}{R}"
        f"   {RED}Cola : {cola_pos:>3}/{finish}{R}"
        f"{ev_str}"
    )
    lines.append("")

    if not _first_frame:
        move_cursor_up(len(lines))
    _first_frame = False

    print("\n".join(lines), end="", flush=True)


# ══════════════════════════════════════════════════════════════
#   RACE ENGINE  —  smooth 1-unit-per-tick movement
# ══════════════════════════════════════════════════════════════

def race():
    global _first_frame
    _first_frame = True

    pepsi_pos = 0
    cola_pos  = 0
    finish    = TRACK_LEN
    event_msg = ""

    # Fractional accumulators for sub-unit speeds
    pepsi_acc = 0.0
    cola_acc  = 0.0

    TICK = 0.055   # seconds per frame (~18 fps)

    hide_cursor()

    while pepsi_pos < finish and cola_pos < finish:
        draw_frame(pepsi_pos, cola_pos, event_msg)
        event_msg = ""

        # Speed roll each tick (floats → smooth)
        # Pepsi: 0.42–0.82  |  Cola: 0.22–0.62  →  Pepsi reliably faster
        pepsi_speed = random.uniform(0.42, 0.82)
        cola_speed  = random.uniform(0.22, 0.62)

        # ── Random race events ──────────────────────────────
        roll = random.random()
        if roll < 0.035:
            boost = random.uniform(0.7, 1.4)
            pepsi_speed += boost
            event_msg = f"⚡ PEPSI NITRO BOOST!  +{boost:.1f} spd"
        elif roll < 0.065:
            slip = random.uniform(0.3, 0.6)
            cola_speed = max(0.0, cola_speed - slip)
            event_msg = f"⚠  Cola TYRE SLIP!  −{slip:.1f} spd"
        elif roll < 0.085:
            stumble = random.uniform(0.15, 0.3)
            pepsi_speed = max(0.1, pepsi_speed - stumble)
            event_msg = f"🔧 Pepsi micro-wobble  −{stumble:.1f} spd"
        elif roll < 0.105:
            cola_speed = max(0.0, cola_speed - 0.5)
            event_msg = "💨 Cola drafting issue — slowing!"

        # Accumulate
        pepsi_acc += pepsi_speed
        cola_acc  += cola_speed

        # Flush whole steps
        steps_p = int(pepsi_acc)
        steps_c = int(cola_acc)
        pepsi_acc -= steps_p
        cola_acc  -= steps_c

        pepsi_pos = min(pepsi_pos + steps_p, finish)
        cola_pos  = min(cola_pos  + steps_c, finish)

        # ── Safety: Pepsi must always win ──────────────────
        # Stop Cola at finish-1 if Pepsi hasn't crossed yet
        if cola_pos >= finish and pepsi_pos < finish:
            cola_pos = finish - 1
        # If Cola gets within 2 units of finish, stall it
        if cola_pos >= finish - 2 and pepsi_pos < finish - 2:
            cola_pos = finish - 3

        time.sleep(TICK)

    # Final frozen frame
    draw_frame(finish, min(cola_pos, finish - 1))
    time.sleep(0.4)
    show_cursor()


# ══════════════════════════════════════════════════════════════
#   WINNER SCREEN
# ══════════════════════════════════════════════════════════════

TROPHY = [
    r"          ___________",
    r"         '._==_==_=_.'",
    r"         .-\:      /-.",
    r"        | (|:.     |) |",
    r"         '-|:.     |-'",
    r"           \::.    /",
    r"            '::. .'",
    r"              ) (",
    r"            _.' '._",
    r"           '-------'",
]

def winner_screen():
    clear()
    print()
    for line in TROPHY:
        print(f"    {YELLOW}{BOLD}{line}{R}")

    print(f"\n  {BLUE}{BOLD}{'🏆  ' * 5}  PEPSI  WINS  THE  GRAND  PRIX!  {'  🏆' * 5}{R}\n")

    for line in PEPSI_CAR:
        print(f"        {BLUE}{BOLD}{line}{R}")

    print(f"\n  {CYAN}{'★' * 54}{R}")
    print(f"  {WHITE}{BOLD}   🔵 Pepsi crosses the finish line FIRST!{R}")
    print(f"  {BLUE}   Pepsi — champion of speed, taste & victory!{R}")
    print(f"  {CYAN}{'★' * 54}{R}")
    print(f"\n  {RED}  🔴 Coca-Cola fought hard — a worthy rival!{R}\n")

    # Celebration flicker
    icons = ["🎉", "🎊", "🏁", "⚡", "🔵", "💨", "🏆"]
    for _ in range(4):
        for f in icons:
            sys.stdout.write(f"\r  {YELLOW}{BOLD}  {f * 11}  {f * 11}{R}  ")
            sys.stdout.flush()
            time.sleep(0.09)

    print(f"\n\n  {GREEN}{BOLD}Thanks for watching the Cola Grand Prix!{R}\n")


# ══════════════════════════════════════════════════════════════
#   MAIN
# ══════════════════════════════════════════════════════════════

def main():
    try:
        intro()
        countdown()
        clear()
        race()
        winner_screen()
    except KeyboardInterrupt:
        show_cursor()
        print(f"\n\n  {YELLOW}Race interrupted! See you next time! 🏁{R}\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
