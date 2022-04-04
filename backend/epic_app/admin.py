import io
from typing import Dict, List, Tuple
from unicodedata import name
from django.contrib import admin
from django import forms
from django.shortcuts import redirect, render
from django.urls import path
from epic_app.models import Answer, EpicUser, Question, Area, Group, Program
import csv

class CsvImportForm(forms.Form):
    """
    Simple form to allow importing a 'csv' file.

    Args:
        forms (forms.Form): Default Django form.
    """
    csv_file = forms.FileField()


class AreaAdmin(admin.ModelAdmin):
    """
    Overriding of the Area list in the admin page so that we can add our custom import for all the data.
    """
    # Admin pages.
    change_list_template = "areas_changelist.html"

    def get_urls(self):
        """
        Extends the default get_urls so we can inject the import-csv on

        Returns:
            List[str]: A list of the urls to load from the admin page.
        """
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        """
        Imports a csv file into the EPIC database structure.

        Args:
            request (_type_): HTML request.

        Returns:
            _type_: HTML response.
        """
        if request.method == "POST":
            class LineDataObject:
                area: str
                group: str
                program: str
                description: str

                @classmethod
                def from_dictreader_row(cls, dict_keys: dict, dict_row: dict):
                    new_line = cls()
                    new_line.area = dict_row.get(dict_keys["area"])
                    new_line.group = dict_row.get(dict_keys["group"])
                    new_line.program = dict_row.get(dict_keys["program"])
                    new_line.description = dict_row.get(dict_keys["description"])
                    return new_line

            def group_entity(
                group_key: str, data_read: List[str]
            ) -> Dict[str, List[LineDataObject]]:
                def tuple_to_dict(
                    tup_lines: Tuple[str, List[LineDataObject]]
                ) -> Dict[str, List[LineDataObject]]:
                    new_dict = {}
                    for key, list_obj in tup_lines:
                        new_dict.setdefault(key, []).append(list_obj)
                    return new_dict

                tuple_list = [(x.__dict__[group_key], x) for x in data_read]
                return tuple_to_dict(tuple_list)

            inmemory_csv_file = request.FILES["csv_file"]
            read_file = inmemory_csv_file.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(read_file))
            keys = dict(
                area=reader.fieldnames[0],
                group=reader.fieldnames[1],
                program=reader.fieldnames[2],
                description=reader.fieldnames[3],
            )
            line_objects = []
            for row in reader:
                line_objects.append(LineDataObject.from_dictreader_row(keys, row))
            # All previous areas and related objects will be removed.
            Area.objects.all().delete()
            read_areas = group_entity("area", line_objects)
            for r_area, r_area_values in read_areas.items():
                # Create new area
                c_area = Area(name=r_area)
                c_area.save()
                read_groups = group_entity("group", r_area_values)
                for r_group, r_group_values in read_groups.items():
                    # Create new group
                    c_group = Group(name=r_group, area=c_area)
                    c_group.save()
                    read_programs = group_entity("program", r_group_values)
                    for r_program, r_program_values in read_programs.items():
                        # Create new program
                        c_program = Program(name=r_program, group=c_group)
                        c_program.save()
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )

# Models exposed to the admin page .
admin.site.register(EpicUser)
admin.site.register(Area, AreaAdmin)
admin.site.register(Group)
admin.site.register(Program)
admin.site.register(Question)
admin.site.register(Answer)