# -*- coding: utf-8 -*-
import re

from opulence.collectors.bases import ScriptCollector
from opulence.common.passwordstore import Store
from opulence.common.plugins.dependencies import BinaryDependency
from opulence.common.plugins.dependencies import PasswordDependency
from opulence.facts import Email
from opulence.facts import File
from opulence.facts import GitRepository
from opulence.facts import Username


class Gitrob(ScriptCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "Gitrob"
    _description_ = "Find sensitive files from public repositories."
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = [BinaryDependency("gitrob"), PasswordDependency("github_token")]

    ###############
    # Collector attributes
    ###############
    _allowed_input_ = Username

    ###############
    # Script attributes
    ###############
    _script_path_ = "gitrob"
    _script_arguments_ = [
        "-commit-depth",
        "50",
        "-github-access-token",
        Store().get_decrypted_password("github_token"),
        "$Username.name$",
    ]

    def parse_result(self, result):
        repos = re.findall(
            "Path\\.*: (.*)\\r\\n  Repo\\.*: (.*)\\r\\n  Message\\.*: (.*)\\r\\n  Author\\.*: (.*) \\<(.*)\\>\\r\\n( *Comment\\.*: .*\\r\\n)?  File URL\\.*: (.*)\\r\\n  Commit URL.*: (.*)\\r\\n -*",  # noqa: E501
            result,
        )
        if repos:
            for r in repos:

                path, repo, _, author, email, comment, file_url, commit_url = r
                raw_file_url = file_url.replace(
                    "/github.com/", "/raw.githubusercontent.com/",
                )
                raw_file_url = raw_file_url.replace("/blob/", "/")
                raw_file_name = raw_file_url.split("/")[-1]

                yield GitRepository(
                    url=f"https://github.com/{repo}.git",
                    host="github.com",
                    username=repo.split("/")[0],
                    project=repo.split("/")[1],
                )
                try:
                    raw_file_ext = raw_file_name.split(".")[-1]
                except Exception:
                    raw_file_ext = None

                yield Email(address=email)
                yield Username(address=author)
                yield File(
                    filename=raw_file_name, url=raw_file_url, extension=raw_file_ext,
                )
