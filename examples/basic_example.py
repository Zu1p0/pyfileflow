"""Basic example on how to use PyFileFlow."""

from pyfileflow import CopyRule, DeleteRule, MoveRule

rule = DeleteRule()
rule = MoveRule(rule)  # if condition : deleted so stop here
rule = CopyRule(rule)

rule.process(folder="/")
