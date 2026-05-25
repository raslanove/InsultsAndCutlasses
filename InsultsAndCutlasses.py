from llama_cpp import Llama
import random
import time
from colorama import init, Fore, Style
import os
from typing import Optional

# =========================================================
# Globals
# =========================================================

# Define the path to your GGUF model file
MODEL_PATH = "gemma-4-E2B-it-Q4_K_M.gguf"
LORA_PATH = "gemma4-e2b-cpu-F32-LoRA.gguf"

# =========================================================
# LLM functions
# =========================================================
os.environ["LLAMA_LOG_LEVEL"] = "ERROR"
llama_model = Llama(
      model_path=MODEL_PATH,
      lora_path=LORA_PATH,
      lora_scale=1.0,
      n_ctx=1024,
      repeat_penalty=1.3,
      chat_format=None,
      seed=random.randint(0, 2**31-1),
      verbose=False
)

def build_prompt(prompt: str, system_prompt: Optional[str] = None) -> str:
    prompt = prompt.strip()
    if system_prompt and system_prompt.strip():
        system_prompt = system_prompt.strip()
        return (
            "<|turn>system\n"
            f"{system_prompt}<turn|>\n"
            "<|turn>user\n"
            f"{prompt}<turn|>\n"
            "<|turn>model\n"
        )
        
    return (
        "<|turn>user\n"
        f"{prompt}<turn|>\n"
        "<|turn>model\n"
    )

def generateInsult() -> str:
    SYSTEM_PROMPT = None
    prompt = build_prompt("<action_insult>")
    return llama_model(
        prompt,
        temperature=2.24,
        top_p=1,
        top_k=30,
        max_tokens=200)["choices"][0]["text"]

def generateReply(insult: str) -> str:
    SYSTEM_PROMPT = None
    prompt = build_prompt(f"<action_reply><insult>{insult}<reply>")
    return llama_model(
        prompt,
        temperature=0.8,
        top_p=0.8,
        top_k=30,
        max_tokens=200)["choices"][0]["text"]

def judgeReply(insult: str, reply: str) -> str:
    SYSTEM_PROMPT = "Reply with 'pass' if there's no insult, the insult is incoherent text, the insult doesn't make sense or if the reply is suitable to the insult. Reply with 'fail' only if the reply is horrible."
    # Our current training rarely ever rewards a good comeback :(( We resort to prompting instead.
    #prompt = build_prompt(f"<action_judge><insult>{insult}<reply>{reply}<grade>", system_prompt=SYSTEM_PROMPT)
    prompt = build_prompt(f"<insult>{insult}<reply>{reply}", system_prompt=SYSTEM_PROMPT)
    return llama_model(
        prompt,
        top_k=1,
        max_tokens=10)["choices"][0]["text"]

# =========================================================
#  EGA PALETTE MAPPING
# =========================================================

# Initialize ANSI colors
init(autoreset=True)

EGA = {
    1: Fore.BLUE,
    2: Fore.GREEN,
    3: Fore.CYAN,
    4: Fore.RED,
    5: Fore.MAGENTA,
    6: Fore.YELLOW,
    7: Fore.WHITE,
    8: Fore.LIGHTBLACK_EX,
    9: Fore.LIGHTBLUE_EX,
    10: Fore.LIGHTGREEN_EX,
    11: Fore.LIGHTCYAN_EX,
    12: Fore.LIGHTRED_EX,
    13: Fore.LIGHTMAGENTA_EX,
    14: Fore.LIGHTYELLOW_EX,
    15: Fore.LIGHTWHITE_EX,
}

GUYBRUSH_COLOR = EGA[7]
JUDGE_COLOR = EGA[5]

# Opponents can use any color except 5 and 7
OPPONENT_COLORS = [
    EGA[i]
    for i in range(1, 16)
    if i not in (5, 7)
]

# =========================================================
#  OPPONENTS
# =========================================================

OPPONENTS = [
    "Ugly Pirate",
    "Ferocious Pirate",
    "One-Eyed Scoundrel",
    "Toothless Buccaneer",
    "Smelly Corsair",
    "Hook-Handed Marauder",
    "Drunken Deckhand",
    "Scar-Faced Pirate",
]

WIN_QUOTES = [
    "Wow, you are good enough to challenge the swordmaster!",
]

LOSE_QUOTES = [
    "UNCLE! UNCLE!",
    "Yikes! Nice move.",
    "Look, a three-headed monkey!",
    "I give up! You win!",
]

# =========================================================
#  ASCII TITLE
# =========================================================

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
    
TITLE = r"""





 ██╗███╗   ██╗███████╗██╗   ██╗██╗  ████████╗███████╗
 ██║████╗  ██║██╔════╝██║   ██║██║  ╚══██╔══╝██╔════╝
 ██║██╔██╗ ██║███████╗██║   ██║██║     ██║   ███████╗
 ██║██║╚██╗██║╚════██║██║   ██║██║     ██║   ╚════██║
 ██║██║ ╚████║███████║╚██████╔╝███████╗██║   ███████║
 ╚═╝╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚══════╝╚═╝   ╚══════╝

              & CUTLASSES
              
              
"""

# =========================================================
#  HELPERS
# =========================================================

def say(name, text, color):
    print(color + f"{name}> {text}" + Style.RESET_ALL)


def judge_says(text):
    print(JUDGE_COLOR + f"[Judge] {text}" + Style.RESET_ALL)


def dramatic_pause():
    for _ in range(3):
        print(".")
        time.sleep(0.5)
    print()


# =========================================================
#  GAME LOOP
# =========================================================

def battle(opponent_name):

    opponent_color = random.choice(OPPONENT_COLORS)

    player_score = 0
    opponent_score = 0

    print()
    print("=" * 60)
    say(
        "Guybrush",
        "My name is Guybrush Threepwood. Prepare to die!",
        GUYBRUSH_COLOR
    )

    player_turn = True

    while player_score < 3 and opponent_score < 3:

        print()

        # =================================================
        # PLAYER INSULTS
        # =================================================
        if player_turn:

            insult = input(
                GUYBRUSH_COLOR + "Guybrush> " + Style.RESET_ALL
            )

            reply = generateReply(insult)

            say(opponent_name, reply, opponent_color)

            result = judgeReply(insult, reply)
            if result == "pass":
                opponent_score += 1

                judge_says(
                    f"{opponent_name} lands the comeback!"
                )

                player_turn = False

            else:
                player_score += 1

                judge_says(
                    "Weak comeback! Guybrush gets the point!"
                )

                player_turn = True

        # =================================================
        # OPPONENT INSULTS
        # =================================================
        else:

            insult = generateInsult()

            say(opponent_name, insult, opponent_color)

            reply = input(
                GUYBRUSH_COLOR + "Guybrush> " + Style.RESET_ALL
            )

            result = judgeReply(insult, reply)

            if result == "pass":
                player_score += 1

                judge_says(
                    "Excellent comeback! Guybrush scores!"
                )

                player_turn = True

            else:
                opponent_score += 1

                judge_says(
                    f"{opponent_name} dominates the exchange!"
                )

                player_turn = False

        judge_says(
            f"Score => Guybrush: {player_score} | "
            f"{opponent_name}: {opponent_score}"
        )

    # =====================================================
    # END OF BATTLE
    # =====================================================

    print()

    if player_score >= 3:
        say(        
            opponent_name,
            random.choice(WIN_QUOTES),
            opponent_color
        )
    else:
        say(
            "Guybrush",
            random.choice(LOSE_QUOTES),
            GUYBRUSH_COLOR
        )

    dramatic_pause()


# =========================================================
#  MAIN
# =========================================================

def main():

    clear_screen()
    print(Fore.YELLOW + TITLE + Style.RESET_ALL)

    while True:
        opponent = random.choice(OPPONENTS)
        battle(opponent)


if __name__ == "__main__":
    main()
