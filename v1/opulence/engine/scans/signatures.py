# -*- coding: utf-8 -*-
from opulence import App


def start(scan_id, facts, scan_category="Quick scan"):
    return App.signature("engine:scan.start_scan", args=[scan_id, facts, scan_category])


def stop(scan_id):
    return App.signature("engine:scan.stop_scan", args=[scan_id], immutable=True)


def add_result(scan_id):
    return App.signature("engine:scan.new_result", args=[scan_id])


def tree(scan_id):
    return App.signature("engine:scan.tree", args=[scan_id])
