import datetime
import os
from sqlite3 import Connection

from dotenv import load_dotenv
from github import Github, GithubException

from main.db.db_config import connect


def get_changes(con: Connection):
    cur = con.cursor()
    cur.execute("SELECT character_name, actor_json FROM characters WHERE pushed = 0")
    result = cur.fetchall()
    cur.close()

    return [
        {
            "character_name": character_name,
            "actor_json": actor_json
        } for character_name, actor_json in result
    ]


def update_pushed_characters(con: Connection, character_names: list[str]):
    cur = con.cursor()
    cur.executemany(
        "UPDATE characters SET pushed = 1 WHERE character_name = ?",
        [(character_name,) for character_name in character_names]
    )


def push_change_single_character(character_name: str, base64):
    g = Github(os.getenv('TOKEN'))

    repo = g.get_repo("EtuneDnD/etune-shared-compendium-db")

    try:
        repo.update_file(
            f"actors/{character_name}.json",
            "Updating character from cron",
            base64,
            sha=repo.get_contents(f"actors/{character_name}.json").sha
        )
    except GithubException as e:
        if e.status == 404:
            repo.create_file(
                f"actors/{character_name}.json",
                "Creating character from cron",
                base64
            )
        else:
            raise e


def push_changes(con: Connection, character_changes: list[dict]):
    for change in character_changes:
        push_change_single_character(change["character_name"], change["actor_json"])
    update_pushed_characters(con, [change["character_name"] for change in character_changes])


def periodic_github_push_action(con: Connection):
    changes = get_changes(con)
    push_changes(con, changes)
    con.commit()
    con.close()


if __name__ == '__main__':
    load_dotenv(dotenv_path="..\\.env")
    periodic_github_push_action(connect())
    print(f"[{datetime.datetime.now()}] - Finished periodic github push.")
