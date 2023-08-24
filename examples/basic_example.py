from pyfileflow import Rule

rule = Rule("delete")
rule = Rule(rule, "move", ...)  # if condition : deleted so stop here
rule = Rule("copy", ...)

rule.apply_rules(folder="/")
