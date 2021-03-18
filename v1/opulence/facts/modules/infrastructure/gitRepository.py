# -*- coding: utf-8 -*-
from opulence.common.fields import StringField
from opulence.facts.bases import BaseFact


class GitRepository(BaseFact):
    _name_ = "Git repository"
    _description_ = "Remote git repository (github, gitlab, bitbucket ..)"
    _author_ = "Louis"
    _version_ = 1

    def setup(self):
        self.url = StringField(
            mandatory=True, default="https://github.com/jurelou/opulence.git",
        )
        self.host = StringField()
        self.username = StringField()
        self.project = StringField()

    def get_summary(self):
        return f"{self.url.value}"
