import os
import random
import subprocess
from datetime import datetime, timedelta


def ask_number():
    while True:
        answer = input("Number of commits [20]: ").strip()
        if not answer:
            return 20
        try:
            number = int(answer)
            if number > 0:
                return number
        except ValueError:
            pass
        print("Enter a positive whole number.")


def ask_repo():
    while True:
        answer = input("Repository path [.]: ").strip() or "."
        if os.path.isdir(answer):
            return answer
        print("That directory does not exist.")


def ask_file():
    return input("File to update [data.txt]: ").strip() or "data.txt"


def random_date():
    now = datetime.now()
    return now - timedelta(
        days=random.randint(0, 364),
        seconds=random.randint(0, 86399),
    )


def make_commit(repo, filename, date):
    path = os.path.join(repo, filename)
    with open(path, "a", encoding="utf-8") as file:
        file.write(f"Update: {date.isoformat()}\n")

    env = os.environ.copy()
    date_text = date.strftime("%Y-%m-%dT%H:%M:%S")
    env["GIT_AUTHOR_DATE"] = date_text
    env["GIT_COMMITTER_DATE"] = date_text

    subprocess.run(["git", "add", filename], cwd=repo, check=True)
    subprocess.run(
        ["git", "commit", "-m", "Update activity data"],
        cwd=repo,
        env=env,
        check=True,
    )


def main():
    print("Odeus - contribution activity helper")
    count = ask_number()
    repo = ask_repo()
    filename = ask_file()

    for index in range(count):
        date = random_date()
        print(f"[{index + 1}/{count}] {date:%Y-%m-%d %H:%M:%S}")
        make_commit(repo, filename, date)

    print("Pushing commits...")
    subprocess.run(["git", "push"], cwd=repo, check=True)
    print("Done.")


if __name__ == "__main__":
    main()
