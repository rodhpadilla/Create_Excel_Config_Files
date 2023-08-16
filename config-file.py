#!/usr/bin/env python3

__author__ = "Rodrigo H Padilla"
__email__ = "rod.hpadilla@gmail.com"


import csv
import xlsxwriter
from jinja2 import FileSystemLoader, StrictUndefined
from jinja2.environment import Environment


CSV_SOURCE_FILE = "source_data.csv"
TEMPLATE = "conf-template.j2"
OUTPUT_CONFIGURATION_FILENAME = "BW_UPGRADES_Configuration_File.xlsx"


def open_template(template_file):
    env = Environment(undefined=StrictUndefined)
    env.loader = FileSystemLoader("./")
    template = env.get_template(template_file)
    return template


def excel_tab(workbook, site, csv_info, template_type):
    format_class = workbook.add_format(
        {"bold": True, "underline": True, "bg_color": "yellow"}
    )
    comment_class = workbook.add_format({"italic": True})
    font_class = workbook.add_format({"font_name": "Consolas", "font_size": "10"})
    worksheet = workbook.add_worksheet(site)
    worksheet.write_url("A1", "internal:'Index'!A1", string="INDEX")
    row = 1
    col = 0
    cfg = template_type.render(csv_info)
    cfg_lines = [cfg.strip() for cfg in cfg.splitlines()]
    for lines in cfg_lines:
        if ".-" in lines:
            worksheet.write(row, col, lines, format_class)
            row += 1
        elif "!" in lines:
            worksheet.write(row, col, lines, comment_class)
            row += 1
        else:
            worksheet.write(row, col, lines, font_class)
            row += 1


def generate_file():
    try:
        template = open_template(TEMPLATE)
        workbook = xlsxwriter.Workbook(OUTPUT_CONFIGURATION_FILENAME)
        worksheet = workbook.add_worksheet("Index")
        with open(CSV_SOURCE_FILE) as f2:
            read_csv2 = csv.DictReader(f2)
            for bw_info in read_csv2:
                site_name2 = bw_info["Branch_Name"].rstrip()
                excel_tab(
                    workbook,
                    site=site_name2,
                    csv_info=bw_info,
                    template_type=template,
                )

        with open(CSV_SOURCE_FILE) as f1:
            read_csv = csv.DictReader(f1)
            bold = workbook.add_format({"bold": True})
            row = 1
            col = 1
            worksheet.write("B1", "Branch_ID", bold)
            worksheet.write("C1", "Branch_Name", bold)
            worksheet.write("D1", "Hostname", bold)
            worksheet.write("E1", "New_BW", bold)
            for info in read_csv:
                Branch_ID = info["Branch_ID"]
                site_name = info["Branch_Name"].rstrip()
                New_BW = info["New_BW"]
                Hostname = info["Hostname"]
                worksheet.write(row, col, Branch_ID)
                worksheet.write_url(
                    row, col + 1, f"internal:'{site_name}'!A1", string=f"{site_name}"
                )
                worksheet.write(row, col + 2, Hostname)
                worksheet.write(row, col + 3, New_BW)
                row += 1
        workbook.close()
    except Exception as err:
        print("Failed --> ", OUTPUT_CONFIGURATION_FILENAME, err)
    else:
        print("Success --> ", OUTPUT_CONFIGURATION_FILENAME)


if __name__ == "__main__":
    generate_file()
