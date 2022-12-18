import os
import sqlite3

from dotenv import load_dotenv
from github import Github


def get_changes():
    con = sqlite3.connect("../database.db")
    cur = con.cursor()
    cur.execute("SELECT character_name, actor_base64 FROM characters WHERE pushed = 0")
    result = cur.fetchall()
    cur.close()
    con.close()

    return [
        {
            "character_name": character_name,
            "actor_base64": actor_base64
        } for character_name, actor_base64 in result
    ]


def update_pushed_characters(character_names: list[str]):
    con = sqlite3.connect("../database.db")
    cur = con.cursor()
    cur.executemany(
        "UPDATE characters SET pushed = 1 WHERE character_name = ?",
        [(character_name,) for character_name in character_names]
    )
    con.commit()
    con.close()


def push_change_single_character(character_name: str, base64):
    load_dotenv()
    g = Github(os.getenv('TOKEN'))

    repo = g.get_repo("EtuneDnD/etune-shared-compendium-db")
    repo.update_file(
        f"actors/{character_name}.json",
        "Updating character from cron",
        base64,
        sha=repo.get_contents(f"actors/{character_name}.json").sha
    )


def push_changes(character_changes: list[dict]):
    for change in character_changes:
        push_change_single_character(change["character_name"], change["actor_base64"])
    update_pushed_characters([change["character_name"] for change in character_changes])


if __name__ == '__main__':
    changes = get_changes()
    push_changes(changes)
