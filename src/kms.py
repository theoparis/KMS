import sys

try:
    sys.stdout.encoding = "utf-8"
except Exception:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import time
import random
from pynput.keyboard import Key, Listener, Controller

print(
    """
===============================================================================
██╗  ██╗███╗   ███╗███████╗
██║ ██╔╝████╗ ████║██╔════╝
█████╔╝ ██╔████╔██║███████╗
██╔═██╗ ██║╚██╔╝██║╚════██║
██║  ██╗██║ ╚═╝ ██║███████║
╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝
===============================================================================
"""
)
# Set up word storage

storage = ""

# Keys being held
held = []

all_selected = False

profanity = {}
positivityModeMessage = ""

controller = Controller()


def main():
    try:
        with open("profanity.txt", "r") as f:
            for line in f:
                data = line.split("-")
                profanity[data[0]] = data[1].replace("\n", "")
    except Exception as e:
        print(f"Error reading profanity file: {e}")
        return

    try:
        with open("positivitymode.txt", "r") as f:
            positivityModeMessage = f.read()
    except FileNotFoundError:
        print("Positivity Mode file not found")
        return
    except Exception as e:
        print(f"Error reading Positivity Mode file: {e}")
        return

    print("Imported profanity...")

    def process_key(key):
        return (
            str(key)
            .replace("'", "")
            .replace("1", "i")
            .replace("0", "o")
            .replace("2", "z")
            .replace("3", "e")
            .replace("4", "a")
            .replace("5", "s")
            .replace("6", "g")
            .replace("7", "t")
            .replace("8", "b")
            .replace("9", "g")
            .lower()
        )

    nonspecial = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        " ",
    ]

    # Set up keyboard listener
    def on_press(key):
        global storage
        global held
        global all_selected

        # convert key to string
        raw_key = process_key(key)
        if raw_key not in held:
            held.append(raw_key)

        if len(raw_key) == 1 and "key.ctrl_l" not in held:
            storage += raw_key

        if raw_key == "key.space":
            storage += " "

        if raw_key == "key.enter":
            storage = ""

        if raw_key == "\\xoi":
            all_selected = True

        if raw_key == "\\xoe":
            print("Bye bye!")
            exit()

        if raw_key == "key.backspace":
            if all_selected:
                storage = ""
                all_selected = False
                return

            if "key.ctrl_l" in held:
                # Cut off letters until space reached or beginning of string
                special = False
                space = False
                erased = 0

                if len(storage) == 0:
                    return

                if storage[-1] not in nonspecial:
                    # Start special character erase, erase until nonspecial character is reached
                    while True:
                        if len(storage) == 0:
                            break

                        if storage[-1] in nonspecial:
                            break

                        storage = storage[:-1]
                else:
                    # Start normal erase. Wait until alphabet reached, then erase until space
                    # Stop at beginning of string

                    alphabetReached = False
                    while True:
                        if len(storage) == 0:
                            break

                        if alphabetReached and storage[-1] == " ":
                            break

                        if storage[-1] in nonspecial and storage[-1] != " ":
                            alphabetReached = True

                        storage = storage[:-1]

            else:
                storage = storage[:-1]

        # Input processed, now scan for profanity

        for word in profanity:
            # Cut storage by last len(word) and compare
            if storage[-len(word) :] == word:
                # Replace word by pressing backspace len(word) times
                for _ in range(len(word)):
                    controller.press(Key.backspace)
                    controller.release(Key.backspace)

                message = profanity[word]

                # 10% chance to trigger P O S I T I V I T Y  M O D E
                if random.randint(0, 100) < 10:
                    message = positivityModeMessage

                # Type out the replacement
                for letter in message:
                    controller.press(letter)
                    controller.release(letter)
                    time.sleep(0.025)

                # Don't scan for more profanity
                break

    def on_release(key):
        global held

        raw_key = process_key(key)
        try:
            held.remove(raw_key)
        except Exception:
            pass

    print("Ready!")

    # Collect events until released
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    main()
    try:
        input()
    except Exception:
        pass
