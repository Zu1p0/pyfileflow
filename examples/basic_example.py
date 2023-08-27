"""Basic example on how to use PyFileFlow."""

from pyfileflow import Rule

rule = Rule(action="delete")
rule = Rule(rule, action="move")  # if condition : deleted so stop here
rule = Rule(rule, action="copy")

rule.process(folder="/")
