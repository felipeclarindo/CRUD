from ..app.validations.validations import (
    validate_column,
    validate_table,
    validate_value,
    validate_id
)


def tests_validate_column_passeds():
    assert validate_column("coluna1") == True
    assert validate_column("  cioluna2") == True
    assert validate_column("  columna") == True
    assert validate_column(" aaa    ") == True
    assert validate_column("    coluimna") == True
    assert validate_column("   cikyna ") == True


def tests_validate_column_fails():
    assert validate_column("") == False
    assert validate_column("!414") == False
    assert validate_column("##%#@!") == False
    assert validate_column("   !!") == False
    assert validate_column(" !$)K$ ") == False
    assert validate_column("alun a") == False
    assert validate_column("pa$aa aa") == False


def tests_validate_table_passeds():
    assert validate_table("table") == True
    assert validate_table("table241") == True
    assert validate_table("   table") == True
    assert validate_table("table   ") == True
    assert validate_table("    table     ") == True
    assert validate_table("    tab1e241     ") == True


def tests_validate_table_fails():
    assert validate_table("!") == False
    assert validate_table("") == False
    assert validate_table("   ") == False
    assert validate_table("!2141") == False
    assert validate_table("  %!%@!$@  ") == False
    assert validate_table("  %!aa$@") == False
    assert validate_table("  42141$@") == False
    assert validate_table("    tabl    e     ") == False
    assert validate_table("    ta  ble   aa    ") == False


def tests_validate_id_passeds():
    assert validate_id("1") == 1
    assert validate_id("2") == 2
    assert validate_id("3") == 3
    assert validate_id("4") == 4
    assert validate_id("5") == 5


def tests_validate_id_fails():
    assert validate_id("a") == False
    assert validate_id(" 8") == False
    assert validate_id("   46   ") == False
    assert validate_id("111 ") == False
    assert validate_id("   !4124@#!") == False


def tests_validate_value_passeds():
    assert validate_value("aaaa") == True
    assert validate_value("111") == True
    assert validate_value("a124") == True
    assert validate_value(" aaaa111") == True
    assert validate_value("        2222") == True
    assert validate_value("      111aaa  ") == True
    assert validate_value("    aaaaaa   ") == True


def tests_validate_value_fails():
    assert validate_value("") == False
    assert validate_value("!1941") == False
    assert validate_value("1@#!") == False
    assert validate_value("12 A") == False
    assert validate_value("$#@!") == False
    assert validate_value("!@#!") == False
    assert validate_value("!@@@@@") == False
    assert validate_value("%!!%@$!¨&") == False
    assert validate_value(    "%!!%@$!¨&") == False
    assert validate_value("%!!%@$!¨&"    ) == False
    assert validate_value(    "%!!%@$!¨&"       ) == False
